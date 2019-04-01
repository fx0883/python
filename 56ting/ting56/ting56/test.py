import execjs
import re

# 执行本地的js

# def getjs():
# #     f = open("./js/main.js", 'r', encoding='UTF-8')
# #     line = f.readline()
# #     htmlstr = ''
# #     while line:
# #         htmlstr = htmlstr + line
# #         line = f.readline()
# #     return htmlstr
# #
# #
# # def getParam(strSource):
# #     ctx = None
# #     if ctx == None:
# #         jsstr = getjs()
# #         ctx = execjs.compile(jsstr)
# #     return ctx.call('getParam', strSource)
# #
# #
# #
# # print(getParam('*121*111*117*115*104*101*110*103*47*50*51*51*56*54*47*50*38*49*51*49*50*38*116*99'))


def getChapterName(strSource):
    retlist = re.findall("2166-0-(.*?).html",strSource)
    return retlist[0]
    # pass

print(getChapterName("http://www.ting56.com/video/2166-0-3.html"))
