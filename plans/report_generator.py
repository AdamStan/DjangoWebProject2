import xlwt
import os
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))


class BasicAlgorithmReport:
    def __init__(self, time, result_value, quality_function_name, other_info_dict=None, lists_with_results=[],
                 file_name="report_"):
        self.time_of_execution = time
        self.result_value = result_value
        self.quality_function_name = quality_function_name
        self.info_dict = other_info_dict
        self.lists_with_results = lists_with_results
        self.file_name = file_name

    def create_report(self):
        print(dir_path)
        book = xlwt.Workbook()
        sh = book.add_sheet('A Test Sheet')

        variables = [self.time_of_execution, self.result_value, self.quality_function_name]
        x_desc = 'time_of_execution'
        y_desc = 'result_value'
        z_desc = 'quality_function_name'
        desc = [x_desc, y_desc, z_desc]

        for n, (v_desc, v) in enumerate(zip(desc, variables)):
            sh.write(n, 0, v_desc)
            sh.write(n, 1, v)

        for m, (key, value) in enumerate(self.info_dict.items()):
            sh.write(3 + m, 0, key)
            sh.write(3 + m, 1, value)

        for i in range(len(self.lists_with_results)):
            for result_index in range(len(self.lists_with_results[i])):
                sh.write(1 + result_index, 3 + i, self.lists_with_results[i][result_index])
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H-%M-%S")
        print("Current Time =", current_time)
        # TODO: save values in dictionary!
        file_name = self.file_name + current_time + "_.xls"
        book.save(file_name)
        return file_name

    def send_on_email(self):
        pass
