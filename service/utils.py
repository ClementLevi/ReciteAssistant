from chardet import detect

__CODE_DETECT_LEN = 200000

# 自动检测编码
def detectCodef(path) -> str:
    """From a text file path refer its possible encoding format.

    Args:
        path (str): selected file.

    Returns:
        str: possible encoding format of the input.
    """
    with open(path, 'rb') as file:
        data = file.read(__CODE_DETECT_LEN)
        dicts = detect(data)
    return dicts["encoding"]


def detectCodes(s) -> str:
    """From a string refer its possible encoding format.

    Args:
        s (str): input string

    Returns:
        str: possible encoding format of the input
    """
    dicts = detect(s.encode())
    return dicts["encoding"]


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

print(detectCodes("你好"))
print(type(detectCodes("你好")))