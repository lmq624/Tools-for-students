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

        btn_path = Button(frame_path, text='指定生成路径：',
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
        f_analysis = open(filename, 'r', encoding='utf-8')
        allinfo = f_analysis.readlines()
        temp_res = ''
        flag = False
        for line in allinfo:
            if line[0] == '|':
                temp_res += line[2:]
                flag = True
            if flag and not line[0] == '|':
                flag = False
                self.task_list.append(temp_res)
                temp_res = ''  # 这句真得很重要

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
            btn = Radiobutton(self.r, text='未完成任务：'+task_line, command=lambda: self.get_zipfile(task_lines[self.now_int.get()]),
                              variable=self.now_int, value=task_lines.index(task_line), anchor=W)
            btn.pack(fill='x')
            self.btns_task.append(btn)

    def get_zipfile(self, task_line):
        r = Toplevel(self.r)
        r.geometry('350x500+460+100')
        r.title(task_line)

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
                    Label(r, text='任务名以及需要提交的文件：' +
                          task[:-1], anchor=W).pack(fill='x')
        Button(r, text='选择符合要求的文件（长按CTRL键可多选）：',
               command=lambda: self.get_paths(name)).pack(fill='x')

    def get_paths(self, task_name):
        filenames = []
        files = filedialog.askopenfiles()
        for file in files:
            filenames.append(file.name)
        if filenames.__len__() > 0:
            with zipfile.ZipFile(self.f_info.path+'/'+task_name+'.zip', 'w') as zipf:
                if filenames.__len__() == 1:
                    temp_str = filenames[0][::-1]
                    filetype = ''
                    for ch in temp_str:
                        filetype += ch
                        if ch == '.':
                            break
                    zipf.write(filenames[0], task_name + '-' +
                               self.f_info.num + '-' + self.f_info.name + filetype[::-1])
                else:
                    for filename in filenames:
                        pass


uploader_tk()
pass
