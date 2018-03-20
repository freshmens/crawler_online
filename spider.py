#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import urllib
import re
import csv
import time
def get_product_info():
    fileName = '商品.csv'
    comment_file = open(fileName, 'w')
    write = csv.writer(comment_file)
    data = ['商品名', '连接', '销售量', '价格', '地址', '累计评价']
    a = []
    for i in data:
        a.append(i.decode("utf-8").encode("gbk"))
    write.writerow(a)
    comment_file.close()

def get_product(url):
    global itemId
    global sellerId
    global titles
    head = {}
    # 写入User Agent信息
    head[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    # 创建Request对象
    res =requests.get(url, headers=head)
    # 读取响应信息并解码
    html = res.text.encode(res.encoding).decode('utf-8')
    # 打印信息
    pattam_id = '"nid":"(.*?)"'
    raw_title = '"raw_title":"(.*?)"'
    view_price = '"view_price":"(.*?)"'
    view_sales = '"view_sales":"(.*?)"'
    item_loc = '"item_loc":"(.*?)"'
    user_id = '"user_id":"(.*?)"'
    all_id = re.compile(pattam_id).findall(html)
    all_title = re.compile(raw_title).findall(html)
    all_price = re.compile(view_price).findall(html)
    all_sales = re.compile(view_sales).findall(html)
    all_loc = re.compile(item_loc).findall(html)
    all_userid = re.compile(user_id).findall(html)
    print("start")
    for i in range(10):
            this_id = all_id[i]
            this_title = all_title[i]
            this_price = all_price[i]
            this_sales = all_sales[i]
            this_loc = all_loc[i]
            this_userid = all_userid[i]
            id = str(this_id)
            title = str(this_title)
            price = str(this_price)
            sales = str(this_sales)
            loc = str(this_loc)
            uid = str(this_userid)
            link = 'https://item.taobao.com/item.htm?id=' + str(id)
            commentlink = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='+id+'&currentPageNum=1'
            head = {}
            # 写入User Agent信息
            head[
                'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
            # 创建Request对象
            res2 = requests.get(commentlink, headers=head)
            # 读取响应信息并解码
            html2 = res2.text.encode(res.encoding).decode('utf-8')
            rateTotal = '"total":(.*?,)"'
            all_rateTotal = re.compile(rateTotal).findall(html2)
            this_rateTotal = all_rateTotal
            rateTotal = str(this_rateTotal)[3:-3]
            print rateTotal
            comment_file = open('商品.csv', 'a')
            data2 = [title, link, sales, price, loc, rateTotal]
            a2 = []
            for i in data2 :
                a2.append(i.decode("utf-8").encode("gbk"))
            write = csv.writer(comment_file)
            write.writerow(a2)
            comment_file.close()


    print("end")

if __name__ == "__main__":
    start = time.time()
    get_product_info()
    url = 'https://s.taobao.com/search?q=%E6%99%BA%E8%83%BD%E9%94%81&sort=sale-desc'
    get_product(url)
    end = time.time()
    total = end-start
    print('timeTotal:{:.2f}s!'.format(total))