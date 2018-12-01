'''
通过链接爬取财新网的内容
'''

import requests
import re

 
HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}

class CaixinSpider:

    def __log(self, content):
        log = open('error_log.txt', 'a+')
        log.writelines(content)
        log.close()

    def __getPage(self, url):
        self.url = url
        response = requests.get(self.url, headers=HEADERS)
        response.encoding = 'utf-8'
        return response.text

    def __getTitle(self, html):
        title = ''
        time = ''
        subhead = ''
        try:
            re_title = re.compile(r'<div id="conTit">.*?<h1>(.*?)<em class="icon_key"></em>.*?</h1>.*?id="pubtime_baidu">(.*?)</span>', re.S)
            content = re.findall(re_title, html)
            title = content[0][0].replace(' ', '').replace('\r\n', '').replace('\n', '')
            time = content[0][1].replace('\n', '')
        except:
            try:
                re_title = re.compile(
                    r'<div id="conTit">.*?<h1>(.*?)</h1>.*?id="pubtime_baidu">(.*?)</span>',
                    re.S)
                content = re.findall(re_title, html)
                title = content[0][0].replace(' ', '').replace('\r\n', '').replace('\n', '')
                time = content[0][1].replace('\n', '')
            except:
                text = "这篇文章不符合要求，文章链接：" + self.url
                print(text)
                self.__log(text + '\n')
        if "招商银行" in title or "招商" in title or "招行" in title:
            try:
                re_titlecomment = re.compile(r'<div id="subhead" class="subhead">(.*?)</div>', re.S)
                titlecomment = re.findall(re_titlecomment, html)
                subhead = titlecomment[0].replace(' ', '').replace('\r\n', '').replace('\n', '')
                # print(subhead)
                self.related = True
            except:
                pass
        else: return
        return (time, title, subhead)

    def __getContent(self, html):
        re_content = re.compile(r'<div id="Main_Content_Val" class="text">(.*?)<a href=',re.S)
        content = re.findall(re_content,html)[0]
        del_href = re.compile(r'<A href=".*?" target="_blank">',re.S)
        del_note = re.compile(r'<!.*?>', re.S)
        del_tag = re.compile(r'</div.*看', re.S)
        del_title= re.compile(r'【财新网】（记者.*?）', re.S)
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
            if(title):
                time, title, subhead = title
                content = self.__getContent(html)
                yield time + " " + title + "  " + subhead + "\t" + content + "\n"


if __name__ == '__main__':
    from baidu_advance import Baidu_advance  # just for test
    test = CaixinSpider()
    baidu = Baidu_advance()
    urls = baidu.getUrl('finance.caixin.com', 20, '招商银行')
    contents = test.get(urls)
    f = open('caixin_baidu_test.txt', 'a+')
    for i in contents:
        f.write(i)
    f.close()
