# 线性回归模型
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 样本数据
X = np.array([[120, 3], [110, 3], [200, 4], [220, 4], [90, 2]])
y = np.array([1500000, 1600000, 2000000, 1600000, 1100000])

# 创建线性回归模型
model = LinearRegression()
model.fit(X, y)

# 预测新的房价
new_house = np.array([[210, 3]])  # 新房子的面积和卧室数量
predicted_price = model.predict(new_house)
print(f"预测的房价: {predicted_price[0]:,.2f}元")

# 可视化
plt.figure(figsize=(8, 6))
# 函数用于绘制散点图，X[:, 0] 表示取二维数组 X 的所有行的第一个元素（即面积数据），y 是房价数据。散点的颜色设置为蓝色 (color='blue')。
# 真实面积下的真实房价-散点图
plt.scatter(X[:, 0], y, color='blue')
# 函数用于绘制线图，X[:, 0] 是面积数据，model.predict(X) 是使用模型预测得到的房价数据。这条线代表了模型在给定面积下的预测房价。线的颜色设置为红色
# 模型在给定面积下的预测房价-线性图
plt.plot(X[:, 0], model.predict(X), color='red')
plt.xlabel('面积 (平方米)')
plt.ylabel('房价 (元)')
plt.title('房价预测')
plt.show()
