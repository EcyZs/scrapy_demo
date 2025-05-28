# 爬取新华网有关AI的前100条新闻
# 1.标题 2.时间 3.内容
# 使用request库，lxml进行数据采集
import requests
from lxml import etree
import json
import time
import httpx
import pandas as pd
import re
# 开始时间
start_time = time.time()

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
# 第四步 测试一
# response = requests.get(url, headers=headers, params=params)
# print(response.status_code)
# print(response.text)
# 请求2页测试
# for i in range(1, 3):
#     params['curPage'] = str(i)
#     response = requests.get(url, headers=headers, params=params)
#     print(i)
#     print(response.status_code)

# 接口返回网页为json格式
# 每条新闻位置json文件->content->results
# 标题位置results->title
# 时间位置results->pubtime
# 链接位置results->url


# 第五步 测试二--->获取第一页第一个新闻
# response = requests.get(url, headers=headers, params=params).json()
# content = response['content']
# results = content['results']
# no_1=results[0]
# title = no_1['title']
# pubtime = no_1['pubtime']
# print(title)
# print(pubtime)

# 第五步 测试三--->获取第一页所有
# response = requests.get(url, headers=headers, params=params).json()
# content = response['content']
# results = content['results']
# for result in results:
#     title = result['title']
#     pubtime = result['pubtime']
#     print(title)
#     print(pubtime)

# 第六步 测试四--->获取两页所有新闻
# for i in range(1, 3):
#     print('第{}页'.format(i))
#     params['curPage'] = str(i)
#     response = requests.get(url, headers=headers, params=params).json()
#     content = response['content']
#     results = content['results']
#     for result in results:
#         title = result['title']
#         pubtime = result['pubtime']
#         print(title)
#         print(pubtime)

# # 第七步 测试五--->获取第一页第5个新闻的内容
# response = requests.get(url, headers=headers, params=params).json()
# content = response['content']
# results = content['results']
# no_5 = results[4]
# url = no_5['url']
# print(url)


# 详细页内容位置://span[@id="detailContent"]
# 详细页每一自然段用了一个p
# 有些p下面直接是文字，如：  甘肃省张掖市高台县解放街小学教师徐迎春担心，AI过度使用或让一些学生“放弃思考”。她说，AI更擅长“打直球”，让学生越过循序渐进、抽丝剥茧的理解思考和钻研过程。
# 有些p下面有图片，如：<img id="Hpce5v7S7npe4YDBC1iU" style="margin: 0 auto; display: block; float: none;" src="20250523b2ac6df08862412dacd1da068dca297b_20250523940d4f3f420d4c378898b04566195adb.jpg" data-material-id="2025052308191823" data-name="20250523940d4f3f420d4c378898b04566195adb.jpg">
# 有些p下面是次要标题，如：<span style="color: #000080;"><strong> 让AI成为辅助教学“多面手”</strong></span>
# 有些p下面是特殊字体，如：<span style="font-family: 楷体; color: #000080;">西北师范大学附属中学学生利用智慧平板电脑开展原电池实验演示。（受访者提供）</span>
# 总结规律之后发现主要就以下三种形式
#
# - p→文本
# - p→span→文本
# - p→img→@id 图片路径


# 第八步 尝试单个网页解析---设计算法解决不同自然段不一致问题
# def parse_p(element):
#     # 第一步 先处理本节点有没有文本，如果有，直接打印
#     if element.text:
#         print(element.text)
#     elif element.tag == 'img':
#         print(element.xpath('./@src'))
#     # 第二步 再处理本节点有没有子节点
#
#     for son_element in element:
#         parse_p(son_element)


# url2='https://education.news.cn/20250523/b2ac6df08862412dacd1da068dca297b/c.html'
# response = requests.get(url2, headers=headers).text
# # 正文部分：//span[@id="detailContent"]
# article = etree.HTML(response).xpath('//span[@id="detailContent"]')[0]
# ps=article.xpath('./p')
# # 循环所有p
# for p in ps:
#     parse_p(p)


# 第九步 测试爬取一页10个新闻标题，时间，内容，保存到list，最后set去重，并打印去重结果

class contentparse:
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


news_list=[]
response = requests.get(url, headers=headers, params=params).json()
content = response['content']
results = content['results']
for result in results:
    title = result['title']
    pubtime = result['pubtime']
    my_dict={}
    url2 = result['url']
    print(f'标题:{title}    发布时间:{pubtime}')
    my_dict['标题']=title
    my_dict['发布时间']=pubtime

    # 进入详细页面，爬取内容
    response2 = requests.get(url=url2, headers=headers)
    print(response2.status_code)
    my_dict['状态码']=response2.status_code
    #获取内容结构
    article = etree.HTML(response2.text).xpath('//span[@id="detailContent"]')[0]
    ps = article.xpath('./p')


    # 第十二步 遍历每个p，并使用内容处理函数
    parser=contentparse()
    for p in ps:
        parser.parse_p(p)

    my_dict['内容']=parser.content_p
    news_list.append(my_dict)

#     my_dict['内容']=Content_p
#     news_list.append(my_dict)
#
#
print(news_list)

# 去重方法

# 清洗HTML标签的函数
def clean_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text


# 去重函数
def drop_duplicate(dict_list, subject=['标题']):
    # 清洗标题中的HTML标签
    for item in dict_list:
        item['标题'] = clean_html_tags(item['标题'])

    df = pd.DataFrame(dict_list)
    df = df.drop_duplicates(subset=subject, keep='first')
    return df.to_dict('records')

duplicated_news_list=drop_duplicate(news_list)

print(duplicated_news_list)

def save_data(duplicated_news_list):
    with open('DATA/news.json', 'w', encoding='utf-8') as f:
        json.dump(duplicated_news_list,f,ensure_ascii=False,indent=2)

save_data(duplicated_news_list)
# 结束时间
end_time = time.time()
print('耗时：{}秒'.format(end_time - start_time))










