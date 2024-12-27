# 线性回归模型
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# 样本数据
X1 = np.array([[120, 3], [110, 3], [200, 4], [220, 4], [90, 2]])
y1 = np.array([1500000, 1600000, 2000000, 1600000, 1100000])

# 创建线性回归模型
model = LinearRegression()
model.fit(X1, y1)

# 保存模型
# 运行这个文件，它会生成一个名为model.pkl的文件，这就是我们训练好的模型。
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
