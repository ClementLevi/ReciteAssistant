import os, time, math, difflib
from getpass import getuser
from jieba import lcut
from string import ascii_lowercase, ascii_uppercase
from random import randint

from Article import *
from Splitter import *
from utils import *
from gui import *
__version = 'v1.0.0'

## 核心算法
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




