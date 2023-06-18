from threading import Thread

from kivy.properties import ObjectProperty
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import sounddevice as sd
import vosk

import json
import queue

import voice_assist.words as words
import voice_assist.voice as voice
import View.ViewInstuctionScreen.view_instuction_screen as screen
from Model.voice_assist import VoiceAssistantModel
from Utility.subject_voice_assist import SubjectVoiceAssistant
from Utility.observer_voice_assist import ObserverVoiceAssistant


class VoiceAssistant(ObserverVoiceAssistant):
    model = VoiceAssistantModel()
    subject = SubjectVoiceAssistant()

    def __init__(self):
        self.subject.attach(self)
        self.q = queue.Queue()
        self.device = sd.default.device
        self.samplerate = int(sd.query_devices(self.device[0], 'input')['default_samplerate'])

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    # Анализ распознанной речи
    def recognize(self, data, vectorizer, clf):
        # проверяем есть ли имя бота в data, если нет, то return
        trg = words.TRIGGERS.intersection(data.split())
        if not trg:
            return

        # удаляем имя бота из текста
        data.replace(list(trg)[0], '')

        # получаем вектор полученного текста
        # сравниваем с вариантами, получая наиболее подходящий ответ
        text_vector = vectorizer.transform([data]).toarray()[0]
        answer = clf.predict([text_vector])[0]

        # получение имени функции из ответа из data_set
        func_name = answer.split()[0]

        # озвучка ответа из модели data_set
        voice.speaker(answer.replace(func_name, ''))

        # запуск функции
        if func_name == 'put_data_pause':
            self.subject.put_data_pause()
        elif func_name == 'do_fast':
            if self.model.slider_value < 5:
                self.model.slider_value += 1
            self.subject.put_data_speed(self.model.slider_value)
        elif func_name == 'slow_down':
            if self.model.slider_value > -5:
                self.model.slider_value -= 1
            self.subject.put_data_speed(self.model.slider_value)
        elif func_name == 'passive':
            pass
        # exec('self.subject.' + func_name + '()')

    def voice_assist(self):
        # Обучение матрицы на data_set модели
        vectorizer = CountVectorizer()
        vectors = vectorizer.fit_transform(list(words.data_set.keys()))
        model = vosk.Model('voice_assist/model_small')

        clf = LogisticRegression()
        clf.fit(vectors, list(words.data_set.values()))

        del words.data_set

        # постоянная прослушка микрофона
        def listening_thread():
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=16000, device=self.device[0], dtype='int16',
                                   channels=1, callback=self.callback):

                rec = vosk.KaldiRecognizer(model, self.samplerate)
                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        data = json.loads(rec.Result())['text']
                        print(data)
                        self.recognize(data, vectorizer, clf)
                    # else:
                    #     print(rec.PartialResult())

        thread = Thread(target=listening_thread)
        thread.daemon = True
        thread.start()
