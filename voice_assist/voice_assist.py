from threading import Thread

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import sounddevice as sd
import vosk

import json
import queue

import voice_assist.words as words
import voice_assist.voice as voice
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

    # Обновляется пауза
    def update_pause(self, subject_voice_assist):
        self.model.is_pause = subject_voice_assist._is_pause

    # Обновляется скорость пролистывания инструкции
    def update_speed(self, subject_voice_assist):
        self.model.slider_value = subject_voice_assist._slider_value

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
        elif func_name == 'search_pin':
            # self.subject.put_data_pin(answer.split)
            try:
                number = text2int(data)
                self.subject.put_data_pin(number)
            except ValueError:
                pass
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
                        self.recognize(data, vectorizer, clf)
                    # else:
                    #     print(rec.PartialResult())

        thread = Thread(target=listening_thread)
        thread.daemon = True
        thread.start()


# Преобразование текста в число
def text2int(textnum, numwords=None):
    if numwords is None:
        numwords = {}
    if not numwords:
        units = [
            "ноль", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь",
            "девять", "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать",
            "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать",
        ]

        tens = ["", "", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят",
                "девяносто"]

        scales = ["сто", "тысяч", "миллион", "миллиард", "триллион"]

        numwords["и"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (1, 10 ** (idx * 3 or 2))

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            continue
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
