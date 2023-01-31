from RecitingAssistant import TestGiver


__MENU_OPTIONS = {'0': 'loadTest', '1': 'manage',
                '2': 'setting', '3': 'about_and_help',
                'E': 'exit'}


def shell_init():
    """Shell main entrance. Accept all command since the shell is on.
    纯文本界面入口。自shell启动后在此接受指令"""
    print("""
        ----[欢迎来到背书辅助器（Shell版）]----
        主菜单：
        【0】开始背诵默写
        【1】管理现有文档
        【2】设置
        【3】关于与帮助
        【E】退出程序
        """)
    menu_order = input("> ").capitalize()

# MENU_OPTION 0
def shell_loadTest():
    """shell下开始测试"""
    # 完成路径确认，开始收集目录内信息

    os.chdir(cwp)
    cwp = os.getcwd()
    file_menu_dict = {}

    for index in range(len(os.listdir(cwp))):
        if os.path.isfile(os.listdir(cwp)[index]):  # 判断是否为文件。我们不打开文件夹
            file_menu_dict.update({index: os.listdir(cwp)[index]})

        print("当前目录下文档如下：")
        for file_id in file_menu_dict:
            print("【{}】".format(file_id), '\t', file_menu_dict[file_id])

        # 多次收集信息，尝试打开文件

        while 1:
            file_chosen_id = int(input("请输入需要学习的文档序号："))
            if int(file_chosen_id) not in file_menu_dict.keys():
                print(" - 序号输入不正确，请检查输入！")
                continue
            else:
                print(" - 您当前选择了文件“{}”".format(file_menu_dict[file_chosen_id]))
                return './'+file_menu_dict[file_chosen_id]
    shell_start_test(shell_selectTestFile())

    return 0


def shell_selectTestFile():
    """选择文件打开
    接收一系列文本格式操作，返回最终选定的文件名（./*.*格式）"""
    cwp = input("当前目录：{}\n请输入文档存放路径（默认为./）：".format(os.getcwd()))
    if not os.path.isdir(cwp):
        print("路径输入错误，请重新输入！")
        return 0


def shell_start_test(test_file_name):
    Teacher = TestGiver()
    Teacher.open_articlef(test_file_name)
    print('当前测试信息：')
    print(Teacher.Article.show_basic_info())

    confirm_launch = input("测试加载完毕。请确认是否开始测试【Y/N】：")
    if confirm_launch != 'Y':
        print(" - 测试已取消！")
        return 0
    # 开始测试，先展示题目，后给出答题规范格式要求，最后使用eval（危）接受答题纸递交批改
    _ = Teacher.new_test()
    paper, answer = _['exam'], _['answer']
    print('''------------------------------
    考试说明：请用规范格式作答！如因作答格式不规范导致的无法批改，后果自负！
    作答样例：
    To ___#1___ or not ___#4___ ___#5___, ...
    作答格式（请注意所有标点为英文半角标点，花括号不可省略！）：
    {"1": "be", "4": "to", "5": "be"}\n------------------------------
    ''')
    print(" ==== 测试题 ====\n\n", paper, end='\n\n------------------------------\n\n')
    raw_answer_dict = eval(input(" - 测试开始，请在以下空白区域作答，完成后提交请按回车键！\n"))
    if type(raw_answer_dict) != type({0: 0}):
        print(" -  作答格式显然不正确，答题纸解析失败！测试现在结束……")
        return -1
    print("测试结束，您的错误项为：")
    for eachWrong in Teacher.correct_test(raw_answer_dict):
        print(
            "#{}: {} -> {}".format(eachWrong[0], eachWrong[1], eachWrong[2]))
    print("您的得分为：%.1f" % Teacher.testMark)
    Teacher.log_record()
    return 0

# MENU_OPTION 1
def shell_manage():
    """shell下管理文档（添加、修改原文、修改统计数据、删除等操作）"""
    pass

# MENU_OPTION 2
def shell_setting():
    """shell下打开设置（默认后缀名）"""
    pass

# MENU_OPTION 3
def shell_about_and_help():
    """shell下打开帮助（查看文档不就好了吗笨）"""
    pass

# MENU_OPTION E
def shell_exit():
    """Shell下退出程序"""
    if input("「真的要退出吗（y/N）：」").upper() == 'Y':
        exit()
    else:
        return 0


# 测试信息
def shell_save_article():
    title = 'Utopia'
    index = 0
    author = 'Moore'
    RSS = ''
    encoding = 'utf-8'
    text = '''In heaven, I replied, there is laid up a pattern of it, methinks, which he who desires may behold, and beholding, may set his own house in order. But whether such an one exists, or ever will exist in fact, is no matter; for he will live after the manner of that city, having nothing to do with any other.'''''
    a = Article()
    a.new_article(title, text, index, author, RSS, encoding=encoding)
    return 0

if __name__ == "__main__":

    while(1):
        shell_init()
        if menu_order in __MENU_OPTIONS:
            eval("shell_"+__MENU_OPTIONS[menu_order])()
