import zipfile
from tkinter import Tk, Toplevel, Label, Button, Frame, filedialog, Radiobutton, IntVar


class Tl_TaskView(Toplevel):
    def __init__(self, r: Tk, task_line):
        super().__init__(r, bg='white')
        self.geometry('350x500+520+100')
        self.title(task_line)
        self.info = r.info
        self.task_dict_list = r.task_dict_list

        self.btns = []
        self.filepath_int = IntVar()

        # print(self.task_list)
        for task in r.task_list:
            name = ''
            for ch in task:
                if ch == '\n':
                    break
                else:
                    name += ch
            # print(task_line, name)
            if task_line == name:
                if task.index(task_line) == 0:
                    Label(self, text='任务名：' +
                          name, anchor='w').pack(fill='x')
        # print(task_line)
        filenames = []
        for task_dict in r.task_dict_list:
            temp_list = list(task_dict.keys())
            if task_line in temp_list:
                # print(task_line, task_dict[task_line]+'ll')
                # print(temp_list)
                for filepath in temp_list:
                    if temp_list.index(filepath):
                        filenames.append('')
                        btn = Radiobutton(self, text=filepath+': ', variable=self.filepath_int, activebackground='lightgreen', bg='white',
                                          value=temp_list.index(filepath), anchor='w', command=lambda: self.get_filename(filenames, self.btns[self.filepath_int.get()-1]))
                        btn.pack(fill='x')
                        self.btns.append(btn)
                break

        Button(self, text='单击此按钮，可使本窗口最大化', relief='flat',
               command=lambda: self.state('zoomed')).pack(fill='x')
        Button(self, text='单击此按钮，查看重要的注意事项', relief='flat',
               command=lambda: self.prompt(self)).pack(fill='x')

        Frame_bool = Frame(self)
        self.btn = Button(Frame_bool, text='确定', command=lambda: self.get_files(task_line, filenames, self), bg='lightgreen', width=20,
                          relief='flat', activebackground='green')
        self.btn.pack(side='left', fill='x', expand=True)
        Button(Frame_bool, text='取消', command=lambda: self.destroy(), bg='white', width=20,
               relief='flat', activebackground='red').pack(side='right', fill='x', expand=True)
        Frame_bool.pack(side='bottom', fill='x')

    def get_filename(self, filenames, btn):
        # print(filenames)
        file = filedialog.askopenfilename()
        if not file == None:
            filenames[self.filepath_int.get()-1] = file
        else:
            return 0

        name = ''
        for ch in btn['text']:
            if ch == ':':
                break
            else:
                name += ch
        btn['text'] = f'{name}: {file}'

    def prompt(self, root: Toplevel):
        r = Toplevel(root)
        r.title('注意事项')
        r.geometry('450x500+895+100')
        Label(r, text='''
温馨提示
不强制要求提交的文件与任务中提到的文件名同名，
本软件将在压缩过程中自动为文件进行重命名
(请注意：软件会保留您所上传的文件的原有文件格式)

请确保压缩包生成路径是存在的，否则将无法正常生成压缩包
请不要修改压缩包的文件名，否则将导致归档端解压缩失败''').pack(fill='both')

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
                    # print(task_name, self.task_dict_list)
                    for task_dict in self.task_dict_list:
                        if task_name in task_dict.keys():
                            break
                    # print(task_name, list(task_dict.keys())[1:])
                    for filename in filenames:
                        # print(filename)
                        if filename == '':
                            self.btn['text'] = '确定[您还有未选择的文件！]'
                            return 0
                        temp_str = filename[::-1]
                        filetype = ''
                        flag = 1
                        for ch in temp_str:
                            if ch == '/':
                                break
                            elif flag:
                                filetype += ch
                            if ch == '.':
                                flag = 0

                        mainname = ''
                        for ch in list(task_dict.keys())[1:][filenames.index(filename)][::-1]:
                            if flag:
                                mainname += ch
                            if ch == '.':
                                flag = 1

                        zipf.write(filenames[0], self.info[1][:-1] + '-' + self.info[0][:-1] + '/' +
                                   mainname[::-1] + filetype[::-1])
            r.destroy()
        else:
            self.btn['text'] = '确定[您还未选择任何文件！]'
