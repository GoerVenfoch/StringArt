class MainScreenModel:
    def __init__(self):
        self._observers = []
        self.selected_file = ''

    def notify_observers(self):
        for observer in self._observers:
            observer.model_is_changed()

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)
        