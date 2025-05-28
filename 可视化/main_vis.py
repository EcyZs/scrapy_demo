import pandas as pd
import matplotlib.pyplot as plt

# 第零步 设置matplotlib的全局字体为SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 第一步 读取csv文件
df=pd.read_csv('D:/1陈阳/python工程/python爬虫突击/1新华网爬取项目/DATA/news.csv')

# 第二步 将时间格式转化为datetime格式
df['发布时间'] = pd.to_datetime(df['发布时间'])

# 第三步 按天聚合
daily_counts=df.groupby(df['发布时间'].dt.date).size()


# 绘制趋势图
plt.figure(figsize=(10, 6))
plt.plot(daily_counts.index, daily_counts.values, marker='o')
plt.xlabel('日期')
plt.ylabel('新闻数量')
plt.title('新闻发布时间趋势图（按天）')
plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
plt.tight_layout()  # 自动调整布局
plt.show()







