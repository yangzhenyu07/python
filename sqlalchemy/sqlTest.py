from sqlalchemy import create_engine, Column, String, Integer, DateTime, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pathlib
import configparser

# 设置配置文件
current_dir = pathlib.Path(__file__).parent
config_file = current_dir / 'config' / 'sql.ini'
config = configparser.ConfigParser()
with open(config_file, 'r', encoding='utf-8') as f:
    config.read_file(f)

url = config['datasource']['url']
db = config['datasource']['db']

mysql_url = f'mysql+pymysql://{url}/{db}'
# 创建数据库引擎
"""
echo=True: 这表示在执行 SQL 查询时会输出所有 SQL 语句及其参数到控制台，方便调试。

pool_size=5: 这设置了数据库连接池的大小为 5，表示在连接池中最多可以保持 5 个连接。

max_overflow=4: 这允许在需要时，连接池外再创建最多 4 个额外的连接，超出连接池大小的部分会在使用后关闭。

pool_recycle=7200: 这表示连接在 7200 秒（2 小时）后会被回收，避免因长时间连接而导致的问题（例如，MySQL 的“互动超时”）。

pool_timeout=30: 这是连接池的超时时间，表示如果在 30 秒内没有获取到可用的连接，将会抛出异常。
"""
engine = create_engine(mysql_url, echo=True, pool_size=5, max_overflow=4, pool_recycle=7200, pool_timeout=30)

Base = declarative_base()

# 设置会话
Session = sessionmaker(bind=engine)
session = Session()


# 表结构
class YzyTest(Base):
    __tablename__ = 't_yzy_test'

    SEQUENCE_NO = Column(Integer, primary_key=True, autoincrement=True, comment='序列号')
    PK_STD_POINT_AI_RELATION = Column(String(36), unique=True, nullable=False, comment='id')
    FK_STD_AUDIT_POINT = Column(String(36), nullable=False, comment='审核标准id')
    FK_AI_STD = Column(String(36), nullable=False, comment='aiId')
    CHANNEL_TAG = Column(String(45), nullable=False, comment='渠道')
    FK_USER_CREATE = Column(String(36), nullable=True, comment='创建人id')
    USER_NAME_CREATE = Column(String(64), nullable=True, comment='创建人姓名')
    CREATE_TIME = Column(DateTime, default=text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间')

    __table_args__ = (
        Index('u_t_yzy_test_01', 'FK_STD_AUDIT_POINT', 'FK_AI_STD', 'CHANNEL_TAG', unique=True),
    )


# 创建表
def create_table():
    Base.metadata.create_all(engine)


# 查询数据
def query():
    return session.query(YzyTest).all()


# 插入数据
def save(param):
    session.add(param)
    session.commit()


# 更新数据
def update(param_id, updated_data):
    param = session.query(YzyTest).filter(YzyTest.PK_STD_POINT_AI_RELATION == param_id).first()
    if param:
        for key, value in updated_data.items():
            setattr(param, key, value)
        session.commit()


# 删除数据
def delete(param_id):
    param = session.query(YzyTest).filter(YzyTest.PK_STD_POINT_AI_RELATION == param_id).first()
    if param:
        session.delete(param)
        session.commit()


if __name__ == '__main__':
    create_table()

    # 示例用法：
    new_param = YzyTest(
        PK_STD_POINT_AI_RELATION='unique-id-1',
        FK_STD_AUDIT_POINT='audit-point-id',
        FK_AI_STD='ai-id',
        CHANNEL_TAG='channel-tag-example',
        USER_NAME_CREATE='创建者姓名'
    )
    save(new_param)

    params = query()
    for param in params:
        print(param.PK_STD_POINT_AI_RELATION, param.FK_STD_AUDIT_POINT, param.FK_AI_STD, param.CHANNEL_TAG, param.USER_NAME_CREATE)

    update('unique-id-1', {'CHANNEL_TAG': 'new_channel_tag'})
    params = query()
    for param in params:
        print(param.PK_STD_POINT_AI_RELATION, param.FK_STD_AUDIT_POINT, param.FK_AI_STD, param.CHANNEL_TAG, param.USER_NAME_CREATE)

    delete('unique-id-1')

