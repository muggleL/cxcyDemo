## baidu_advance.py

百度高级搜索爬虫

输入: 需要搜索的网站 需要获取的页数 关键词

输出: 由爬到的链接构成的 list

用法：

```python
get = Baidu_andvance()
urls = get.getUrl('caixin.com', 10, '工商银行'）
```
## caixin_spider.py

财新网爬虫

输入: 财新网链接

输出： 用 yield 打包的新闻

例：

```python
from baidu_advance import Baidu_advance  # just for test
test = CaixinSpider()
baidu = Baidu_advance()
urls = baidu.getUrl('finance.caixin.com', 20, '招商银行')
contents = test.get(urls)
f = open('caixin_baidu_test.txt', 'a+')
for i in contents:
    f.write(i)
f.close()
```
