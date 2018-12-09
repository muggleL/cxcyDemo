"""
爬取 caixin.com 的文章
输入：文章链接
返回：文章内容 集
"""

import requests
import re

 
HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}

class Caixin_spider:

    ## 错误日志
    def __log(self, content):
        log = open('error_log.txt', 'a+', encoding='utf-8')
        log.writelines(content)
        log.close()

    ##获取链接 html
    def __getPage(self, url):
        self.url = url
        response = requests.get(self.url, headers=HEADERS)
        response.encoding = 'utf-8'
        return response.text

    ##获取 标题 日期 和 文章评论？
    def __getTitle(self, html):
        title = ''
        time = ''
        subhead = ''
        try: # 文章的 html 有两种形式 所以 这里区分一下 
            re_title = re.compile(r'<div id="conTit">.*?<h1>(.*?)<em class="icon_key"></em>.*?</h1>.*?id="pubtime_baidu">(.*?)</span>', re.S)
            content = re.findall(re_title, html) # 包含信息的代码块
            title = content[0][0].replace(' ', '').replace('\r\n', '').replace('\n', '') # 标题 去除多余符号
            time = content[0][1].replace('\n', '')  # 文章发布时间
        except:
            try:
                re_title = re.compile(
                    r'<div id="conTit">.*?<h1>(.*?)</h1>.*?id="pubtime_baidu">(.*?)</span>',
                    re.S)
                content = re.findall(re_title, html)
                title = content[0][0].replace(' ', '').replace('\r\n', '').replace('\n', '')
                time = content[0][1].replace('\n', '')
            except: ## 将不符合上面两种形式的文章链接写入 log 文件
                text = "这篇文章不符合要求，文章链接：" + self.url
                print(text)
                self.__log(text + '\n')
        if "招商银行" in title or "招商" in title or "招行" in title: ## 标题里有关键字的文章， 一定是我们需要的文章 这可能会有遗漏， 不过暂时没有什么方法。
            try:
                re_titlecomment = re.compile(r'<div id="subhead" class="subhead">(.*?)</div>', re.S)
                titlecomment = re.findall(re_titlecomment, html)
                subhead = titlecomment[0].replace(' ', '').replace('\r\n', '').replace('\n', '')
                # print(subhead)
            except:
                pass
        else: return
        return (time, title, subhead)

    ## 获取 正文 由于权限问题 只能获取到很小的一部分内容
    def __getContent(self, html):
        re_content = re.compile(r'<div id="Main_Content_Val" class="text">(.*?)<a href=',re.S)
        content = re.findall(re_content,html)[0]
        del_href = re.compile(r'<A href=".*?" target="_blank">',re.S) # 删除文章内部链接
        del_note = re.compile(r'<!.*?>', re.S) # 不记得 note 是什么鬼了
        del_tag = re.compile(r'</div.*看', re.S) # 删除文章末尾的代码
        del_title= re.compile(r'【财新网】（记者.*?）', re.S) # 删除文章前的固定标题 记者等信息
        content = re.sub(del_href," ",content)
        content = re.sub(del_note, " ", content)
        content = re.sub(del_tag, " ", content)
        content = re.sub(del_title, " ", content)
        content = content.replace('<P>','').replace('</P>','').replace('<B>','').replace('</B>','').replace('</A>','')
        content = re.sub(r'\s','',content) 
        return content


    def get(self, urls):
        for url in urls:
            html = self.__getPage(url)
            title = self.__getTitle(html)
            if(title): # 这个链接包含关键字 才获取这篇文章的信息， 否则 放过
                time, title, subhead = title
                content = self.__getContent(html)
                yield time + " " + title + "  " + subhead + "\t" + content + "\n"


if __name__ == '__main__':
    from baidu_advance import Baidu_advance  # just for test
    test = Caixin_spider()
    baidu = Baidu_advance()
    urls = baidu.getUrl('finance.caixin.com', 20, '招商银行')
    contents = test.get(urls)
    f = open('caixin_baidu_test.txt', 'a+', encoding='utf-8')
    for i in contents:
        f.write(i)
    f.close()
