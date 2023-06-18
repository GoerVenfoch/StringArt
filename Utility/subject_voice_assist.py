from typing import List
from Utility.observer_voice_assist import ObserverVoiceAssistant


class SubjectVoiceAssistant:
    _observers: List[ObserverVoiceAssistant] = []
    _is_pause = True
    _slider_value = 0
    _current_number = 0

    def attach(self, observer: ObserverVoiceAssistant) -> None:
        self._observers.append(observer)

    def detach(self, observer: ObserverVoiceAssistant) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def notify_pause(self) -> None:
        for observer in self._observers:
            observer.update_pause(self)

    def notify_pin(self) -> None:
        for observer in self._observers:
            observer.update_pin(self)

    def notify_speed(self) -> None:
        for observer in self._observers:
            observer.update_speed(self)

    def put_data_pause(self) -> None:
        self._is_pause = not self._is_pause
        self.notify_pause()

    def put_data_pin(self, pin) -> None:
        self._current_number = pin
        self.notify_pin()

    def put_data_speed(self, value) -> None:
        self._slider_value = value
        self.notify_speed()

