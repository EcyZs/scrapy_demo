import requests
from lxml import etree
import json
import time
import httpx
import re
import pandas as pd
# 开始时间
start_time = time.time()
# 创建存储列表
news_list=[]

# 第一步 请求接口
url='https://so.news.cn/getNews'

# 第二步 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.772.64',
    'Referer': 'https://so.news.cn/',
    'Cookie':'localNewsIndex=0; localNewsInfo=%E5%8C%97%E4%BA%AC'
}

# 第三步 请求参数
#lang=cn&curPage=1&searchFields=1&sortField=0&keyword=AI
params = {
    'lang': 'cn',
    'curPage': '1',
    'searchFields': '1',
    'sortField': '0',
    'keyword': 'AI'

}

# 第四步 清洗标签函数
def clean_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text


# 第五步 去重函数
def drop_duplicate(dict_list, subject=['标题']):
    # 清洗标题中的HTML标签
    for item in dict_list:
        item['标题'] = clean_html_tags(item['标题'])

    df = pd.DataFrame(dict_list)
    df = df.drop_duplicates(subset=subject, keep='first')
    return df.to_dict('records')

# 第六步 数据保存函数
def save_data(duplicated_news_list):
    with open('DATA/news.json', 'w', encoding='utf-8') as f:
        json.dump(duplicated_news_list,f,ensure_ascii=False,indent=2)

# 第七步 定义内容提取类
class Contentparse:
    def __init__(self):
        self.content_p=''
    def parse_p(self,element):

        # 第一步 先处理本节点有没有文本，如果有，直接打印
        if element.text:
            self.content_p+=element.text
            print(element.text)
        elif element.tag == 'img':
            self.content_p+=element.xpath('./@src')[0]
            print(element.xpath('./@src'))
        # 第二步 再处理本节点有没有子节点

        for son_element in element:
            self.parse_p(son_element)

def parse_p(element):
    # 第一步 先处理本节点有没有文本，如果有，直接打印
    if element.text:
        print(element.text)
    elif element.tag == 'img':
        print(element.xpath('./@src'))

    # 第二步 再处理本节点有没有子节点
    for son_element in element:
        parse_p(son_element)

# 第八步 修改params以换页
for i in range(1,11):
    params['curPage']=str(i)

    # 第九步 每一页发送一个请求
    response = requests.get(url=url,headers=headers,params=params)
    print(f'当前为第{i}页->{response.status_code}')
    response=response.json()
    # 第十步 获取文章列表
    content = response['content']
    results = content['results']

    # 第十一步 遍历每一页上的文章
    for result in results:

        # 第十二步 获取文章的 标题 时间 详细页url
        title = result['title']
        pubtime = result['pubtime']
        url2 = result['url']
        print(f'标题:{title}    发布时间:{pubtime}')

        # 第十三步 进入详细页面，爬取内容
        response2= requests.get(url=url2,headers=headers)
        print(response2.status_code)

        # 第十四步 获取内容结构

        article = etree.HTML(response2.text).xpath('//span[@id="detailContent"]')
        if not article:
            print('文章结构不符合')
            my_dict = {}
            my_dict['标题'] = title
            my_dict['发布时间'] = pubtime
            my_dict['状态码'] = response2.status_code
            my_dict['内容'] = '文章结构不符合，可能是视频类新闻等'
            news_list.append(my_dict)
            continue

        ps = article[0].xpath('./p')


        # 第十五步 遍历每个p，并使用内容处理函数
        parser = Contentparse()
        for p in ps:
            parser.parse_p(p)

        # 第十六步 数据保存到列表
        my_dict={}
        my_dict['标题'] = title
        my_dict['发布时间'] = pubtime
        my_dict['状态码'] = response2.status_code
        my_dict['内容'] = parser.content_p
        news_list.append(my_dict)


print('数据获取完毕')
# 第十七步 数据去重
duplicated_news_list = drop_duplicate(news_list)
# 第十八步 数据保存到json
save_data(duplicated_news_list)

df=pd.DataFrame(duplicated_news_list)
df.to_csv('DATA/news.csv',index=False,encoding='utf-8-sig')

print(f'保存结束，共{len(duplicated_news_list)}条数据')

# 结束时间
end_time = time.time()
print('耗时：{}秒'.format(end_time - start_time))








