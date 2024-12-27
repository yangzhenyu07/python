import pandas as pd

log_file = "2024-12-19.0-dev.log"

try:
    with open(log_file, 'r', encoding='utf-8') as file:
        logs = []
        for line in file:
            logs.append(line)
    # 查看前几行日志
    for log in logs[:5]:
        print(log)
except Exception as e:
    print(f"出现错误: {e}")

