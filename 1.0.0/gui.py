import time
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
# from RecitingAssistant import *

_version = 'v1.0.0'
"I want to know whether this can be logged in to Git by the app 'Code' on my iPad"
class TimerSimple():
    def __init__(self):
        self.time_start = None
        self.time_stop = None
        self.standby = None
        self.timerecord = None
        self.tick = self.format_ticktock()

    def _ticktock(self):
        if self.standby == None:
            self.standby = False
            self.time_start = time.time()
        elif self.standby == False:
            self.standby = True
            self.time_stop = time.time()
            self.timerecord = self.time_stop - self.time_start
            return self._format()
        else:
            self.standby = None
            self.time_stop = None
            self.standby = None
            self.timerecord = None
            return 0

    def _format(self):
        sec = int(self.timerecord)
        ms = int((self.timerecord - sec)*1000)
        clock = {'h':0, 'm':0, 's':0, 'ms':0}
        clock['h'] = sec//3600
        clock['m'] = sec//60
        clock['s'] = sec%60
        clock['ms']= ms
        return clock
    
    def format_ticktock(self):
        self._ = []
        def outer():
            def inner():
                self._.append(0)
                if len(self._)==3:
                    self._=[]
                return self._ticktock
            return inner

        try:
            d = outer()
            return str(d['h']).ljust(2,'0')+":"+str(d['m']).ljust(2,'0')+":"+str(d['s']).ljust(2,'0')+":"+str(d['ms']).ljust(3,'0')
        except:
            return None


class UI():
    def __init__(self):
        self.testOnGoing = 0 # 测试状态符；0：未开始/就绪；1：进行中；-1：暂停中
        self.clock = TimerSimple()
        self.root = tk.Tk()
        self.root.title("CL的背诵默写辅助器")
        self.root.resizable(False, False)
        self.root.geometry("720x640")

        self.mainframe = tk.Frame(self.root)
        # self.main_text_version_text = tk.Label(self.root, text="Version: "+_version)
        # self.main_text_version_text.place()
        self.mainframe.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.main_menu()

    # 主菜单界面
    def main_menu(self):

        self.main_title = tk.Label(self.mainframe, text='背诵默写小助手', font=('SJbangshu Regular',24))
        self.main_text_welcome_slogan = tk.Label(self.mainframe, text='欢迎来到背诵默写小助手！')
        self.main_button_start_test = tk.Button(self.mainframe, text='开始记忆', command=self.main_test, height=2, width=20)
        self.main_button_view_articles = tk.Button(self.mainframe, text='浏览文库', command=self.main_view_articles, height=2, width=20)
        self.main_button_view_study_record = tk.Button(self.mainframe, text='查看学习记录', command=self.view_study_record, height=2, width=20)
        self.main_button_settings = tk.Button(self.mainframe, text='设置', command=self.main_settings)
        self.main_button_about = tk.Button(self.mainframe, text='关于', command=self.main_about)
        self.main_button_exit = tk.Button(self.mainframe, text='退出', command=self.main_exit)

        self.main_title.grid(row=0, column=1)
        self.main_text_welcome_slogan.grid(row=1, column=1, pady=18)
        self.main_button_start_test.grid(row=2, column=1, pady=20)
        self.main_button_view_articles.grid(row=3, column=1, pady=0)
        self.main_button_view_study_record.grid(row=4, column=1, pady=0)
        self.main_button_settings.grid(row=5, column=0, pady=5)
        self.main_button_about.grid(row=5, column=1, pady=5)
        self.main_button_exit.grid(row=5, column=2, pady=5)

        self.root.mainloop()

    # 设置
    def main_settings(self):
        # 没想好要放些什么东西，先不做

        def Page1():
            self.setting_button_pagebutton_1preference.configure(relief=tk.SUNKEN)
            self.setting_button_pagebutton_2other.configure(relief=tk.RAISED)
            self.setting_frame_2other.place_forget()
            self.setting_frame_1preference.place(x=-1, y=28)


        def Page2():
            self.setting_button_pagebutton_1preference.configure(relief=tk.RAISED)
            self.setting_button_pagebutton_2other.configure(relief=tk.SUNKEN)
            self.setting_frame_1preference.place_forget()
            self.setting_frame_2other.place(x=-1, y=28)


        def Confirm():
            pass
            Return2menu()

        def Discard():
            pass
            Return2menu()

        def Return2menu():
            self.setting_window.destroy()

        self.setting_window = tk.Toplevel()
        self.setting_window.title("设置")
        self.setting_window.geometry("640x480")
        # setting_window.resizable(False, False)

        self.setting_frame_pageholder = tk.Frame(self.setting_window, bd=1, relief=tk.GROOVE)
        self.setting_frame_1preference = tk.Frame(self.setting_frame_pageholder, width=600, height=352, bd=1, relief=tk.GROOVE)
        self.setting_frame_2other = tk.Frame(self.setting_frame_pageholder, width=600, height=352, bd=1, relief=tk.GROOVE)
        # self.setting_frame_2other.forget()

        self.setting_button_pagebutton_1preference = tk.Button(self.setting_frame_pageholder, text='偏 好', borderwidth=1, command=Page1, relief=tk.SUNKEN, takefocus=True)
        self.setting_button_pagebutton_2other = tk.Button(self.setting_frame_pageholder, text='其 它', borderwidth=1, command=Page2, takefocus=True)
        self.setting_button_confirm = tk.Button(self.setting_window, text='确认', borderwidth=1, command=Confirm, takefocus=True)
        self.setting_buton_discard = tk.Button(self.setting_window, text='取消', borderwidth=1, command=Discard, takefocus=True)
        self.setting_button_return2menu = tk.Button(self.setting_window, text='回到主菜单', borderwidth=1, command=Return2menu, takefocus=True)

        self.setting_frame_pageholder.place(x=20, y=20, width=600, height=380)

        self.setting_button_pagebutton_1preference.place(x=0, y=0)
        self.setting_button_pagebutton_2other.place(x=37, y=0)
        Page1()
        self.setting_button_confirm.place(x=470, y=430)
        self.setting_buton_discard.place(x=510, y=430)
        self.setting_button_return2menu.place(x=550, y=430)

        notice1 = tk.Label(self.setting_frame_1preference, text='现在还没有可以设置的东西。。')
        notice2 = tk.Label(self.setting_frame_2other, text='这里也没有。。')
        notice1.place(x=10, y=20)
        notice2.place(x=10, y=20)

    # 打开文章并开始默写
    def main_test(self):
        self.mainframe.place_forget()

        def finishTest():
            self.start_frame_testSource.destroy()
            self.start_frame_testInfo.destroy()
            self.start_frame_testInput.destroy()
            self.start_frame_testResult.destroy()
            self.start_button_finishTest.destroy()
            self.mainframe.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        def viewResult():
            self.start_frame_testSource.destroy()
            self.start_frame_testInfo.destroy()
            self.start_frame_testInput.destroy()

            self.start_frame_testResult.place()

        def startTest():
            self.testOnGoing = 1

        def submitTest():
            pass

        def pauseTest():
            if self.testOnGoing == 1:
                self.start_button_pauseTest.configure(text='继续', command=continueTest)
                self.testOnGoing = -1
            else:
                return -1
        
        def continueTest():
            if self.testOnGoing == -1:
                self.start_button_pauseTest.configure(text='暂停', command=pauseTest)
                self.testOnGoing = 1
            else:
                return -1


        self.start_frame_testSource = tk.LabelFrame(self.root)
        self.start_frame_testInfo = tk.Frame(self.root)
        self.start_frame_testInput = tk.Frame(self.root)
        self.start_frame_testResult = tk.Frame(self.root)

        self.start_button_startTest = tk.Button(self.root, text='开始新测试', command=startTest)
        self.start_button_pauseTest = tk.Button(self.root, text='暂停', command=pauseTest)
        self.start_button_submitTest = tk.Button(self.root, text='提交', command=submitTest)
        self.start_button_finishTest = tk.Button(self.root, text='返回主菜单', command=finishTest)



        self.start_button_finishTest.pack()

    # 管理文档
    def main_view_articles(self):
        pass

    # 查看学习记录
    def view_study_record(self):
        pass

    # 关于信息
    def main_about(self):
        def about_finish():
            self.about_window.destroy()

        self.about_window = tk.Toplevel()
        self.about_window.title("关于程序")
        self.about_window.geometry("640x480")
        self.about_window.resizable(False, False)

        self.about_frame_about = tk.LabelFrame(self.about_window, text='关于')
        self.about_frame_help = tk.LabelFrame(self.about_window, text='帮助')
        self.about_button_finish = tk.Button(self.about_window, text='完成', command=about_finish, height=3, width=16, font=('Microsoft Yahei UI', 14))


        about_text_about_text =  '''
        本项目本是用来应付英国文学史的默写的，却意料之中的好用，故就此开源。\n
        作者：Clement_Levi  联系方式：clement_levi@qq.com \n
        GitHub: 链接改天放，先欠着 \n
        核心算法见代码
        '''
        about_text_help_text = r'''
        使用方法：
        1. 什么什么
        2. 什么什么
        3. 什么什么
        4. 什么什么'''

        

        self.about_text_about = tk.Label(self.about_frame_about, text=about_text_about_text, justify=tk.LEFT)
        self.about_text_help = tk.Label(self.about_frame_help, text=about_text_help_text, justify=tk.LEFT)

        self.about_frame_about.place(x=20, y=10, relheight=0.4, relwidth=0.9)
        self.about_frame_help.place(x=20, y=210, relheight=0.4, relwidth=0.9)
        self.about_button_finish.place(height=60, width=120, x=320-60, y=410)

        self.about_text_about.pack(side='left')
        self.about_text_help.pack(side='left')

    # 退出
    def main_exit(self):
        confirm = messagebox.askokcancel("退出", "确实要结束学习吗？")
        if confirm:
            self.mainframe.destroy()
            self.root.quit()
            exit()
        else:
            pass

if __name__ == '__main__':
    GUI = UI()