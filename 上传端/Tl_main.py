from os.path import join, dirname
from tkinter import Tk, Toplevel, Text, Label, Event, Button, Text, Frame, filedialog, Radiobutton
from Tl_TaskView import Tl_TaskView


class Tl_nnp(Toplevel):
    def __init__(self, r: Tk, event: Event):
        self.r = r

        super().__init__(r, bg='white')
        self.title('修改姓名与学号')
        self.attributes('-toolwindow', True)
        self.attributes('-topmost', True)
        self.title('编辑个人信息')
        self.geometry(
            f'200x200+{int(event.x_root-60)}+{int(event.y_root-40)}')
        Button(self, text='确定', bg='lightgreen',
               relief='flat', activebackground='green',
               command=self.okFunc).pack(
            fill='x')

        Frame_name = Frame(self)
        Label(Frame_name, text='编辑姓名：', anchor='w',
              bg='white').pack(side='left', anchor='w')
        self.Text_name = Text(Frame_name, height=1)
        self.Text_name.insert(1.0, r.info[0][:-1])
        self.Text_name.pack(side='left', fill='x')
        Frame_name.pack(fill='x')

        Frame_number = Frame(self)
        Label(Frame_number, text='编辑学号：', anchor='w',
              bg='white').pack(side='left', anchor='w')
        self.Text_number = Text(Frame_number, height=1)
        self.Text_number.insert(1.0, r.info[1][:-1])
        self.Text_number.pack(side='left', fill='x')
        Frame_number.pack(fill='x')

        self.path = ''
        Button(self, text='单击重选压缩包生成路径',
               bg='white', relief='flat', command=lambda: self.editPath()).pack(fill='x')
        self.Text_path = Text(self, height=5, bg='lightblue')
        self.Text_path.insert(1.0, r.info[2])
        self.Text_path.pack()

    def editPath(self):
        self.path = filedialog.askdirectory(title='请选择用于压缩包的文件夹')
        if not self.path == '':
            self.Text_path.delete(1.0, 'end')
            self.Text_path.insert(1.0, self.path)

    def okFunc(self):
        # print(self.Text_name.get(1.0, 'end'),
        #       self.Text_number.get(1.0, 'end'),
        #       self.Text_path.get(1.0, 'end'))
        new_name = self.Text_name.get(1.0, 'end')[:-1]
        new_number = self.Text_number.get(1.0, 'end')[:-1]
        new_path = self.Text_path.get(1.0, 'end')[:-1]
        self.r.cv.itemconfig(self.r.text_name, text='姓名：' + new_name)
        self.r.cv.itemconfig(self.r.text_number, text='学号：' + new_number)
        self.r.cv.itemconfig(self.r.text_path, text='压缩包生成路径：\n' + new_path)
        with open(join(dirname(__file__), 'info.txt'), 'w', encoding='utf-8') as f:
            f.write(f'{new_name}\n{new_number}\n{new_path}')
        with open(join(dirname(__file__), 'info.txt'), 'r', encoding='utf-8') as f:
            self.r.info = f.readlines()
        self.destroy()


class Tl_TasksView(Toplevel):
    def __init__(self, r: Tk, task_lines):
        super().__init__(r, bg='white')
        self.geometry('400x220+100+380')
        self.title('任务视窗')
        # print(task_lines)
        self.task_lines = task_lines
        self.task_dict_list = r.task_dict_list

        if task_lines.__len__():
            Label(self, text=f'还有 {task_lines.__len__()} 项任务未完成',
                  anchor='w', bg='white').pack(fill='x')
        else:
            Label(self, text='已完成所有任务！',
                  anchor='w', bg='white').pack(fill='x')
        if r.btns_task.__len__():
            for btn in r.btns_task:
                btn.destroy()
            r.btns_task = []
        for task_line in task_lines:
            btn = Radiobutton(self, text=f'未完成任务{task_lines.index(task_line)+1}：'+task_line, command=lambda: Tl_TaskView(r, task_lines[r.now_int.get()]),
                              variable=r.now_int, value=task_lines.index(task_line), anchor='w', bg='white')
            btn.pack(fill='x')
            r.btns_task.append(btn)


if __name__ == '__main__':
    # 必须导入Launch.py进行测试
    r = Tk()
    r.geometry('400x300+100+100')
    r.title('上传端')

    btn = Button(r, text='测试按钮')
    btn.bind('<Button-1>', lambda event: Tl_nnp(r, event))
    btn.pack()

    r.mainloop()
