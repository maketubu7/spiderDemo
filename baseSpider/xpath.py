#/和//的区别

#//div[@class='cont_sourece']
#结果为【www.ruiwen.com - 汪曾祺】

#//div[@class='cont_sourece']/text()
#获取该元素下文本内容

#//div[@class='cont_sourece']/.
#//div[@class='cont_sourece']/..
#一个点代表选取当前节点，两个点代表选取当前节点的父节点

#//div[@class='info']/span[@class='time']/text()
#结果为时间：2017-11-09,//span[@class='time']/text()

#通过索引获取兄弟节点
#//div[@class='info']/span[1]/a/text()
#结果为汪曾祺

#//link[@rel='dns-prefetch']
#获取所有link标签，属性为rel='dns-prefetch']

#模糊查询，获取所有包含content属性的div节点
#//div[contains(@class,"content")]
#取反
#//div[not(contains(@class,"content"))]

#last函数
#//div[@class='content']/p[last()-13]
#结果为萧胜一边流着一串一串的眼泪，一边吃黄油烙饼。他的眼泪流进了嘴里。黄油烙饼是甜的，眼泪是咸的。

#position函数
#//div[@class='content']/p[position()>61]
#获取p节点大于61的p节点

#通过竖线分隔
#//span[@class='source']/a/text()|//span[@class='time']/text()
#那么如果左右两侧的xpath语句都有结果，则都显示，否则，如果左侧没有结果，则判断右侧，如果右侧也没有，则显示为空


