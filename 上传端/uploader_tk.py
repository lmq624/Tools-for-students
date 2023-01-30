# uploader_tk.py
from tkinter import *
from tkinter import filedialog
import os


class Frame_info(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)

        f = open(os.path.dirname(__file__) + '/info', 'r', encoding='utf-8')
        self.name = f.readline()[:-1]
        self.num = f.readline()[:-1]
        self.path = f.readline()
        f.close()

        frame_name_num = Frame(self)

        label_name = Label(frame_name_num, text='姓名：', anchor=E)
        label_name.pack(side='left')

        self.text_name = Text(frame_name_num, width=10, height=1)
        self.text_name.insert(1.0, self.name)
        self.text_name.pack(side='left')

        label_num = Label(frame_name_num, text='        学号：', anchor=E)
        label_num.pack(side='left', fill='x')

        self.text_num = Text(frame_name_num, width=12, height=1)
        self.text_num.insert(1.0, self.num)
        self.text_num.pack(side='left', fill='x')

        frame_name_num.pack(fill='x')

        frame_path = Frame(self)

        btn_path = Button(frame_path, text='指定生成路径：',
                          anchor=E, command=self.get_path)
        btn_path.pack(side='left')

        self.text_path = Text(frame_path, height=1)
        self.text_path.insert(1.0, self.path)
        self.text_path.pack(side='left', fill='x')

        frame_path.pack(fill='x')

        self.bind('<Motion>', self.update_info)
        self.text_name.bind('<Motion>', self.update_info)
        self.text_num.bind('<Motion>', self.update_info)
        self.text_path.bind('<Motion>', self.update_info)
        label_name.bind('<Motion>', self.update_info)
        label_num.bind('<Motion>', self.update_info)
        btn_path.bind('<Motion>', self.update_info)

    def get_path(self):
        res = filedialog.askdirectory()
        if not res == '':
            self.text_path.delete(1.0, 'end')
            self.text_path.insert(1.0, res)

    def update_info(self, event) -> None:
        name = self.text_name.get(1.0, 'end')[:-1]
        num = self.text_num.get(1.0, 'end')[:-1]
        path = self.text_path.get(1.0, 'end')[:-1]
        if not name == self.name or not num == self.num or not path == self.path:
            f = open('info', 'w', encoding='utf-8')
            nnp = name + '\n' + num + '\n' + path
            f.write(nnp)
            f.close()


class uploader_tk:
    r = Tk()
    f_info = Frame_info(r)
    btn_analysis = Button(r, text='解析统计文件', command=lambda: print(
        filedialog.askopenfilename()))

    def __init__(self):
        self.r.title('上传端')
        self.r.geometry('300x500+100+100')

        Label(self.r, text='个人信息').pack()
        self.f_info.pack(fill='x')

        # Label(self.r, text='功能按键').pack()
        self.btn_analysis.pack(fill='x')

        self.r.mainloop()


uploader_tk()
pass
