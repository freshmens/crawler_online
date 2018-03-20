#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import re
import time
product = []
#others = []
def get_phone_info() :
    url = 'http://mobile.mi.com/in/category/'
    head = {}
    # 写入User Agent信息
    head[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    # 创建Request对象
    res =requests.get(url, headers=head)
    # 读取响应信息并解码
    html = res.text.encode(res.encoding).decode('utf-8')
    #找到所有产品的产品id
    find_all_product_id(html)
    #print product
    #print "start"
    list1 = []
    for id in product :
        #print id
        new_url = 'http://m.buy.mi.com/in/misc/getgoodsinformation/?tag='+ str(id)
        #print new_url
        head[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
        # 创建Request对象
        res2 =requests.get(new_url, headers=head)
        # 读取响应信息并解码
        html2 = res2.text.encode(res.encoding).decode('utf-8')
        #is_cos 用于判断是否缺货，name表示缺货产品名称
        on_sale = '"is_cos":(.*?,)'
        on_name = '"name":"(.*?)"'
        sale = re.compile(on_sale).findall(html2)
        name = re.compile(on_name).findall(html2)
        this_sale = sale
        this_name = name
        print this_sale
        for s in range(len(this_sale)):
            #print s
            st = this_sale[s]
            print st[0:-1]
            if(st[0:-1] == 'true'):
                list1.append(this_name[s].encode('utf-8'))
    print list1
    string = "\n"
    content = string.join(list1)
    print content

def get_next_product_id(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('product_id=', start_link)
    end_quote = page.find('"', start_quote + 1)
    product_id = page[start_quote + len('product_id='): end_quote]
    return product_id, end_quote

def find_all_product_id(page):
    while True:
        product_id, endpos = get_next_product_id(page)
        print product_id
        if product_id:
            product.append(product_id.encode('utf-8'))
            #print product
            page = page[endpos:]
        else:
            break


if __name__ == "__main__":
    start = time.time()
    get_phone_info()
    end = time.time()
    total = end-start
    print('timeTotal:{:.2f}s!'.format(total))