from typing import List
from Utility.observer import Observer


class Subject:
    _observers: List[Observer] = []
    _path_file = ""
    _num_points = 0
    _list_inst = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def put_data(self, path, num, inst) -> None:
        self._path_file = path
        self._num_points = num
        self._list_inst = inst
        self.notify()

    # def put_num_points(self, num) -> None:
    #     self._num_points = num
    #     self.notify()
    #
    # def put_list_inst(self, inst) -> None:
    #     self._list_inst = inst
    #     self.notify()
