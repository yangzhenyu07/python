import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


# 读取数据
df = pd.read_csv('parsed_logs.csv', sep=",")
df.columns = df.columns.str.strip()

# 将 timestamp 转换为日期时间格式，并提取小时、分钟、秒作为特征
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['minute'] = df['timestamp'].dt.minute
df['second'] = df['timestamp'].dt.second

# 将日志级别 (level) 转换为数值
level_mapping = {'INFO': 0, 'WARN': 1, 'ERROR': 2}
df['level'] = df['level'].map(level_mapping)

# 处理 trace_id：使用 MD5 哈希函数将其转换为一个数值
from hashlib import md5
df['trace_id_hash'] = df['trace_id'].apply(lambda x: int(md5(x.encode('utf-8')).hexdigest(), 16) % (10 ** 8))

# 选择特征：hour, minute, second, level, trace_id_hash
X = df[['hour', 'minute', 'second', 'level', 'trace_id_hash']]

# 使用 Isolation Forest 进行异常检测
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

# 预测：1表示正常，-1表示异常
y_pred = model.predict(X)

# 将预测的 -1（异常）和 1（正常）转换为 1 和 0
y_pred = np.where(y_pred == -1, 1, 0)

# 输出结果，假设异常为 1
df['is_anomaly'] = y_pred

# 打印检测到的异常数据
print(df[df['is_anomaly'] == 1])


