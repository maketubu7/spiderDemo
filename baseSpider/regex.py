import re
string = 'python45 | java123 | c#34 | c++76 | scala123 | ruby234 | R324'

'''
普通字符集 及 元字符 \d \D 
'''
res1 = re.findall('python',string)   #返回的为一个列表，因为匹配到的结果可能不止一个
print(res1)  

res2 = re.findall('js',string)
if len(res2) > 0:
    print(res2)
else:
    print('None')

res3 = re.findall('\d',string)   #匹配所有的数字
print(res3)

res4 = re.findall('\D',string)   #匹配所有的非数字
print(res4)

string2 = 'abc afc acc abg acg asc'

res5 = re.findall('a[cf]c', string2)  #字符加模式匹配  可以控制具体值
print(res5)

res6 = re.findall('a[^cf]c',string2)  #字符加模式取反  可以筛选具体值
print(res6)

res7 = re.findall('a[a-r]c', string2)  #字符加范围匹配  可以控制值的范围
print(res7)

'''
概括字符集 [0-9],[^0-9],\w=[A-Za-z0-9](字符和数字 不包含特殊字符)，\W(非单词字符，特殊字符,空白字符)，
\s(空白字符)，\S(非空白字符)，.除换行符\n外的所有字符
'''
string3 = 'asdas&% \n\tasd123*'
res = re.findall('\w',string3)
print(res)

res = re.findall('\W',string3)
print(res)



res = re.findall('\s',string3)
print(res)

res = re.findall('\S',string3)
print(res)

'''
数量词的表示 {n}, {m,n}, *(0次或多次)，+(一次或多次),?(0次或一次)
'''

string4 = 'java 234 php34 scala2394 my123'
res = re.findall('[a-z]{2,5}',string4)
print(res)

'''
贪婪与非贪婪 ？非贪婪
'''
res = re.findall('[a-z]{2,5}?',string4)
print(res)

'''
边界匹配 ^表示开头  $表示结尾
'''
qq = '256548788'

res = re.findall('^\d{4,8}$',qq)
print(res)

res = re.findall('^\d{4,9}$',qq)
print(res)

'''
组  （）括号里面的内容是且的关系 []中括号里的内容是或的关系
'''

string6 = 'pythonpythonpythonpythonpythonpythonpythonpython'

res = re.findall('(python){3}',string6)     #返回的是匹配多个的次数有几次的个数的组  ['python'，'python']
print(res)

'''
匹配模式参数   re.I 忽略大小写进行匹配  re.S 给与点.匹配所有字符的特权
'''
language = 'pythonC#\njava'

res = re.findall('c#.{1}',language, re.I | re.S)   # res ['C#\n']
print(res)

'''
re.sub('reg','repl',string,count = 0)
'''

string5 = 'javac#pythonc#scalac#java'

res = re.sub('c#','make',string5,0)  #若count参数为0   则会替换所有匹配到的元素
print(res)


def convert(data):   #传入的函数，匹配到几次， 就执行几次， 传入的data是一个对象，  data.group()方法，返回其匹配到的值
    print(data)    #<_sre.SRE_Match object; span=(4, 6), match='c#'>
    matched = data.group()
    return '^-^' + matched + '^-^'   #返回的值，就像相当于传入的repl 即替换的字符串

res = re.sub('c#',convert,string5,1)   # count=1即代表  只匹配到一次即停止匹配  res java^-^c#^-^pythonc#scalac#java
print(res)


s = 'asd45sd7sd2d0df45l213y'

def conver(data):
    matched = int(data.group())

    if matched > 50:
        return '9'
    else:
        return '0'

res = re.sub('\d{2}',conver,s)    #sub  传入函数的示例

print(res)

'''
re.match 从第一个位置开始匹配，匹配不到则返回None,若匹配到直接返回当前结果的序列化对象,用group()方法得到具体的值，用span()得到索引的位置
re.sereach 匹配到一个就停止匹配，并直接返回当前结果的序列化对象,用group()方法得到具体的值，用span()得到索引的位置
re.findall 匹配到所有的值，并返回匹配到的实际的字符串而不是序列化的对象
'''

s1 = 'a231231'
s2 = '12312'
r1 = re.match('\d',s1)
print(r1)    # r1  None

r2 = re.search('\d',s1)
print(r2)    # r2  <_sre.SRE_Match object; span=(1, 2), match='2'>

r1 = re.match('\d',s2)
print(r1)    # r1  None

r2 = re.search('\d',s2)
print(r2)    # r2  <_sre.SRE_Match object; span=(1, 2), match='2'>

'''
group的使用
'''

s = 'life is short, i use python, i use scala aslo '

res = re.search('life(.*)python(.*)aslo', s)

print(res.group())    #group() group(0)  都是返回完整结果
print(res.group(1))   #group(1) 返回表达式里的第一个组即第一个()里的值
print(res.group(2))   #group(2) 返回第二个组
print(res.group(0,1,2))  #返回由每个结果组成的元组   ('life is short, i use python, i use scala aslo', ' is short, i use ', ', i use scala ')
print(res.groups())    #返回每个组的返回值 组成的元组    (' is short, i use ', ', i use scala ')

