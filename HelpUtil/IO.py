from HelpUtil.DateTime import Datetime as dt


class Read:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='UTF8') as file:
            self.data_dict = {dt.strptime(pair[0].strip(), '%Y-%m-%d'): pair[1].strip() for line in file for pair in
                              [line.strip().split(':', 1)]}

    def get_data(self):
        return self.data_dict
