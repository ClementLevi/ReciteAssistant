import json

from Splitter import split_yield

class Article:
    """_summary_: 文章数据结构与文章的读写方法
    """
        # 包括了常用的大部分中英德文标点符号
    _PUNCTUATIONS = r''' ~,.?!&"'\\()-_+*/=@#<>:;%$[]{}|`^·！￥……（）——【】、；：‘’“”，。《》？„‚‘“`´°§'''
    _ILLEGAL_CHAR = r'''\/*?:"<>|'''

    def __init__(self, title='NewArticle'):
        """根据模板，生成一个新文档，准备接受写入的数据。\n
        self.__IGNORED_ATTRS__是被保护的变量名容器，不参与算法，只用于JSON模块操作。在其中的所有属性名都不会被导出到JSON中。\n
        JSON导出实例对象属性的方法见dumps和dumpf方法。"""
        ## 受保护的实例属性
        self._content = {} # 保护的变量容器，用于JSON导出
        self._currentFileName = '' # 当前打开文件。保存时会被dumpf()使用
        self.answer = [] # 从TestGiver类中赋值。每次新建题目都会有所不同，故特此设计
        self.__IGNORED_ATTRS__ = ["_content", "_currentFileName", "answer", "__IGNORED_ATTRS__"]  # 需要保护的变量名请写在这里

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
            if attr not in self.__IGNORED_ATTRS__:
                self._content.update({attr: self.__dict__[attr]})
        if not file_name: # 无自定义文件名或路径时，默认存放在本目录下
            file_name = self.basic['title']+'-'+str(self.basic['index'])+'-'+self.basic['author']+'-'+self.basic['date']
                # 文件名默认为标题+索引+作者+日期，需注意不应含有非法字符
        # 无论有无自定义文件名，都进行筛查并保存
        for i in file_name:
            if i in self._ILLEGAL_CHAR:
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
        printCount：shell内打印次数，默认为0'''
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