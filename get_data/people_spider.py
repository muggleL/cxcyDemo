"""人民网金融新闻爬虫"""
import requests
import re
import time

HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}
class People_spider:
    def __init__(self, keys):
        '''文章相关度， 用 逗号隔开‘'''
        self.key = keys.split('、')

    def __getPage(self, url):
        """通过url 获取页面html"""
        print(url)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
        except requests.exceptions.ReadTimeout:
            print("time out")
            time.sleep(10)
            response = requests.get(url, headers=HEADERS, timeout=10)

        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        else:
            print("bad request!")
            exit(1)

    def __getTitle(self, content): #标题 时间
        try:
            re_title = re.compile('<h3 class="pre">(.*?)</h3>.*?<h1>(.*?)</h1>.*?<h4 class="sub">(.*?)</h4>', re.S)
            re_date = re.compile('<div class="fl">(.*?)</div>', re.S)
            del_blank = re.compile('&nbsp;.*', re.S)
            title = re.findall(re_title, content)
            title = title[0][0]+title[0][1]+title[0][2]
            title = title.replace('&nbsp;', '').replace('——', '') #前标题 主标题 副标题组成标题
            date = re.findall(re_date, content)[1]
            date = re.sub(del_blank, '', date).replace('年', '-').replace('月', '-').replace('日', ' ') #统一日期格式
        except:
            return
        for i in self.key:
            if i in title:
                return title, date
        return

    def __getContent(self, html):
        # re_content = re.compile('<p style="text-indent: 2em;">(.*)<p style="text-indent: 2em;">', re.S)
        re_content = re.compile('<div class="box_pic"></div>(.*?)<div class="box_pic">', re.S)
        content =re.findall(re_content, html)[0]
        del_1 = re.compile('<div.*/.*>', re.S)
        del_2 = re.compile('<span.*?</span>', re.S)
        content = re.sub(del_1, "", content)
        content = re.sub(del_2, "", content)
        content = content.replace('<p style="text-indent: 2em;">', '').replace('<p>', '').replace('</p>', '')\
            .replace('\r\n', '').replace('\n', '').replace(' ', '').replace('\t', '').replace('\u3000', '')\
            .replace('&nbsp;', '').replace('<strong>', '').replace('</strong>', '').replace('<br/>', '')
        return content

    def get(self, urls):
        for url in urls:
            content = self.__getPage(url)
            req = self.__getTitle(content)
            if(req):
                content = self.__getContent(content)
                print(url)
                title, date = req
                print(title)
                print(date)
                print(date + " " + title + "  " + "\t" + content + "\n")
                yield date + " " + title + "  " + "\t" + content + "\n"

if __name__ == '__main__':
    from baidu_advance import Baidu_advance
    urls = Baidu_advance().getUrl('finance.people.com.cn', 1, '招行')
    contents = People_spider('招行、招商银行、招商').get(urls)
    f = open('people_baidu_test2.txt', 'w+', encoding='utf-8')
    for i in contents:
        f.write(i)
    f.close()