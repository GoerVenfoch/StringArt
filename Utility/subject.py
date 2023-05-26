from typing import List
from Utility.observer import Observer


class Subject:
    _observers: List[Observer] = []
    _path_file = ""

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)
        for observer in self._observers:
            print(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def put_path_file(self, path) -> None:
        print("\nSubject: I'm doing something important.}")
        self._path_file = path

        print(f"Subject: My state has just changed to: {self._path_file}")
        self.notify()
