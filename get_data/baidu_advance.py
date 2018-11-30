"""

GetUrlInEachPage 通过百度搜索 搜索 一年以内 特定的网站 特定的关键词
输入：网站 需要获取的页数 关键词
返回：包含所有新闻链接的 list

get = GetUrlInEachPage('baidu.com', 10, '测试')
theUrl = get.getUrl

theUrl 即包含了所有一年以内 的 baidu.com 上 以 ‘测试’ 为关键字 的通过百度搜索到的前10页所有的条目链接
"""
import requests
from bs4 import BeautifulSoup


BAESE_URL = 'https://www.baidu.com'
HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}


class Baidu_advance:

    def __advanceSearch(self, site, keyWords=''):
        """
        构造百度高级搜索 输入 获取的网站和 关键词 返回结果链接
        """
        newsite = 'site%3A' + site.replace(' ', '') + '%20' + keyWords.replace(" ", '')
        url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' + newsite + '&oq='+ newsite + '&rsv_pq=faa075c70000d63a&rsv_t=1075iVsqlnDuVvD6gxOn2pbo4kPcmeJZgby%2BTcynBvPl%2Fvpim8afseEQdzc&rqlang=cn&rsv_enter=1&gpc=stf%3D1511922778%2C1543458778%7Cstftype%3D1&tfflag=1&si=' + site + '&ct=2097152'
        #print(url)
        return url

    def __getPageContent(self, url):
        """获取每页的内容"""
        response = requests.get(url, headers = HEADERS)
        response.encoding = 'utf-8'
        content = response.text
        return content

    def __getNextPageUrl(self, content):
        """获取每页的10个链接"""
        soup = BeautifulSoup(content, 'lxml')
        try:
            pages = soup.find(id='page').find_all('a')
            pageSet = []
            for page in pages:
                # yield BAESE_URL + page.get('href')
                pageSet.append(BAESE_URL + page.get('href'))
            return pageSet[:-1] #去掉最后一条
        except:
            print("没有获取到任何信息")
            print("请手动检查该条链接是否有效")
            print(self.__firstUrl)
            exit(1)

    def __getItemsFromContent(self, content):
        """从 html 里面提取出新闻的链接"""
        soup = BeautifulSoup(content, 'lxml')
        try:
            items = soup.select('.t a')
            for i in items:
                yield i.get('href')
        except:
            print("没有获取到任何信息")
            print("请手动检查该条链接是否有效")
            print(self.__firstUrl)
            exit(1)

    def getUrl(self, site, numOfPage, keyWords=''):
        self.__firstUrl = self.__advanceSearch(site, keyWords) #为了方便错误调试 设置为类方法
        firstPage = self.__getPageContent(self.__firstUrl)
        pagesUrl = self.__getNextPageUrl(firstPage) #第一页的 10个链接
        urls = [self.__firstUrl] #我们需要的页数链接总数 第一页链接应该也得算上
        # 如果小于10
        if numOfPage <= 10:
            urls = urls + pagesUrl
        else:
            times = (numOfPage - 10) % 4 + 1#后面每页只能获取 4 条链接
            for i in range(0, times):
                lastPage = self.__getPageContent(pagesUrl[-1]) #已经获取到链接的最后一页的链接
                newUrls = self.__getNextPageUrl(lastPage)[-4:] #只有后四条不与前面重复
                urls = pagesUrl + newUrls

        urls = urls[:numOfPage]
        #获取链接
        hrefs = []
        for url in urls:
            content = self.__getPageContent(url)
            for href in self.__getItemsFromContent(content):
                hrefs.append(href)
        return hrefs


if __name__ == '__main__':
    test = Baidu_advance()

    hrefs = test.getUrl('caixin.com', 1, '江西')
    
    for i in hrefs:
        print(i)
    