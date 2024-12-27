import re
import pandas as pd

log_file = "2024-12-19.0-dev.log"

# 尝试读取日志文件
try:
    with open(log_file, 'r', encoding='utf-8') as file:
        logs = [line.strip() for line in file]  # 使用列表推导式，去除每行的多余空白
except Exception as e:
    print(f"出现错误: {e}")

# 定义正则表达式来解析日志行
log_pattern = re.compile(
    r'(?P<timestamp>\S+\s\S+)\s*\[(?P<trace_id>[a-f0-9]+)\]\s*-\s*(?P<level>\w+)\s+---\[(?P<thread_name>[^\]]+)\]\s*(?P<class_name>\S+.*\S+)\s*:\s*(?P<message>.*)'
)

# 用于存储解析后的日志信息
parsed_logs = []

# 解析每一行日志
for log in logs:
    match = log_pattern.match(log)
    if match:
        parsed_logs.append(match.groupdict())

# 将解析后的日志转换为 DataFrame
df = pd.DataFrame(parsed_logs)

# 显示前几行数据及列名
print(df.head())
print(df.columns)

# 将 DataFrame 转换为 CSV 格式并保存到文件
df.to_csv('parsed_logs.csv', index=False, encoding='utf-8')

# 如果你仍然希望将其保存为纯文本
df_str = df.to_string(index=False)
with open('parsed_logs.txt', 'w', encoding='utf-8') as f:
    f.write(df_str)

print("数据已保存到 parsed_logs.txt 和 parsed_logs.csv 文件")
