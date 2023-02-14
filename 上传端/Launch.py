from tkinter import Tk, Canvas, filedialog, IntVar
from ctypes import OleDLL
from Tl_main import Tl_nnp, Tl_TasksView
from os.path import join, dirname


class main(Tk):
    def __init__(self):
        OleDLL('shcore').SetProcessDpiAwareness(1)
        super().__init__()

        self.geometry('400x220+100+100')
        self.title('上传端')
        self.resizable(0, 0)

        self.btns_task = []
        self.now_int = IntVar()
        self.filepath_int = IntVar()

        self.cv = Canvas(self, bg='white')
        self.cv.pack(fill='both', expand=True)

        self.setGUI()

    def setGUI(self):
        self.tag_name_and_number_and_path = 'nnp'
        self.cv.create_line((230, 10), (230, 90),
                            (370, 50), (230, 10),
                            fill='gray', width=2)
        self.cv.create_polygon(
            (230, 10), (230, 90), (370, 50),
            fill='lightgreen', tag='nnp', activefill='green')

        with open(join(dirname(__file__), 'info.txt'), 'r', encoding='utf-8') as f:
            self.info = f.readlines()

        self.text_name = self.cv.create_text(
            10, 33, text='姓名：'+self.info[0][:-1], tag='nnp', anchor='w')
        self.text_number = self.cv.create_text(
            10, 66, text='学号：'+self.info[1][:-1], tag='nnp', anchor='w')
        self.cv.create_line((5, 77), (90, 77))
        self.text_path = self.cv.create_text(
            10, 99, text='压缩包生成路径：\n'+self.info[2], tag='nnp', anchor='w')

        self.cv.create_line((0, 135), (390, 135),
                            arrow='last', dash=(1, 10))

        self.tag_readLog = 'log'
        self.cv.create_text(
            10, 175, text='单击选择：常规统计.{creat_time}.log 文件\n——自动进行任务读取操作',
            anchor='w', tag='log', font=('楷体', 11), activefill='red')

        self.cv.tag_bind('nnp', '<Button-1>',
                         lambda event: Tl_nnp(self, event))
        self.cv.tag_bind('log', '<Button-1>',
                         lambda event: self.file_analysis(
                             filedialog.askopenfilename()))

    def file_analysis(self, filename):
        if filename == '':
            return None

        # 读全部任务
        self.task_list = []
        # ['test\ntestfile.txt\n', '测试：单文件任务\n文件1.docx\n', '测试：多文件任务\n文件1.docx\n文件2.pptx\n文件3.xlsx\n']
        self.task_dict_list = []
        # [{'test': '', 'testfile.txt': ''}, {'测试：单文件任务': '', '文件1.docx': ''},
        # {'测试：多文件任务': '', '文件1.docx': '', '文件2.pptx': '', '文件3.xlsx': ''}]
        f_analysis = open(filename, 'r', encoding='utf-8')
        allinfo = f_analysis.readlines()
        temp_res = ''
        temp_task_dict = {}
        flag = False
        for line in allinfo:
            if line[0] == '|':
                temp_res += line[2:]
                temp_task_dict.setdefault(line[2:-1], '')
                # print(temp_task_dict)
                flag = True
            if flag and not line[0] == '|':
                flag = False
                self.task_list.append(temp_res)
                self.task_dict_list.append(temp_task_dict)
                temp_res = ''  # 这句真得很重要
                temp_task_dict = {}
        # print(self.task_list, self.task_dict_list)

        # 读个人任务
        allinfo.reverse()
        # print(allinfo)
        task_lines = []
        for line in allinfo:
            if self.info[1][:-1] in line:
                if line.index(self.info[1][:-1]) == 0:
                    # print(line[self.info[1][:-1].__len__()+2:])
                    temp_str = ''
                    for ch in line[self.info[1][:-1].__len__()+2:]:
                        if ch == '|':
                            # print(temp_str)
                            task_lines.append(temp_str)
                            temp_str = ''
                        else:
                            temp_str += ch
                    break
        # print(task_lines)
        Tl_TasksView(self, task_lines)
        f_analysis.close()


if __name__ == "__main__":
    main().mainloop()
