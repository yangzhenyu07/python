import json
import traceback
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from common.LogConfig import _logging
import logging
import pathlib
import configparser
from flask import Flask, jsonify

app = Flask(__name__)

# 日志和配置初始化
current_dir = pathlib.Path(__file__).parent
config_file = current_dir / 'config' / 'baiduConfig.ini'
config = configparser.ConfigParser()
with open(config_file, 'r', encoding='utf-8') as f:
    config.read_file(f)

log_file = current_dir / config['logging']['log_file']
log_level = config['logging'].get('log_level', 'INFO').upper()
log_back_up_days = config['logging'].getint('log_back_up_days', 5)

# 初始化日志配置
log_file.parent.mkdir(parents=True, exist_ok=True)
log = logging.getLogger(__name__)
logger = _logging(log, log_file, log_back_up_days, log_level)

app = Flask(__name__)


def get_python():
    """
    执行百度热搜抓取逻辑
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.54 Safari/537.36 '
    }

    url1 = 'https://top.baidu.com/board?platform=pc&sa=pcindex_entry'

    # 发起请求
    res = requests.get(url=url1, headers=header, timeout=10)

    res.encoding = 'utf-8'
    logger.info(f'状态码:{res.status_code}')

    soup_body = BeautifulSoup(res.text, 'html.parser')
    hot_search_items = soup_body.find_all("div", attrs={"class": "active-item_1Em2h"})

    result = []
    for item in hot_search_items:
        index = item.find("div", attrs={"class": "sign-index_mtI7K"})
        value = item.find("div", attrs={"class": "c-single-text-ellipsis"})
        num = index.text
        if num is None or num.strip() == "":
            continue
        # strip() 去空格
        logger.info(f'【{num.strip()}】,{value.text.strip()}')
        result.append(f'【{num.strip()}】,{value.text.strip()}')

    logger.info('<<<<<<<<<<<<百度热搜>>>>>>>>>>>>>>>')
    return result


@app.route('/get', methods=['GET'])
def get():
    try:
        logger.info("进入 /get 请求开始爬取百度热搜...")
        result = get_python()  # 调用函数并获取结果
        return app.response_class(
            response=json.dumps(result, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())  # 输出详细的堆栈信息
        return jsonify({"error": str(e)}), 500  # 返回错误信息和状态码


# 主页
@app.route('/')
def index():
    print('Hello, World!')
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
