from tkinter import Tk, Canvas, Radiobutton, Toplevel, Label, Button, Frame, filedialog, FLAT, W, BOTH, IntVar
from ctypes import OleDLL
from Tl import Tl_nnp
from os.path import join, dirname
import zipfile


class main(Tk):
    def __init__(self):
        OleDLL('shcore').SetProcessDpiAwareness(1)
        super().__init__()

        self.geometry('400x220+100+100')
        self.title('上传端')
        self.resizable(0, 0)

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
            fill='lightgreen', tag='nnp')

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
            10, 175, text='单击选择：常规统计.{creat_time}.log 文件\n——自动进行任务读取操作', anchor='w', tag='log', font=('楷体', 11))

        self.cv.tag_bind('nnp', '<Button-1>',
                         lambda event: Tl_nnp(self, event))
        self.cv.tag_bind('log', '<Button-1>',
                         lambda event: self.file_analysis(
                             filedialog.askopenfilename()))

        self.btns_task = []
        self.now_int = IntVar()
        self.filepath_int = IntVar()

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
        self.update_frame_task(task_lines)
        f_analysis.close()

    def update_frame_task(self, task_lines):
        r = Toplevel(self)
        r.geometry('400x220+100+420')
        r.title('任务视窗')
        Label(r, text=f'还有 {task_lines.__len__()} 项未完成任务',
              anchor='w').pack(fill='x')
        if self.btns_task.__len__():
            for btn in self.btns_task:
                btn.destroy()
            self.btns_task = []
        for task_line in task_lines:
            btn = Radiobutton(r, text=f'未完成任务{task_lines.index(task_line)+1}：'+task_line, command=lambda: self.get_zipfile(task_lines[self.now_int.get()]),
                              variable=self.now_int, value=task_lines.index(task_line), anchor=W)
            btn.pack(fill='x')
            self.btns_task.append(btn)

    def get_zipfile(self, task_line):
        # print(task_line)
        r = Toplevel(self)
        r.geometry('350x500+460+100')
        r.title(task_line)
        r.btns = []

        # print(self.task_list)
        for task in self.task_list:
            name = ''
            for ch in task:
                if ch == '\n':
                    break
                else:
                    name += ch
            # print(task_line, name)
            if task_line == name:
                if task.index(task_line) == 0:
                    Label(r, text='任务名：' +
                          name, anchor=W).pack(fill='x')
        # print(task_line)
        filenames = []
        for task_dict in self.task_dict_list:
            temp_list = list(task_dict.keys())
            if task_line in temp_list:
                # print(task_line, task_dict[task_line]+'ll')
                # print(temp_list)
                for filepath in temp_list:
                    if temp_list.index(filepath):
                        filenames.append('')
                        btn = Radiobutton(r, text=filepath+': ', variable=self.filepath_int, activebackground='lightgreen', bg='white',
                                          value=temp_list.index(filepath), anchor=W, command=lambda: self.get_filename(filenames, r.btns[self.filepath_int.get()-1]))
                        btn.pack(fill='x')
                        r.btns.append(btn)
                break

        Button(r, text='单击此按钮，可使本窗口最大化',
               command=lambda: r.state('zoomed')).pack(fill='x')
        Button(r, text='单击此按钮，查看重要的注意事项',
               command=lambda: self.prompt(r)).pack(fill='x')

        Frame_bool = Frame(r)
        self.btn = Button(Frame_bool, text='确定', command=lambda: self.get_files(task_line, filenames, r), bg='lightgreen', width=20,
                          relief=FLAT, activebackground='green')
        self.btn.pack(side='left', fill='x', expand=True)
        Button(Frame_bool, text='取消', command=lambda: r.destroy(), bg='white', width=20,
               relief=FLAT, activebackground='red').pack(side='right', fill='x', expand=True)
        Frame_bool.pack(side='bottom', fill='x')

    def prompt(self, root: Toplevel):
        r = Toplevel(root)
        r.title('注意事项')
        r.geometry('350x500+820+100')
        Label(r, text='''
温馨提示
不强制要求提交的文件与任务中提到的文件名同名，
本软件将在压缩过程中自动为文件进行重命名
(请注意：软件会保留您所上传的文件的原有文件格式)

请确保压缩包生成路径是存在的，否则将无法正常生成压缩包
请不要修改压缩包的文件名，否则将导致归档端解压缩失败''').pack(fill=BOTH)

    def get_filename(self, filenames, btn):
        # print(filenames)
        file = filedialog.askopenfile()
        if not file == None:
            filenames[self.filepath_int.get()-1] = file.name
        else:
            return 0

        name = ''
        for ch in btn['text']:
            if ch == ':':
                break
            else:
                name += ch
        btn['text'] = f'{name}: {file.name}'

    def get_files(self, task_name, filenames, r: Toplevel):
        # print(task_name)
        if filenames.__len__() > 0:
            with zipfile.ZipFile(self.info[2]+'/' + self.info[1][:-1] + '-' + self.info[0][:-1] + '=' + task_name + '.zip', 'w') as zipf:
                if filenames.__len__() == 1:
                    temp_str = filenames[0][::-1]
                    filetype = ''
                    for ch in temp_str:
                        filetype += ch
                        if ch == '.':
                            break
                    zipf.write(filenames[0],  # task_name + '-' +
                               self.info[1][:-1] + '-' + self.info[0][:-1] + filetype[::-1])
                else:
                    for filename in filenames:
                        # print(filename)
                        if filename == '':
                            self.btn['text'] = '确定[您还有未选择的文件！]'
                            return 0
                        temp_str = filename[::-1]
                        filetype = ''
                        mainname = ''
                        flag = 1
                        for ch in temp_str:
                            if ch == '/':
                                break
                            elif flag:
                                filetype += ch
                            else:
                                mainname += ch
                            if ch == '.':
                                flag = 0
                        zipf.write(filenames[0], self.info[1][:-1] + '-' + self.info[0][:-1] + '/' +
                                   mainname[::-1] + filetype[::-1])
            r.destroy()
        else:
            self.btn['text'] = '确定[您还未选择任何文件！]'


if __name__ == "__main__":
    main().mainloop()
