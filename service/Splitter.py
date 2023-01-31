import os
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