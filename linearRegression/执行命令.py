# 1、https://pypi.org/project/scikit-learn/#files 下载scikit_learn
# 注意的是要找和你当前python兼容的版本，我的版本:Python 3.10.9
# pip install scikit_learn-0.24.2-cp39-cp39-manylinux2010_x86_64.whl
# python LinearRegressionModel_test.py
# python LinearRegressionModelFlask.py
# curl -X POST http://127.0.0.1:8081/predict -H "Content-Type: application/json" -d "{\"area\": 120, \"num\": 3}"
# curl -X POST http://127.0.0.1:8081/predictUI -H "Content-Type: application/json" -d "{\"area\": 120, \"num\": 3}"