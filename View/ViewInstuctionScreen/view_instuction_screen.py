from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from Utility.observer import Observer
from Utility.subject import Subject


class ViewInstructionScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()
    subject = Subject()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.subject.attach(self)
        for i in range(self.model.size_list_buffer_outlist):
            label = MDLabel(halign='center')
            self.model.label_references.append(label)
            self.ids.inst_list.add_widget(label)

    def update(self, subject):
        self.model.selected_file = subject._path_file
        self.model.list_inst = subject._list_inst

    def on_enter(self):
        self.ids.play_pause_button.icon = "pause"
        self.on_start()

    def on_start(self):
        self.model.buffer_outlist = [''] * self.model.size_list_buffer_outlist
        current_index = self.model.current_ind_list - int(self.model.size_list_buffer_outlist / 2) - 1

        for i in range(self.model.size_list_buffer_outlist):
            if 0 <= i + current_index < len(self.model.list_inst):
                self.model.buffer_outlist.append(self.model.list_inst[i + current_index])
            else:
                self.model.buffer_outlist.append("")
            if current_index > len(self.model.list_inst):
                self.model.buffer_outlist = self.model.buffer_outlist[::-1]
        # print(self.model.list_inst[i])
        self.update_inst_list()
        self.ids.num_lines.text = f"{self.model.current_ind_list} / {len(self.model.list_inst)}"
        self.schedule_read_list_inst()

    def schedule_read_list_inst(self):
        Clock.schedule_once(self.read_list_inst, self.model.schedule_interval)

    def read_list_inst(self, dt):
        if self.model.current_ind_list < len(self.model.list_inst):
            if (self.model.current_ind_list + int(self.model.size_list_buffer_outlist / 2)) < len(self.model.list_inst):
                self.model.buffer_outlist\
                    .append(self.model.list_inst[self.model.current_ind_list +
                                                 int(self.model.size_list_buffer_outlist / 2)])
            else:
                self.model.buffer_outlist.append("")
            self.model.buffer_outlist = self.model.buffer_outlist[-self.model.size_list_buffer_outlist:]
            print(self.model.buffer_outlist)
            self.update_inst_list()
            self.model.current_ind_list += 1
            self.ids.num_lines.text = f"{self.model.current_ind_list} / {len(self.model.list_inst)}"
            self.schedule_read_list_inst()
        else:
            Clock.unschedule(self.read_list_inst)

    def update_inst_list(self):
        for i in range(self.model.size_list_buffer_outlist):
            self.model.label_references[i].text = self.model.buffer_outlist[i]

    def toggle_play_pause(self):
        self.model.is_paused = not self.model.is_paused
        if self.model.is_paused:
            Clock.unschedule(self.read_list_inst)
            self.ids.play_pause_button.icon = "play"
        else:
            self.ids.play_pause_button.icon = "pause"
            Clock.schedule_once(self.read_list_inst, self.model.schedule_interval)


class SearchLine(Popup):
    def __init__(self, obj, **kwargs):
        super(SearchLine, self).__init__(**kwargs)
        self.obj_visv = obj

    def search_line(self, text):
        try:
            self.obj_visv.model.current_ind_list = self.obj_visv.model.list_inst.index(text)
            print(self.obj_visv.model.current_ind_list)
            self.obj_visv.on_start()
        except ValueError:
            toast("No found!")
