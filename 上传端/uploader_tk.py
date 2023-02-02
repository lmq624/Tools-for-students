# uploader_tk.py
from tkinter import *
from tkinter import filedialog
import os
import zipfile


class Frame_info(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)

        f = open(os.path.dirname(__file__) + '/info', 'r', encoding='utf-8')
        self.name = f.readline()[:-1]
        self.num = f.readline()[:-1]
        self.path = f.readline()
        f.close()

        frame_name_num = Frame(self)

        btn_update = Button(frame_name_num, text='更新个人信息：',
                            command=self.update_info)
        btn_update.pack(side='left', fill='x')

        label_name = Label(frame_name_num, text='姓名：', anchor=E)
        label_name.pack(side='left')

        self.text_name = Text(frame_name_num, width=10, height=1)
        self.text_name.insert(1.0, self.name)
        self.text_name.pack(side='left')

        label_num = Label(frame_name_num, text='学号：', anchor=E)
        label_num.pack(side='left')

        self.text_num = Text(frame_name_num, width=12, height=1)
        self.text_num.insert(1.0, self.num)
        self.text_num.pack(side='left')

        frame_name_num.pack(fill='x')

        frame_path = Frame(self)

        btn_path = Button(frame_path, text='压缩包生成路径：',
                          anchor=E, command=self.get_path)
        btn_path.pack(side='left')

        self.text_path = Text(frame_path, height=1)
        self.text_path.insert(1.0, self.path)
        self.text_path.pack(side='left', fill='x')

        frame_path.pack(fill='x')

    def get_path(self):
        res = filedialog.askdirectory()
        if not res == '':
            self.text_path.delete(1.0, 'end')
            self.text_path.insert(1.0, res)
        self.update_info()

    def update_info(self) -> None:
        self.name = self.text_name.get(1.0, 'end')[:-1]
        self.num = self.text_num.get(1.0, 'end')[:-1]
        self.path = self.text_path.get(1.0, 'end')[:-1]
        nnp = self.name + '\n' + self.num + '\n' + self.path
        # print(nnp)
        f = open(os.path.dirname(__file__)+'\\info', 'w', encoding='utf-8')
        f.write(nnp)
        f.close()


class uploader_tk:
    r = Tk()
    f_info = Frame_info(r)
    btns_task = []
    now_int = IntVar()
    filepath_int = IntVar()

    def __init__(self):
        self.r.title('上传端')
        self.r.geometry('350x500+100+100')

        Label(self.r, text='个人信息').pack()
        self.f_info.pack(fill='x')

        # Label(self.r, text='功能按键').pack()
        btn_analysis = Button(self.r, text='解析统计文件', command=lambda: self.file_analysis(
            filedialog.askopenfilename()))
        btn_analysis.pack(fill='x')

        self.r.mainloop()

    def file_analysis(self, filename):
        if filename == '':
            return None

        self.task_list = []
        self.task_dict_list = []
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
        # print(self.task_dict_list)

        allinfo.reverse()
        # print(allinfo)
        task_lines = []
        for line in allinfo:
            if self.f_info.num in line:
                if line.index(self.f_info.num) == 0:
                    # print(line[self.f_info.num.__len__()+2:])
                    temp_str = ''
                    for ch in line[self.f_info.num.__len__()+2:]:
                        if ch == '|':
                            # print(temp_str)
                            task_lines.append(temp_str)
                            temp_str = ''
                        else:
                            temp_str += ch
                    break
        self.update_frame_task(task_lines)
        f_analysis.close()

    def update_frame_task(self, task_lines):
        if self.btns_task.__len__():
            for btn in self.btns_task:
                btn.destroy()
            self.btns_task = []
        for task_line in task_lines:
            btn = Radiobutton(self.r, text=f'未完成任务{task_lines.index(task_line)+1}：'+task_line, command=lambda: self.get_zipfile(task_lines[self.now_int.get()]),
                              variable=self.now_int, value=task_lines.index(task_line), anchor=W)
            btn.pack(fill='x')
            self.btns_task.append(btn)

    def get_zipfile(self, task_line):
        # print(task_line)
        r = Toplevel(self.r)
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

        Label(r, text='\n温馨提示\n不强制要求提交的文件与任务中提到的文件名同名，\n本软件将自动在压缩过程中对文件进行重命名。\n\n请不要修改压缩包的文件名，否则将导致压缩失败').pack(
            fill='x')
        Button(r, text='单击此按钮，可使本窗口最大化',
               command=lambda: r.state('zoomed')).pack()

        Frame_bool = Frame(r)
        self.btn = Button(Frame_bool, text='确定', command=lambda: self.get_files(task_line, filenames, r), bg='lightgreen', width=20,
                          relief=FLAT, activebackground='green')
        self.btn.pack(side='left', fill='x', expand=True)
        Button(Frame_bool, text='取消', command=lambda: r.destroy(), bg='white', width=20,
               relief=FLAT, activebackground='red').pack(side='right', fill='x', expand=True)
        Frame_bool.pack(side='bottom', fill='x')

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
            with zipfile.ZipFile(self.f_info.path+'/' + self.f_info.num + '-' + self.f_info.name + '=' + task_name + '.zip', 'w') as zipf:
                if filenames.__len__() == 1:
                    temp_str = filenames[0][::-1]
                    filetype = ''
                    for ch in temp_str:
                        filetype += ch
                        if ch == '.':
                            break
                    zipf.write(filenames[0],  # task_name + '-' +
                               self.f_info.num + '-' + self.f_info.name + filetype[::-1])
                else:
                    for filename in filenames:
                        # print(filename)
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
                        zipf.write(filenames[0], self.f_info.num + '-' + self.f_info.name + '/' +
                                   mainname[::-1] + filetype[::-1])
            r.destroy()
        else:
            self.btn['text'] = '确定[您还未选择任何文件！]'


uploader_tk()
pass
