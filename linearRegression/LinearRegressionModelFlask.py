# app.py
from flask import Flask, request, jsonify, send_file
import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import io
import traceback

app = Flask(__name__)
matplotlib.use('Agg')
# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 加载模型
# 模型数据通常不会直接用于生成图像，而是用于预测或处理数据。
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # 数据验证
    if 'area' not in data or 'num' not in data:
        return jsonify({'error': 'Invalid input data. Please provide "area" and "num".'}), 400

    try:
        new_house = np.array([[float(data['area']), float(data['num'])]])
    except ValueError:
        return jsonify({'error': 'Invalid input data. "area" and "num" must be numeric values.'}), 400

    new_house = np.array([[data['area'], data['num']]])
    prediction = model.predict(new_house)
    return jsonify({'prediction': prediction[0]})


@app.route('/predictUI', methods=['POST'])
def predictUI():
    try:
        data_list = request.get_json(force=True)

        if not isinstance(data_list, list):
            return jsonify({'error': '输入数据必须是对象列表。'}), 400

        predictions = []
        areas = []

        for data in data_list:
            if 'area' not in data or 'num' not in data:
                return jsonify({'error': '每个对象必须包含 "area" 和 "num" 属性。'}), 400

            try:
                new_house = np.array([[float(data['area']), float(data['num'])]])
            except ValueError:
                return jsonify({'error': '无效的输入数据。"area" 和 "num" 必须是数值。'}), 400

            prediction = model.predict(new_house)[0]
            predictions.append(prediction)
            areas.append(data['area'])

        # 生成图像
        plt.figure(figsize=(8, 6))
        plt.scatter(areas, predictions, color='blue', label='模型在给定面积下的预测房价-散点图')
        plt.plot(areas, predictions, color='red', label='模型在给定面积下的预测房价-线性图')

        plt.xlabel('面积 (平方米)')
        plt.ylabel('房价 (元)')
        plt.title('房价预测')
        plt.legend()

        # 将图像保存到内存缓冲区
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        # 清理图像以供下次使用
        plt.clf()
        plt.close()

        # 返回图像文件
        return send_file(img_buf, mimetype='image/png')
    except Exception as e:
        # 打印完整的错误堆栈跟踪信息
        traceback.print_exc()
        return jsonify({'error': '服务器内部错误'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

