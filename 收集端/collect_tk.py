# collect.py
from tkinter import *
from tkinter import filedialog
import os


class Toplevel_task(Toplevel):
    def __init__(self, r):
        super().__init__(r)
        self.title('生成新任务')
        self.geometry('350x500+410+100')

        Label(self, text='【必填】任务名称/文件夹名称：').pack(anchor=W)
        self.text_name = Text(self, height=1)
        self.text_name.pack(fill='x')
        Label(self, text='【至少一项】所需提交的文件名(最好包括文件类型)列表：').pack(anchor=W)
        self.task_name = Text(self, height=30)
        example = '''
模拟电子线路仿真项目一实验报告.docx
温控声光报警器.ms14
项目概述.doc

（注：Windows系统内，文件名不得含有以下任何半角字符：\ / : * ? " < > | ）
（以上都是引导用的例子，实际使用时应该删除它们）'''
        self.task_name.insert(1.0, example)
        self.task_name.pack(fill='x')

        Frame_bool = Frame(self)
        Button(Frame_bool, text='确定', command=self.add_tack, bg='lightgreen', width=20,
               relief=FLAT, activebackground='green').pack(side='left', fill='x')
        Button(Frame_bool, text='取消', command=self.destroy, bg='white', width=20,
               relief=FLAT, activebackground='red').pack(side='right', fill='x')
        Frame_bool.pack(side='bottom', fill='x')

    def add_tack(self):
        f = open(os.path.dirname(__file__)+'\\tasks\\' +
                 self.text_name.get(1.0, 'end')[:-1]+'.task.txt', 'w', encoding='utf-8')
        tasks = self.task_name.get(1.0, 'end')
        res_str = self.text_name.get(1.0, 'end')
        temp_str = ''
        for ch in tasks:
            if ch == '\n':
                if temp_str.__len__() and not self.isonlyhaveblank(temp_str):
                    res_str += temp_str+ch
                temp_str = ''
            else:
                temp_str += ch
        f.write(res_str)
        f.close()
        self.destroy()

    def isonlyhaveblank(self, test_str):
        for ch in test_str:
            if not ch == ' ' and not ch == '\t':
                return False
        return True


class collect_tk:
    r = Tk()

    def __init__(self):
        self.r.title('上传端')
        self.r.geometry('300x500+100+100')

        Button(self.r, text='生成新任务',
               command=lambda: Toplevel_task(self.r)).pack(fill='x')
        Button(self.r, text='查看已有任务', command=lambda: os.startfile(
            os.path.dirname(__file__)+'\\tasks')).pack(fill='x')
        Button(self.r, text='生成统计文件', command=lambda: print(
            filedialog.askopenfilename())).pack(fill='x')
        Button(self.r, text='查看已有统计文件', command=lambda: os.startfile(
            os.path.dirname(__file__)+'\\统计文件')).pack(fill='x')

        t_jieya = '解压文件 | '
        for root, dirs, files in os.walk(os.path.dirname(__file__)+'\\待解压的文件'):
            t_jieya += '待解压数量：' + str(files.__len__())
        Button(self.r, text=t_jieya, command=lambda: print(
            filedialog.askopenfilename())).pack(fill='x')

        self.r.mainloop()


collect_tk()
pass
