import os
import pandas as pd
from sqlalchemy import create_engine
import datetime

# 读取文件并解析成 DataFrame
def read_data(file_path):
    try:
        # 读取数据，添加 on_bad_lines='skip' 来忽略格式错误的行
        df = pd.read_csv(file_path, sep='|', skipinitialspace=True, skiprows=1, on_bad_lines='skip')

        # 输出列数信息，便于调试
        print(f"读取的文件: {file_path}")
        print(f"原始列数: {df.shape[1]} 列")
        print(f"原始列名: {df.columns.tolist()}")

        # 检查列数是否符合预期，如果不符合，则根据实际情况调整
        expected_columns = ['start', '岗位', '区域', '薪资', '年限信息', '公司名称', '公司信息', '链接', 'end']
        if df.shape[1] == len(expected_columns):
            df.columns = expected_columns
        else:
            # 动态处理列数不匹配的情况
            print(f"列数不匹配，实际列数为 {df.shape[1]}，期望列数为 {len(expected_columns)}")
            return None  # 返回 None 表示文件格式不正确

        return df
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None


# 根据年限信息设置 LEVEL 值
def set_level(experience):
    if '3-5年' in experience:
        return '1'  # 3-5年为1
    elif '5-10年' in experience:
        return '0'  # 5-10年为0
    else:
        return '未知'  # 如果年限信息不符合规则则返回 None


# 根据区域信息设置城市
def set_city(var):
    cities = ['北京', '成都', '沈阳', '深圳', '西安', '郑州', '长沙', '重庆']
    for city in cities:
        if city in var:
            return city
    return '未知'  # 如果区域信息不符合规则则返回 '未知'


# 将 DataFrame 数据存储到 MySQL 数据库中
def save_to_db(df):
    # 数据库配置
    db_user = 'TESTDB'
    db_password = 'TESTDB'
    db_host = '127.0.0.1:3306'
    db_name = 'TESTDB?charset=utf8'

    # 创建数据库连接
    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

    # 为每一行设置 LEVEL 值和 CREATE_TIME
    df['LEVEL'] = df['年限信息'].apply(set_level)
    df['CITY'] = df['区域'].apply(set_city)
    df['CREATE_TIME'] = datetime.datetime.now()

    # 选择符合表结构的列并保存到 t_job_info 表
    df_to_save = df[['岗位', '区域', '薪资', '年限信息', '公司名称', '公司信息', 'LEVEL', 'CREATE_TIME', 'CITY']]
    df_to_save.columns = ['POSITION', 'REGION', 'SALARY', 'EXPERIENCE', 'COMPANY_NAME', 'COMPANY_INFO', 'LEVEL',
                          'CREATE_TIME', 'CITY']

    # 存储数据到 t_job_info 表
    df_to_save.to_sql('t_job_info', con=engine, if_exists='append', index=False)


# 遍历文件夹中的所有文件并处理
def process_all_files(directory):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # 只处理 .txt 文件
            file_path = os.path.join(directory, filename)
            print(f'Processing file: {file_path}')
            df = read_data(file_path)

            # 确认读取成功
            if df is not None:
                # 保存到数据库
                save_to_db(df)
            else:
                print(f"文件 {file_path} 处理失败，跳过。")


# 主函数
def main():
    directory = './file'  # 替换为你的文件夹路径
    process_all_files(directory)


if __name__ == '__main__':
    main()
