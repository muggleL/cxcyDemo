import requests
import re
import time

HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}

class Sina_spider:
    def __getPage(self, url):
        """通过url 获取页面html"""
        print(url)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
        except requests.exceptions.ReadTimeout:
            print("time out")
            time.sleep(10)
            response = requests.get(url, headers=HEADERS, timeout=10)

        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            print("bad request!")
            exit(1)

    def __getTitleAndTime(self, content):
        """获取时间和日期"""
        try:
            re_title = re.compile('<h1 class="main-title">(.*?)</h1>', re.S)
            re_time = re.compile('<span class="date">(.*?)</span>')
            title = re.findall(re_title, content)[0]
            c_time = re.findall(re_time, content)[0].replace("年", '-').replace('月', '-').replace('日', '')
        except:
            pass
            return
        if "招商银行" in title or "招商" in title or "招行" in title:
            return (title, c_time)
        else:
            return

    def __getContent(self, html):
        """获取正文"""
        # re_content = re.compile('<div class="article" id="artibody">(.*?)<p class="article-editor">', re.S)
        re_content = re.compile('<div class="article" id="artibody">(.*?)<!-- 编辑姓名及工作代码 -->', re.S)
        content = re.findall(re_content, html)[0].replace('\r\n','').replace('\n','').replace('\t','').replace(' ','')
        if '视频加载中' in content: #排除视频
            return
        del_ad = re.compile(r'<!--article_adlist.*?article_adlist-->', re.S)
        del_note = re.compile(r'<!.*?>', re.S)
        del_head = re.compile(r'<p>\u3000\u3000<spanstyle=.*class="img_wrapper".*?</div>', re.S)
        del_tag = re.compile(r'<.*?>', re.S)
        del_mz = re.compile(r'免责声明.*', re.S)
        del_ed = re.compile('。■ 作者.*', re.S)
        content = re.sub(del_ad, "", content)
        content = re.sub(del_note, "", content)
        content = re.sub(del_head, "", content)
        content = content.replace("<p>", "").replace('\u3000', '').replace('</p>', '').replace('&#x3000;','')
        content = re.sub(del_tag, "", content)
        content = re.sub(del_mz, "", content)
        content = re.sub(del_ed, "。", content)
        return content

    def get(self, urls):
        for url in urls:
            content = self.__getPage(url)
            req = self.__getTitleAndTime(content)
            if(req):
                content = self.__getContent(content)
                if content:
                    print(url)
                    title, c_time = req
                    # print(c_time + " " + title + "  " + "\t" + content + "\n")
                    yield c_time + " " + title + "  " + "\t" + content + "\n"
            time.sleep(1)


if __name__ == '__main__':
    from baidu_advance import Baidu_advance
    urls = Baidu_advance().getUrl('finance.sina.com.cn', 10, '招行')
    contents = Sina_spider().get(urls)
    f = open('sina_baidu_test2.txt', 'a+', encoding='utf-8')
    for i in contents:
        f.write(i)
    f.close()