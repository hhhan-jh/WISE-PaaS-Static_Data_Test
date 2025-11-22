from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os
import traceback

app = Flask(__name__)
CORS(app)

FILENAME = "dummy_data_24hour.json"

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, FILENAME)
    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f: return json.load(f)

@app.route('/')
def home(): return "SimpleJson Server (Final - Time Filtered) Running!"

@app.route('/search', methods=['POST'])
def search():
    return jsonify(["distance", "x", "y", "collision_table"])

@app.route('/query', methods=['POST'])
def query():
    try:
        # [수정 1] 요청 데이터를 먼저 받아야 print를 할 수 있음
        req = request.get_json()
        
        # 디버깅: Grafana가 요청한 시간 범위 출력
        print(f"📡 Grafana 요청: {req['range']['from']} ~ {req['range']['to']}")

        raw_data = load_data()
        
        # [수정 2] 시간 필터링 적용
        from_time_str = req['range']['from']
        to_time_str = req['range']['to']
        
        filtered_data = []
        for row in raw_data:
            # ISO 포맷 문자열 비교 (해당 시간 범위 내 데이터만 골라냄)
            if from_time_str <= row['timestamp'] <= to_time_str:
                filtered_data.append(row)

        # [수정 3] 필터링된 데이터(filtered_data)를 사용해서 응답 생성
        response = []
        
        # 히트맵(x,y 동시 요청)을 위해 targets 반복문 사용
        for t in req['targets']:
            target_name = t.get('target')
            
            # 1. 표(Table) 요청
            if target_name == "collision_table":
                rows = []
                for row in filtered_data: # filtered_data 사용!
                    dt_str = row['timestamp'].replace("Z", "")
                    if "." in dt_str:
                        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
                    epoch_ms = int(dt.timestamp() * 1000)
                    rows.append([epoch_ms, row['sourceTag'], row['message'], row['x'], row['y'], row['distance']])
                
                response.append({
                    "type": "table",
                    "columns": [
                        {"text": "Time", "type": "time"},
                        {"text": "Tag", "type": "string"},
                        {"text": "Message", "type": "string"},
                        {"text": "X", "type": "number"},
                        {"text": "Y", "type": "number"},
                        {"text": "Dist", "type": "number"}
                    ],
                    "rows": rows
                })

            # 2. 그래프/카운트/히트맵용 데이터 (x, y, distance)
            else:
                datapoints = []
                for row in filtered_data: # filtered_data 사용!
                    dt_str = row['timestamp'].replace("Z", "")
                    if "." in dt_str:
                        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
                    epoch_ms = int(dt.timestamp() * 1000)
                    
                    val = 0
                    if target_name == "distance": val = row.get('distance', 0)
                    elif target_name == "x": val = row.get('x', 0)
                    elif target_name == "y": val = row.get('y', 0)
                    
                    datapoints.append([val, epoch_ms])
                
                response.append({
                    "target": target_name, 
                    "datapoints": datapoints
                })

        return jsonify(response)

    except Exception as e:
        print("Error:", traceback.format_exc())
        return jsonify([])

@app.route('/annotations', methods=['POST'])
def annotations(): return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)