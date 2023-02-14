from ctypes import OleDLL
from tkinter import Tk, Toplevel, Button, Text, Label, Frame
import os
import time
import zipfile

cur_path = os.path.dirname(__file__)


class Toplevel_task(Toplevel):
    def __init__(self, r, event):
        super().__init__(r)
        self.title('生成新任务')
        self.attributes('-toolwindow', 1)
        self.geometry(
            f'350x500+{int(event.x_root-60)}+{int(event.y_root-70)}')

        Label(self, text='【必填】任务名称/文件夹名称：').pack(anchor='w')
        self.text_name = Text(self, height=1)
        self.text_name.pack(fill='x')
        Label(self, text='所需提交的文件名(最好包括文件类型)列表：').pack(anchor='w')
        Button(self, text='清空本行以下文字', relief='groove',
               command=lambda: self.task_name.delete(1.0, 'end')).pack(fill='x')
        self.task_name = Text(self, height=25)
        example = '''
模拟电子线路仿真项目一实验报告.docx
温控声光报警器.ms14
项目概述.doc

（注：Windows系统内，文件名不得含有以下任何半角字符：\ / : * ? " < > | ）
（由本软件功能运行(压缩、解压缩)要求：文件名内不得含有等号，即“=”。）
（当本文本框被清空时或仅填一项时，压缩包将被解压为单文件，否则为文件夹）
（以上都是引导用的例子，实际使用时应该删除它们）'''
        self.task_name.insert(1.0, example)
        self.task_name.pack(fill='x')

        Frame_bool = Frame(self)
        self.btn = Button(Frame_bool, text='确定', command=self.add_tack, bg='lightgreen', width=20,
                          relief='flat', activebackground='green')
        self.btn.pack(side='left', fill='x', expand=True)
        Button(Frame_bool, text='取消', command=self.destroy, bg='white', width=20,
               relief='flat', activebackground='red').pack(side='right', fill='x', expand=True)
        Frame_bool.pack(side='bottom', fill='x')

    def add_tack(self):
        if self.text_name.get(1.0, 'end')[:-1] == '':
            self.btn['text'] = '确定[任务名称为必填项！]'
            return None
        f = open(cur_path+'\\tasks\\' +
                 self.text_name.get(1.0, 'end')[:-1]+'.task.txt', 'w', encoding='utf-8')
        tasks = self.task_name.get(1.0, 'end')
        res_str = self.text_name.get(1.0, 'end')
        temp_str = ''
        for ch in tasks:
            if ch == '\n':
                if temp_str.__len__() and not self.isonlyhaveBlank(temp_str):
                    res_str += temp_str+ch
                temp_str = ''
            else:
                temp_str += ch
        f.write(res_str)
        f.close()
        os.mkdir(cur_path+'\\已解压的文件\\'+self.text_name.get(1.0, 'end')[:-1])
        self.destroy()

    def isonlyhaveBlank(self, test_str):
        for ch in test_str:
            if not ch == ' ' and not ch == '\t' and not ch == '\n':
                return False
        return True


class archive_tk(Tk):
    def __init__(self):
        super().__init__()
        OleDLL('shcore').SetProcessDpiAwareness(1)
        self.title('归档端')
        self.geometry('300x255+1000+200')

        # 名单
        Button(self, text='修改名单/查看名单', height=3,
               relief='groove', bg='LightBlue',
               command=lambda: os.startfile(cur_path+'\\name_list.txt')).pack(fill='both')

        # 任务
        Frame_task = Frame(self)
        btn_task = Button(Frame_task, text='生成新任务', width=20, height=3,
                          relief='groove', bg='cyan')
        btn_task.pack(side='right', fill='x', expand=1)
        btn_task.bind('<Button-1>', lambda event: Toplevel_task(self, event))
        Button(Frame_task, text='查看已有任务', width=20, height=3,
               relief='groove', bg='DeepSkyBlue',
               command=lambda: os.startfile(cur_path+'\\tasks')).pack(side='left', fill='x', expand=1)
        Frame_task.pack(fill='x')

        # 统计
        Frame_statistics = Frame(self)
        Button(Frame_statistics, text='生成统计文件', width=20, height=3,
               relief='groove', bg='Aquamarine',
               command=self.statistics).pack(side='right', fill='x', expand=1)
        Button(Frame_statistics, text='查看已有统计文件', width=20, height=3,
               relief='groove', bg='DodgerBlue',
               command=lambda: os.startfile(cur_path+'\\统计文件')).pack(side='left', fill='x', expand=1)
        Frame_statistics.pack(fill='x')

        # 解压
        Frame_zipfile = Frame(self)
        Button(Frame_zipfile, text='查看已解压的文件', width=20, height=3,
               relief='groove', bg='RoyalBlue',
               command=lambda: os.startfile(cur_path+'\\已解压的文件')
               ).pack(side='left', fill='x', expand=1)
        for root, dirs, files in os.walk(cur_path+'\\待解压的文件'):
            if root == cur_path+'\\待解压的文件':
                ZipfileNum = files.__len__()  # + dirs.__len__()
        self.btn_zipf = Button(Frame_zipfile, text='解压文件\n待解压数量：' + str(ZipfileNum),
                               relief='groove', bg='PaleGreen',
                               width=20, height=3, command=self.read_zip)
        self.btn_zipf.pack(side='right', fill='x', expand=1)
        Frame_zipfile.pack(fill='x')

        self.mainloop()

    def statistics(self):
        f = open(cur_path+'\\统计文件\\'+'常规统计_%s.log' %
                 (time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())), 'w', encoding='utf-8')

        # 读名单
        num_list = []
        name_list = []
        res_list = []  # 统计未提交的相关情况
        f_name_list = open(cur_path +
                           '\\name_list.txt', 'r', encoding='utf-8')
        nn_list = f_name_list.readlines()
        # print(nn_list)
        f_name_list.close()
        for i in range(nn_list.__len__()):
            if not '\n' in nn_list[i]:
                nn_list[i] += '\n'
            if not nn_list[i] == None:
                if i % 2 == 0:
                    # num
                    # print(nn_list[i][:-1])
                    num_list.append(nn_list[i])
                    res_list.append([nn_list[i]])
                else:
                    # name, 要考虑到同名情况
                    # print(nn_list[i][:-1])
                    name_list.append(nn_list[i])
        f.write('名单概览：\n')
        i = 0
        for num in num_list:
            f.write(num[:-1]+'-'+name_list[i][:-1]+', ')
            i += 1
            if i % 8 == 0:
                f.write('\n')
        f.write('\n\n')

        # 读任务，从tasks文件夹获取任务信息
        task_list = []
        for root, dirs, files in os.walk(cur_path+'\\tasks'):
            for file in files:
                # print(root + '\\' + file)
                f_tasks = open(root + '\\' + file, 'r', encoding='utf-8')
                task_list.append(f_tasks.readlines())
                f_tasks.close()
        # print(num_list, name_list, task_list, res_list)

        # 遍历文件夹：已解压的文件。顺便写入以任务为主要对象的统计字段
        f.write('## 任务层次未交情况统计 ##')
        len_of_dir = (cur_path + '\\已解压的文件').__len__() + 1
        for root, dirs, files in os.walk(cur_path + '\\已解压的文件'):
            if root == cur_path + '\\已解压的文件':
                pass
            elif '\\' in root[len_of_dir:]:
                pass
            else:
                # print(root)
                # print(root[len_of_dir:], dirs, files)
                # print(task_list)
                for task in task_list:
                    if root[len_of_dir:] == task[0][:-1]:
                        f.write('\n任务名：'+task[0][:-1]+'\n')
                        f.write('| '+task[0])
                        for task_info in task[1:]:
                            f.write('| '+task_info)
                        f.write(f'已交数量：{files.__len__()+dirs.__len__()}\n')
                        f.write(
                            f'未交数量：{num_list.__len__()-files.__len__()-dirs.__len__()}\n')
                        # print(task[0][:-1], files)

                        for res in res_list:
                            hasupload = False
                            if dirs.__len__() == 0:
                                # print(dirs.__len__(), files)
                                for file in files:
                                    # print(res[0][:-1], file)
                                    if res[0][:-1] in file:
                                        hasupload = True
                                        break
                                if hasupload == False:
                                    res.append(task[0])
                            else:
                                for dir_ in dirs:
                                    # print(dir_[-root.__len__():])
                                    if res[0][:-1] in dir_[-root.__len__():]:
                                        hasupload = True
                                        break
                                if hasupload == False:
                                    res.append(task[0])

        # print(num_list, name_list, task_list)
        # print(res_list)

        f.write('\n## 个人层次未交情况统计 ##')
        for res in res_list:
            for student_info in res:
                if res.index(student_info):
                    f.write(student_info[:-1]+'|')
                else:
                    f.write('\n'+student_info[:-1]+': ')
        f.write('\n')

        f.close()

    def read_zip(self):
        for root, dirs, files in os.walk(cur_path+'\\待解压的文件'):
            for f in files:
                # print(root + '\\' + f)
                with zipfile.ZipFile(root + '\\' + f, 'r') as zipf:
                    # print(f)
                    task_name = ''
                    for ch in f[:-4][::-1]:
                        if ch == '=':
                            break
                        else:
                            task_name += ch
                    zipf.extractall(os.path.dirname(
                        __file__)+'\\已解压的文件\\'+task_name[::-1])
                os.remove(root + '\\' + f)
        for root, dirs, files in os.walk(cur_path+'\\待解压的文件'):
            self.btn_zipf['text'] = '解压文件\n待解压数量：' + str(files.__len__())


archive_tk()
pass
