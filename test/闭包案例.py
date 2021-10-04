Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 16:33:24) [MSC v.1928 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import tkinter as tk
>>> class a():
	def __init__(self):
		root = tk.Tk()
		label = tk.Label(root, text="Text")
		button = tk.Button(root, text='click', command=label.destroy)
		label.pack()
		button.pack()
		root.mainloop()

		
>>> a()
<__main__.a object at 0x0319D5B0>
>>> class a():
	def __init__(self):
		root = tk.Tk()
		label = tk.Label(root, text="Text")
		button = tk.Button(root, text='click', command=label.forget)
		label.pack()
		button.pack()
		root.mainloop()

		
>>> a()
<__main__.a object at 0x0362AF70>
>>> class a():
	def __init__(self):
		def switch():
			if self.t=0:
				label.forget()
				self.t=1
			else:
				label.pack()
				self.t=0
		self.t=0
		root = tk.Tk()
		label = tk.Label(root, text="Text")
		button = tk.Button(root, text='click', command=switch)
		label.pack()
		button.pack()
		root.mainloop()
		
SyntaxError: invalid syntax
>>> 
>>> class a():
	def __init__(self):
		def switch():
			if self.t==0:
				label.forget()
				self.t=1
			else:
				label.pack()
				self.t=0
		self.t=0
		root = tk.Tk()
		label = tk.Label(root, text="Text")
		button = tk.Button(root, text='click', command=switch)
		label.pack()
		button.pack()
		root.mainloop()

		
>>> a()
<__main__.a object at 0x0319D5B0>
>>> class a():
	def __init__(self):
		def switch():
			if self.t==0:
				label.forget()
				self.t=1
			else:
				label.pack()
				self.t=0
		self.t=0
		root = tk.Tk()
		frame=tk.Frame(root, bd=2, relief=tk.GROOVE)
		label = tk.Label(frame, text="Text")
		button = tk.Button(root, text='click', command=switch)
		frame.pack()
		label.pack()
		button.pack()
		root.mainloop()

		
>>> a()
<__main__.a object at 0x0362AF58>
>>> import time
>>> time.localtime()
time.struct_time(tm_year=2021, tm_mon=4, tm_mday=13, tm_hour=21, tm_min=10, tm_sec=34, tm_wday=1, tm_yday=103, tm_isdst=0)
>>> dir(time.localtime())
['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index', 'n_fields', 'n_sequence_fields', 'n_unnamed_fields', 'tm_gmtoff', 'tm_hour', 'tm_isdst', 'tm_mday', 'tm_min', 'tm_mon', 'tm_sec', 'tm_wday', 'tm_yday', 'tm_year', 'tm_zone']
>>> type(time.localtime())
<class 'time.struct_time'>
>>> time.time()
1618319473.5054371
>>> class TimerSimple():
    def __init__(self):
        self.time_start = None
        self.time_stop = None
        self.standby = None

    def ticktock(self):
        if self.standby == None:
            self.standby = False
            self.time_start = time.time()
        elif self.standby == False:
            self.standby = True
            self.time_stop = time.time()
            return self.time_stop - self.time_start
        else:
            self.standby = None
            self.time_stop = None
            self.standby = None
            return 0

        
>>> t = TimerSimple()
>>> t.ticktock()
>>> t.ticktock()
1.9616291522979736
>>> t.ticktock()
0
>>> t.ticktock()
>>> t.ticktock()
6.927323818206787
>>> t.ticktock()
0
>>> t.ticktock()
>>> b = t.ticktock()
>>> b
8.472495555877686
>>> type(b)
<class 'float'>
>>> b = t.ticktock()
>>> b = t.ticktock()
>>> b = t.ticktock()
>>> b = t.ticktock()
>>> b = t.ticktock()
>>> b
>>> b
>>> b
>>> b
>>> b
>>> b
>>> b
>>> t.ticktock()
11.518887042999268
>>> t.ticktock()
0
>>> int(3.123)
3
>>> int(3.623)
3
>>> int(3.9923)
3
>>> 24//3
8
>>> 24//9
2
>>> 24%9
6
>>>     def format(x):
        clock = {'h':0, 'm':0, 's':0}
        clock['h'] = x//3600
        clock['m'] = x//60
        clock['s'] = x%60
        
SyntaxError: unexpected indent
>>> def format(x):
        clock = {'h':0, 'm':0, 's':0}
        clock['h'] = x//3600
        clock['m'] = x//60
        clock['s'] = x%60
        print(clock)

        
>>> format(61)
{'h': 0, 'm': 1, 's': 1}
>>> format(661)
{'h': 0, 'm': 11, 's': 1}
>>> 10//0.001
9999.0
>>> 10/0.001
10000.0
>>> 3.111111/0.001
3111.1110000000003
>>> def format(x):
        sec = int(x)
        ms = int(x*1000)/1000 - sec
        clock = {'h':0, 'm':0, 's':0, 'ms':0}
        clock['h'] = sec//3600
        clock['m'] = sec//60
        clock['s'] = sec%60
        clock['ms']= ms
        return clock

>>> format(300)
{'h': 0, 'm': 5, 's': 0, 'ms': 0.0}
>>> format(300.001)
{'h': 0, 'm': 5, 's': 0, 'ms': 0.0009999999999763531}
>>> def format(x):
        sec = int(x)
        ms = int(int(x*1000)/1000 - sec)
        clock = {'h':0, 'm':0, 's':0, 'ms':0}
        clock['h'] = sec//3600
        clock['m'] = sec//60
        clock['s'] = sec%60
        clock['ms']= ms
        return clock

>>> format(300.001)
{'h': 0, 'm': 5, 's': 0, 'ms': 0}
>>> int(int(0.001*1000)/1000 - sec)
Traceback (most recent call last):
  File "<pyshell#76>", line 1, in <module>
    int(int(0.001*1000)/1000 - sec)
NameError: name 'sec' is not defined
>>> int(int(0.001*1000)/1000)
0
>>> 0.001*1000
1.0
>>> 1.0/1000
0.001
>>> 1.001*1000
1000.9999999999999
>>> sec = 1989.986479
>>> ms = int((sec- int(sec))*1000)

>>> ms
986
>>> class TimerSimple():
    def __init__(self):
        self.time_start = None
        self.time_stop = None
        self.standby = None
        self.timerecord = None

    def ticktock(self):
        if self.standby == None:
            self.standby = False
            self.time_start = time.time()
        elif self.standby == False:
            self.standby = True
            self.time_stop = time.time()
            self.timerecord = self.time_stop - self.time_start
            return self.format()
        else:
            self.standby = None
            self.time_stop = None
            self.standby = None
            self.timerecord = None
            return 0

    def format(self):
        sec = int(self.timerecord)
        ms = int((self.timerecord- sec)*1000)
        clock = {'h':0, 'm':0, 's':0, 'ms':0}
        clock['h'] = sec//3600
        clock['m'] = sec//60
        clock['s'] = sec%60
        clock['ms']= ms
        return clock

>>> a = TimerSimple()
>>> a.ticktock()
>>> a.ticktock()
{'h': 0, 'm': 0, 's': 1, 'ms': 910}
>>> a.ticktock()
0
>>> a.ticktock()
>>> a.ticktock()
{'h': 0, 'm': 0, 's': 3, 'ms': 883}
>>> a.ticktock()
0
>>> b = a.ticktock()
>>> c = a.ticktock()
>>> id(b); id(c)
2039760220
56951104
>>> b
>>> b
>>> b
>>> b()
Traceback (most recent call last):
  File "<pyshell#99>", line 1, in <module>
    b()
TypeError: 'NoneType' object is not callable
>>> b = a.ticktock()
>>> b = a.ticktock()
>>> b = a.ticktock()
>>> b = a.ticktock(); id(b)
9465968
>>> b = a.ticktock(); id(b)
2039760220
>>> b = a.ticktock(); id(b)
51944016
>>> b = a.ticktock(); id(b)
9465968
>>> b = a.ticktock(); id(b)
2039760220
>>> b = a.ticktock(); id(b)
8932520
>>> b = a.ticktock(); id(b)
9465968
>>> b = a.ticktock(); id(b)
2039760220
>>> b = a.ticktock(); id(b)
56868488
>>> b = a.ticktock(); id(b)
9465968
>>> def a(x):
	def b(x):
		x +=1
		print(x)
	b(x)

	
>>> a(0)
1
>>> a(0)
1
>>> a(0)
1
>>> def a():
	def b(x):
		x +=1
		return x
	return b

>>> a(2)
Traceback (most recent call last):
  File "<pyshell#126>", line 1, in <module>
    a(2)
TypeError: a() takes 0 positional arguments but 1 was given
>>> c=a()
>>> c(2)
3
>>> c(2)
3
>>> 
>>> def a():
	l = []
	def b(x):
		l.append(x)
		return l
	return b

>>> c=a()
>>> c(1)
[1]
>>> c(1)
[1, 1]
>>> c(1)
[1, 1, 1]
>>> c(1)
[1, 1, 1, 1]
>>> c(1)
[1, 1, 1, 1, 1]
>>> c(1)
[1, 1, 1, 1, 1, 1]
>>> c(1)
[1, 1, 1, 1, 1, 1, 1]
>>> class A():
	def __init__(self):
		self.a = self.b()
	def b(self):
		l = []
		def c(x):
			l.append(x)
			return l
		return c

	
>>> d = A()
>>> d.a(1)
[1]
>>> d.a(1)
[1, 1]
>>> 
>>> d.a(1)
[1, 1, 1]
>>> d.a(1)
[1, 1, 1, 1]
>>> d.a(1)
[1, 1, 1, 1, 1]
>>> class TimerSimple():
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
        ms = int((self.timerecord- sec)*1000)
        clock = {'h':0, 'm':0, 's':0, 'ms':0}
        clock['h'] = sec//3600
        clock['m'] = sec//60
        clock['s'] = sec%60
        clock['ms']= ms
        return clock
    
    def format_ticktock(self):
        try:
            d = self._ticktock
            return str(d['h']).ljust(2,'0')+":"+str(d['m']).ljust(2,'0')+":"+str(d['s']).ljust(2,'0')+":"+str(d['ms']).ljust(3,'0')
        except:
            return None

        
>>> a = TimerSimple()
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> class TimerSimple():
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
        def temp(x):
            return x
        try:
            d = temp(self._ticktock)
            return str(d['h']).ljust(2,'0')+":"+str(d['m']).ljust(2,'0')+":"+str(d['s']).ljust(2,'0')+":"+str(d['ms']).ljust(3,'0')
        except:
            return None

        
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> a.format_ticktock()
>>> class A():
	def __init__(self):
		self.l=[]
	def a():
		def outer():
			def inner(self):
				self.l.append(1)
				return self.l
			return inner
		temp = outer()
		return temp

	
>>> b = A()
>>> b.a()
Traceback (most recent call last):
  File "<pyshell#183>", line 1, in <module>
    b.a()
TypeError: a() takes 0 positional arguments but 1 was given
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(self):
				self.l.append(1)
				return self.l
			return inner
		temp = outer()
		return temp

	
>>> b = A()
>>> b.a()
<function A.a.<locals>.outer.<locals>.inner at 0x0088A4A8>
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(self, x):
				self.l.append(x)
				return self.l
			return inner
		temp = outer()
		temp(1)
		return temp

	
>>> b = A()
>>> b.a()
Traceback (most recent call last):
  File "<pyshell#191>", line 1, in <module>
    b.a()
  File "<pyshell#189>", line 11, in a
    temp(1)
TypeError: inner() missing 1 required positional argument: 'x'
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(x):
				self.l.append(x)
				return self.l
			return inner
		temp = outer()
		temp(1)
		return temp

	
>>> b = A()
>>> b.a()
<function A.a.<locals>.outer.<locals>.inner at 0x0088A6E8>
>>> b.a()()
Traceback (most recent call last):
  File "<pyshell#196>", line 1, in <module>
    b.a()()
TypeError: inner() missing 1 required positional argument: 'x'
>>> b.a()(1)
[1, 1, 1, 1]
>>> b.a()(1)
[1, 1, 1, 1, 1, 1]
>>> del b
>>> b = A()
>>> b.a()
<function A.a.<locals>.outer.<locals>.inner at 0x0088A6E8>
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(x):
				self.l.append(x)
				return self.l
			return inner
		temp = outer()
		return temp(1)

	
>>> b = A()
>>> b.a()
[1]
>>> b.a()
[1, 1]
>>> b.a()
[1, 1, 1]
>>> b.a()
[1, 1, 1, 1]
>>> b.a()
[1, 1, 1, 1, 1]
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(x):
				self.l.append(x)
				return self.l
			return inner
		temp = outer()
		return str(temp(1))

	
>>> b = A()
>>> b.a()
'[1]'
>>> b.a()
'[1, 1]'
>>> b.a()
'[1, 1, 1]'
>>> b.a()
'[1, 1, 1, 1]'
>>> b.a()
'[1, 1, 1, 1, 1]'
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(x):
				self.l.append(x)
				if len(self.l)==3:
					print(self.l, '!')
				return None
			return inner
		temp = outer()
		return str(temp(1))

	
>>> b = A()
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
[1, 1, 1] !
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> class A():
	def __init__(self):
		self.l=[]
	def a(self):
		def outer():
			def inner(x):
				self.l.append(x)
				if len(self.l)==3:
					print(self.l, '!')
				return None
			return inner
		temp = outer()
		return str(temp(1))

	
>>> class A():
	def a(self):
		def outer():
			l=[]
			def inner(x):
				l.append(x)
				if len(self.l)==3:
					print(self.l, '!')
				return None
			return inner
		temp = outer()
		return str(temp(1))

	
>>> b=A()
>>> b.a()
Traceback (most recent call last):
  File "<pyshell#236>", line 1, in <module>
    b.a()
  File "<pyshell#234>", line 12, in a
    return str(temp(1))
  File "<pyshell#234>", line 7, in inner
    if len(self.l)==3:
AttributeError: 'A' object has no attribute 'l'
>>> class A():
	def a(self):
		def outer():
			l=[]
			def inner(x):
				l.append(x)
				if len(l)==3:
					print(l, '!')
				return None
			return inner
		temp = outer()
		return str(temp(1))

	
>>> b.a()
Traceback (most recent call last):
  File "<pyshell#239>", line 1, in <module>
    b.a()
  File "<pyshell#234>", line 12, in a
    return str(temp(1))
  File "<pyshell#234>", line 7, in inner
    if len(self.l)==3:
AttributeError: 'A' object has no attribute 'l'
>>> b=A()
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> b.a()
'None'
>>> 