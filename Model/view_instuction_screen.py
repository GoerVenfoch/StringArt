class ViewInstructionScreenModel:
    def __init__(self):
        self.num_points = 0
        self.list_inst = []
        self.label_references = []
        self.schedule_interval = 6
        self.current_ind_list = 0
        self.is_paused = False
        self.size_list_buffer_outlist = 15
        self.buffer_outlist = []

