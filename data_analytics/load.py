import json
import pandas as pd

# def load(file):
#     with open(file) as f:
#         data = json.load(f)
#     return data


json_file = './data_analytics/testsuite_1_metrics.json'
# print (load(json_file)[0])

data = pd.read_json(json_file)
df = pd.DataFrame(data)
print(df)