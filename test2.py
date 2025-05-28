import pandas as pd
import re


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


# 示例数据
news_list = [
    {'标题': '世界无人机大会：<font color=red>AI</font>加持，解锁低空经济无限潜能', '发布时间': '2025-05-24 16:28:32',
     '状态码': 200, '内容': '...'},
    {'标题': '世界无人机大会：<font color=red>AI</font>加持，解锁低空经济无限潜能', '发布时间': '2025-05-24 16:28:20',
     '状态码': 200, '内容': '...'},
    {'标题': '另一条新闻标题', '发布时间': '2025-05-24 16:28:10', '状态码': 200, '内容': '...'}
]

# 调用去重函数
duplicated_news_list = drop_duplicate(news_list)

# 打印结果
print(duplicated_news_list)
print(len(duplicated_news_list))