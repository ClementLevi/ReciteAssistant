import os, time, json, math, threading, difflib
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from getpass import getuser
from jieba import lcut
from string import ascii_lowercase, ascii_uppercase
from chardet import detect
from random import randint

## 核心算法
# 自动检测编码
def detectCodef(path):
    """Receive a text file path, return its possible encoding as string.
    'path': selected file."""
    with open(path, 'rb') as file:
        data = file.read(200000)
        dicts = detect(data)
    return dicts["encoding"]

def detectCodes(s):
    dicts = detect(s.encode())
    return dicts["encoding"]

# 字词分解器（接受一个字符串，返回操作结果标识符）
class Spliter:
    eng_punc_num = '''1234567890 ~,.?!&"'\\()-_+*/=@#<>:;%$[]{}|`^'''
    chi_punc = '''·！￥……（）——【】、；：‘’“”，。《》？'''

    def __init__(self, target_file=None, target_text=None):
        self.text_file = target_file
        self.text = target_text
        self.text_output = []
        self.text_type = ''
        print("<Spliter> Spliter is standing by at %s!" % hex(id(self)))
            # 没有什么用的打印输出，纯粹为了好看和装逼
        # 接收此文件
        if (not (self.text_file or self.text)):
            print("<Spliter> Text has not been input. But you can still input one later with attribute 'Spliter.text_file = './path.txt' '")
        else:
            if self.text_file:
                print("<Spliter> Text from file read in ", self.textf_read(), " characters.")
            elif self.text:
                print("<Spliter> Text from input read in ", self.texts_read(self.text), " characters.")
        print("<Spliter> Stand by...")

    def textf_read(self, f=None):
        '''从文件读取文本字符串；将会继续调用texts_read方法读取文件内容'''
        if f and os.path.exists(f):
            self.text_file = f
        file = self.text_file
        try:
            with open(file, 'rt', encoding=detectCodef(file)) as _F:
                self.textf=_F.read()
                self.texts_read(self.textf)
                return len(self.text)
        except(ValueError):
            print("【打开失败】目标文件不是文本文件或暂时不可用！")
            return -1

    def texts_read(self, string=None):
        '''从字符串直接读取'''
        if not string:
            string = self.text
        # 检测是否全数字
        if string.isdigit():
            self._numSplit()
            self.text_type = 'number'
            return len(self.text)

        # 检测是否全英文
        else:
            for i in string:
                if i in ascii_lowercase+ascii_uppercase+self.eng_punc_num: # 使用了string库里的ascii字符集来判断
                    if self.text_type == 'German' or self.text_type =='Chinese':
                        continue
                    self.text_type = 'Latin(English)'
                else:
                    if i in 'öÖüÜäÄß„‚‘“`´°§': # 顺便检测是不是德语，德语也用拉丁字解析
                        self.text_type = 'German'
                    elif '\u4e00' <= i <= '\u9fff' or i in self.chi_punc: # 纯汉语字符画（真是天才的思路）也算汉语
                        self.text_type = 'Chinese'
                    else:
                        break


        if self.text_type == 'Latin(English)' or self.text_type == 'German':
            self._latinSplit()

        # 否则用汉语解析器
        elif self.text_type == 'Chinese':
            self._chiSplit()

        else:
            print("> 无法解析的文本类型！请添加更多可解析类型！\n> Unanalyzable text. Please add more features to digest!")
            self.text_type = '?'
            return -1

        return len(self.text)

    def _chiSplit(self):
        """汉语分解器，使用结巴分词拆分文本\n
        返回拆分后的字符串列表"""
        self.text_output = lcut(self.text, cut_all=False) # 调用结巴分词的lcut精确分解模式分解汉语文本
        # https://github.com/fxsjy/jieba

        return self.text_output

    def _latinSplit(self):
        '''拉丁字符语言分解器（英文德文什么的，使用内构方法'str.split()'）\n
        返回拆分后的字符串列表'''
        self.text_output = self.text.split()
        return self.text_output

    def _numSplit(self):
        '''数字分解器（兄啊数字你也要背诵的吗）\n
        每组size位字符\n
        返回拆分后的字符串列表'''
        size, temp = 4, '' #'size'表示每小节四位数，方便记忆
        _text_temp = self.text

        while(len(_text_temp)>size):
            '''每次截取前size位字符，保存，并从临时串中移除，继续下一组字符'''
            temp += _text_temp[0:size]
            self.text_output.append(temp)
            _text_temp=_text_temp[size:]
            temp = ''
        else:
            self.text_output.append(_text_temp)


class Article:
        # 包括了常用的大部分中英德文标点符号
    _punctuations = r''' ~,.?!&"'\\()-_+*/=@#<>:;%$[]{}|`^·！￥……（）——【】、；：‘’“”，。《》？„‚‘“`´°§'''
    _illegalchar = r'''\/*?:"<>|'''
    def __init__(self, title='NewArticle'):
        """根据模板，生成一个新文档，准备接受写入的数据。\n
        self.__ignoreAttr__是被保护的变量名容器，不参与算法，只用于JSON模块操作。在其中的所有属性名都不会被导出到JSON中。\n
        JSON导出实例对象属性的方法见dumps和dumpf方法。"""
        ## 受保护的实例属性
        self._content = {} # 保护的变量容器，用于JSON导出
        self._currentFileName = '' # 当前打开文件。保存时会被dumpf()使用
        self.answer = [] # 从TestGiver类中赋值。每次新建题目都会有所不同，故特此设计
        self.__ignoreAttr__ = ["_content", "_currentFileName", "answer", "__ignoreAttr__"]  # 需要保护的变量名请写在这里
        ## 不受保护的实例属性
        # 根据下列模板生成一个新文档，准备接受各信息。
        self.basic = {
            "title": "New Article",
            "original_text": "",
            "index": 0,
            "date": "",
            "text_type": "",
            "submitter": "",
            "author": "",
            "RSS": "",
            "encoding":"utf-8"
        }
        self.content = {
            "0":{
                "word":"",
                "bw": 15,
                "Fc": 0,
                "Mw": 0,
            }
        }
        self.test_info = {
            "test_count": 0,
            "test_record":{
                "sample": [0, "time_took", "comment on this test"]
            }
        }
        self.comments = {
            "idlist":{
                "c_sample": []
            },
            "comments_content":{
                "c_sample": ""
            }
        }
        # 这些都是将于JSON中定义的变量名。不应当在导入之前就覆盖保存，否则等同删档

    def dumpf(self, file_name=None):
        '''（推荐使用）保存此文章的相关数据到JSON文件中，返回0\n
        注意：会覆盖已有的其他文本！'''
        for attr in self.__dict__:
            if attr not in self.__ignoreAttr__:
                self._content.update({attr: self.__dict__[attr]})

        if not file_name: # 无自定义文件名或路径时，默认存放在本目录下
            file_name = self.basic['title']+'-'+str(self.basic['index'])+'-'+self.basic['author']+'-'+self.basic['date']
                # 文件名默认为标题+索引+作者+日期，需注意不应含有非法字符

        # 无论有无自定义文件名，都进行筛查并保存
        for i in file_name:
            if i in self._illegalchar:
                file_name = file_name.replace(i, '_')
                    # 由此就完成了对非法字符的过滤（破坏性）
        with open('./%s.json' % file_name, 'w', encoding=self.basic["encoding"]) as file:
            json.dump(self._content, file, indent=4) # 默认都格式化比较好看，毕竟是文本文件
        return 0

    def loadf(self, file='./Article_data.json'):
        '''从JSON文件读取数据并加载到文章对象中，返回加载的数据条数'''
        self.currentFileName = file
        with open(file, 'r', encoding=detectCodef(file)) as file:
            self._content = json.load(file)

        count = 0
        for attr in self._content.keys():
            setattr(self, attr, self._content[attr])
            count += 1
        return count

    def dumps(self, strIndent=None):
        '''保存此文章的相关数据到JSON字符串中，返回该字符串\n
        strIndent=None/4: 不格式化或每个元素设置4空格缩进'''
        for attr in self.__dict__:
            if attr != '_content':
                self._content.update({attr: self.__dict__[attr]})

        jsonstr = json.dumps(self._content, indent=strIndent) # 默认不格式化，实际上也可以指定要格式化，输入4即可
        return jsonstr

    def loads(self, jsonstr):
        '''从JSON字符串读取数据并加载到文章对象中，返回加载的数据条数'''
        self._content = json.loads(jsonstr)

        count = 0
        for attr in self._content.keys():
            setattr(self, attr, self._content[attr])
            count += 1
        return count

    def show_text(self, printCount=0):
        '''打印输出并或仅返回原文字符串。\n
        printcount：shell内打印次数，默认为0'''
        for _ in range(printCount):
            print(self.basic["original_text"])
        return self.basic["original_text"]

    def show_basic_info(self, printCount=0):
        '''不展示原文，打印输出并或仅其他基本信息的字典。\n
        printcount：shell内打印次数，默认为0'''
        display = self.basic.copy()
        del display["original_text"]

        for _ in range(printCount):
            print(display)
        return display

    def new_article(self, title, text, index, author, RSS,
    date=time.strftime("%Y%m%d-%H%M%S", time.localtime()),
    submitter=getuser(), encoding='utf-8'):
        """接收传入的参数，直接保存为新的json文件。\n
        推荐使用全局函数save_article操作"""
        self.basic["encoding"] = encoding
        self.basic["title"] = title
        self.basic["original_text"] = text
        self.basic["index"] = index
        self.basic["author"] = author
        self.basic["date"] = date
        self.basic["submitter"] = submitter
        self.basic["RSS"] = RSS

        #调用分词器，逐个分词并保存到self.content里，准备导出JSON
        splitted_words_generator, id = split_yield(text), 0
        # 拷贝一个分好的词生成器，计数用
        count = split_yield(text)

        # 根据基础模板生成content元素
        try:
            for _ in count:
                self.content.update({str(id):
                {"word":next(splitted_words_generator),
                "bw": 15,
                "Fc": 0,
                "Mw": 0}})
                id+=1
        except (StopIteration):
            print("<Article> Automatic Splitting accomplished.\n")

        if not self.dumpf():
            print("<Article> Article saved succesfully.\n")
            return 0
        else:
            print("<Article> Article not saved.\n")
            return 1


class TestGiver(Article):
    def __init__(self):
        self.Article = None
        self.blocklist = ['and', 'or', 'but', 'the', 'of', 'that', 'when']

    def open_articlef(self, f=''):
        """加载JSON文件配置，如果路径不正确将会打开失败，返回-1；成功则返回加载的数据数量\n
        f: JSON文件的路径，允许使用相对路径"""
        self.Article = Article()
        if os.path.exists(f):
            result = self.Article.loadf(f)

        else:
            print('File doesn`t exist. Failed to load.')
            return -1
        return result

    def new_test(self, difficulty=3):
        '''开始新测试（出一套题）
        每个单词被抽中的可能性由公式决定。
        difficulty: 题目难度，1-10之间的整数；10即为全文默写；
        F(A): 单词A在历次测试中出错的频率，0-1之间；
        M(A): 手动标注的单词A之重要程度，1-2之间；
        B: 每个单词出现的基本概率，默认为15
        P(str is blank) = P( 1D100 < difficulty/length * 200*M(A) *tan(59.42*F(A)) + 2*B*M(A))
        theta = (e/(sqrt(2*pi)))^(-((30*(x-0.5))^2)/2), 如有需要可乘在常数项上，以减小常数项影响'''
        def rank(arg, d=difficulty, B=15):
            """根据公式直接从历史错误次数计算出本词本次被挖空的概率
            arg: str类型，必须是self.Article.content中的键名。"""
            # 确保除数不为零
            if not self.Article.test_info["test_count"] or type(self.Article.content[arg]["Fc"])!=type(1):
                F=0
            else:
                F = self.Article.content[arg]["Fc"]/self.Article.test_info["test_count"]
            # 若难度大于10级或为-1，则要求默写非屏蔽词以外的全文。
            if d == 11 or d == -1:
                return 101
            # 继续引入其他参数开始计算
            deltaM = self.Article.content[arg]["Mw"]
            B =self.Article.content[arg]["bw"]
            length = len(self.Article.content)
            # 按照公式计算并返回
            P = 2000*d/length*(1+deltaM)*math.tan(59.42*F) + 2*B*(1+deltaM)
            return P

        def westoutput(keys_name_and_TF):
            """返回带空格的原文，同时根据阈值情况挖空"""
            result = ''
            for word_index in list(keys_name_and_TF.keys()):
                word = self.Article.content[word_index]["word"]
                if keys_name_and_TF[word_index]:
                    result += '_'* len(word)+' ' # 每个单词有多长，空格就有多长
                else:
                    result += word+' ' #带空格
            return result

        def chioutput(keys_name_and_TF):
            """返回不带空格的原文，同时根据阈值情况挖空"""
            result = ''
            for word_index in list(keys_name_and_TF.keys()):
                word = self.Article.content[word_index]["word"]
                if keys_name_and_TF[word_index]:
                    result += '__'* len(word) # 汉语的下划线比英语长
                else:
                    result += word # 汉语不用带空格
            return result

        def orderedoutput(keys_name_and_TF, mode="west"):
            """返回带空格的原文，同时根据阈值情况挖空"""
            result = ''
            for word_index in list(keys_name_and_TF.keys()):
                word = self.Article.content[word_index]["word"]
                if keys_name_and_TF[word_index]:
                    result += ('___#%s___ ' % word_index)
                else:
                    if mode == "west":
                        result += word+' ' #带空格
                    elif mode == "chi":
                        result += word # 汉语不用带空格
                    else:
                        raise NameError("Argument must be either 'west' or 'chi'.")
            return result

        def ignore(word):
            """检测传入的单词是否被屏蔽。若是，则永远不会被挖空作为题目输出。\n
            返回布尔值，True=未被屏蔽。\n
            屏蔽词列表位于实例属性self.blocklist中。"""
            if word in self.blocklist:
                return False
            return True

        # 先确认有无已打开的文件
        if not self.Article:
            print("尚无已打开的文件！请先使用open_articlef(“文件路径”)打开！")
            return 1
        # 骰nD100，把结果保存
        dices = []
        for _ in range(len(self.Article.content)):
            dices.append(randint(0,100))
        # 建立每个单词与1D100的对应关系，以备检测
        possibility_distributed = {}
        keys_name = list(self.Article.content.keys())
        # keys_name即每个单词的索引的总列表（不是单词本身！单词本身要用self.Article.content[eachword]["word"]访问）
        for each in keys_name:
            possibility_distributed.update({each: dices[keys_name.index(each)]})
        # 准备挖空前，先准备参考答案。参考答案的生成将由比对过程完成
        answer = {}
        # 匹配阈值与1D100的结果，成功则打上挖空标记（True），否则留作原文
        for eachword in possibility_distributed:
            threshold = rank(eachword)
            if possibility_distributed[eachword] < threshold:
            # 在确认挖空前，还需要经ignore函数确认是否在屏蔽列表内。
                possibility_distributed[eachword] = ignore(self.Article.content[eachword]["word"])
                if possibility_distributed[eachword]:
                    answer.update({eachword:self.Article.content[eachword]["word"]}) # 在答案纸里添加答案内容
            else:
                possibility_distributed[eachword] = False
        # 统一使用带序号的模式导出，手动识别文本类型
        if self.Article.basic["text_type"] != "Chinese":
            exam = orderedoutput(possibility_distributed, "west")
        else:
            exam = orderedoutput(possibility_distributed, "chi")
        # 缓存答案信息和题目信息到类对象中
        self.answer = answer
        self.answer_keys = self.answer.keys()
        self.exam = exam
        return {"exam":exam, "answer":answer}

    def correct_test(self, answerSheet, timeTook=None, Comments=None, RecordName=None):
        """批改试卷。接收参数：\n
        answerSheet: 字典，包含各题的原文索引及学生原始答案\n
        timeTook: 字符串，默认为None，测试所消耗时间\n
        Comments: 字符串，默认为None，作答记录中填写的评语\n
        RecordName: 字符串，默认为None，作答记录的名称，推荐留默认"""
        # 使用difflib库进行批改，允许一点点小错误（和不允许也没差多少了）
        correctedPaper, wrongCount, wrongAnswerList = {}, 0, []
        for eachAnswerIndex in answerSheet.keys():
            if difflib.SequenceMatcher(lambda x:x in ' ', # 过滤空格，空格没写全的不扣分；前：学生答案；后：参考答案
            answerSheet[eachAnswerIndex], self.answer[eachAnswerIndex]).ratio() <= 0.6:
                correctedPaper.update({eachAnswerIndex:False}) # 答错的标记False
                wrongCount += 1
                wrongAnswerList.append((eachAnswerIndex, answerSheet[eachAnswerIndex], self.answer[eachAnswerIndex]))
            else:
                correctedPaper.update({eachAnswerIndex:True})
        # 然后登分：
        # 先记录测试成绩
        self.Article.test_info["test_count"] += 1
        self.currentRecord = recordName = time.strftime("%Y%m%d-%H%M%S", time.localtime()) # 记录时间并保存在self.currentRecord中
        self.Article.test_info["test_record"].update({recordName:[
            wrongCount, timeTook, Comments]
            })
        self.testMark = wrongCount/100.0
        # 再记录每个单词错误情况
        for eachAnswer_log in correctedPaper.keys():
            if not correctedPaper[eachAnswer_log]:
                self.Article.content[eachAnswer_log]["Fc"] += 1
        # 最后提交记录名和评语
        # 最终返回错题和正解列表
        return wrongAnswerList

    def log_record(self, recordName=None, Comments=None, RecordName=None):
        if not recordName:
            recordName=self.currentRecord
        else:
            del self.Article.test_info["test_record"][self.currentRecord]
        # self.Article.test_info["test_record"][1] = TimeTook
        self.Article.test_info["test_record"][2] = Comments
        self.Article.dumpf(self.Article._currentFileName)

# 计时器。想了想还是在GUI模块实现比较好
    # class Timer():
    #     """一个计时器类。需要计算做题时长时使用。
    #     来自FishC Python教程的课堂作业，自然是我自己写的实现。
    #     """
    #     def __init__(self):
    #         self.time_b = 0
    #         self.time_e = 0
    #         self.timecost = 0

    #     def __add__(self, other):
    #         _t1 = self.calculate()
    #         _t2 = other.calculate()
    #         _te = [_t1[0] + _t2[0], _t1[1] + _t2[1], _t1[2] + _t2[2], _t1[3] + _t2[3]]
    #         while _te[3] >= 60:
    #             _te[3] -= 60
    #             _te[2] +=1
    #             while _te[2] >= 60:
    #                 _te[2] -= 60
    #                 _te[1] +=1
    #                 while _te[1] >= 24:
    #                     _te[2] -= 24
    #                     _te[1] +=1
    #         print("共计运行了%s天%s小时%s分钟%s秒" % (_te[0], _te[1], _te[2], _te[3]))
    #         return _te

    #     def __repr__(self):
    #         if self.time_b != 0 and self.time_e == 0:
    #             return "请先结束上一轮计时"
    #         else:
    #             self.calculate()
    #             return self.timecost

    #     ##计时器核心组件区
    #     def start(self):
    #         if self.time_b != 0:
    #             print('请先结束上一轮计时')
    #             return None
    #         self.reset(blockmsg=1)
    #         self.time_b = time.time()
    #         print("计时开始")

    #     def stop(self):
    #         if self.time_b == 0:
    #             print('请先开始计时')
    #             return None
            
    #         self.time_e = time.time()
    #         print("计时结束")

    #     def reset(self, blockmsg=0):
    #         self.time_b = 0
    #         self.time_e = 0
    #         self.timecost = 0
    #         if blockmsg == 0:
    #             print("计时器已归零")
                
    #     ##计时器时长计算区
    #     def calculate(self):
    #         day, hour, minute = 0,0,0
    #         second = self.time_e - self.time_b
            
    #         while second >= 60:
    #             second -= 60
    #             minute += 1
    #             while minute >= 60:
    #                     minute -= 60
    #                     hour += 1
    #                     while hour >= 24:
    #                         hour -= 24
    #                         day += 1
    #         self.timecost =  "运行了%s天%s小时%s分钟%s秒" % (day, hour, minute, second)
    #         return [day, hour, minute, second]


def shell_save_article():
    title = 'Utopia'
    index = 0
    author = 'Moore'
    RSS = ''
    encoding = 'utf-8'
    text = '''In heaven, I replied, there is laid up a pattern of it, methinks, which he who desires may behold, and beholding, may set his own house in order. But whether such an one exists, or ever will exist in fact, is no matter; for he will 
live after the manner of that city, having nothing to do with any other.'''''
    a = Article()
    a.new_article(title, text, index, author, RSS, encoding=encoding)
    return 0

def split_list(text):
    """简单调用一下分割器Spliter类分割文本。返回分割后的列表"""
    spliter = Spliter(target_text=text)
    spliter.texts_read()

    splitted_words = spliter.text_output
    return splitted_words

def split_yield(text):
    """类似split_list，但作为迭代器使用。（yielder = split_yield(text); ）"""
    splitted_words = split_list(text)
    for i in splitted_words:
        yield i


# Shell界面下主菜单
def main():
    def shell_start():
        """shell下开始测试"""
        def shell_select_test():
            """选择文件打开
            接收一系列文本格式操作，返回最终选定的文件名（./*.*格式）"""
            cwp = input("当前目录：{}\n请输入文档存放路径（默认为./）：".format(os.getcwd()))
            if not os.path.isdir(cwp):
                print("路径输入错误，请重新输入！")
                return 0
            # 完成路径确认，开始收集目录内信息
            os.chdir(cwp)
            cwp = os.getcwd()

            file_menu_dict = {}
            for index in range(len(os.listdir(cwp))):
                if os.path.isfile(os.listdir(cwp)[index]): # 判断是否为文件。我们不打开文件夹
                    file_menu_dict.update({index: os.listdir(cwp)[index]})
            print("当前目录下文档如下：")
            for file_id in file_menu_dict:
                print("【{}】".format(file_id), '\t',file_menu_dict[file_id])
            # 多次收集信息，尝试打开文件
            while 1:
                file_chosen_id = int(input("请输入需要学习的文档序号："))
                if int(file_chosen_id) not in file_menu_dict.keys():
                    print(" - 序号输入不正确，请检查输入！")
                    continue
                else:
                    print(" - 您当前选择了文件“{}”".format(file_menu_dict[file_chosen_id]))
                    return './'+file_menu_dict[file_chosen_id]

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
            _ = Teacher.new_test(); paper, answer = _['exam'], _['answer']
            print('''------------------------------
            考试说明：请用规范格式作答！如因作答格式不规范导致的无法批改，后果自负！
            作答样例：
            To ___#1___ or not ___#4___ ___#5___, ...
            作答格式（请注意所有标点为英文半角标点，花括号不可省略！）：
            {"1": "be", "4": "to", "5": "be"}\n------------------------------
            ''')
            print(" ==== 测试题 ====\n\n", paper, end='\n\n------------------------------\n\n')
            raw_answer_dict = eval(input(" - 测试开始，请在以下空白区域作答，完成后提交请按回车键！\n"))

            if type(raw_answer_dict) != type({0:0}):
                print(" -  作答格式显然不正确，答题纸解析失败！测试现在结束……")
                return -1

            print("测试结束，您的错误项为：")
            for eachWrong in Teacher.correct_test(raw_answer_dict):
                print("#{}: {} -> {}".format(eachWrong[0], eachWrong[1], eachWrong[2]))

            print("您的得分为：%.1f" % Teacher.testMark)
            Teacher.log_record()
            return 0

        shell_start_test(shell_select_test())
        return 0





    def shell_manage():
        """shell下管理文档（添加、修改原文、修改统计数据、删除等操作）"""
        pass

    def shell_setting():
        """shell下打开设置（默认后缀名）"""
        pass

    def shell_about_and_help():
        """shell下打开帮助（查看文档不就好了吗笨）"""
        pass

    def shell_exit():
        """Shell下退出程序"""
        if input("「真的要退出吗（Y/N）：」").upper() == 'Y':
            exit()
        else:
            return 0

    while(1):
        print("""
        ----[欢迎来到背书辅助器（Shell版）]----
        主菜单：
        【0】开始背诵默写
        【1】管理现有文档
        【2】设置
        【3】关于与帮助
        【E】退出程序
        """)
        menu_func = {'0':'start', '1':'manage', '2':'setting', '3':'about_and_help', 'E':'exit'}
        menu_order = input("> ").capitalize()
        if menu_order in menu_func:
            eval("shell_"+menu_func[menu_order])()
## 测试信息
if __name__ == "__main__":
    main()