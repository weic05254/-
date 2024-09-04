from app import app,render_template,StdData_conn,StdData_cursor,StdData_lock
from flask import jsonify, request
import json
import zstandard as zstd

"""
@app.route('/apiTEST/Global_StdData', methods=['GET'])
def test_getdata():
    try:
        #data = get_request_data()
        cursor.execute("SELECT Term, ClassID, ClassName, Score FROM StdScoreData")
        rows = cursor.fetchall()
        result = [{"Term": row[0], "ClassID": row[1], "ClassName": row[2], "Score": row[3]} for row in rows]

        cctx = zstd.ZstdCompressor()
        compressed_data = cctx.compress(json.dumps(result).encode('utf-8'))
        return compressed_data, 200, {'Content-Encoding': 'zstd', 'Content-Type': 'application/json'}
    except Exception as e:
        return f"Error: {str(e)}", 500
"""

@app.route('/Global_StdData')
def View_Global_StdData():
    StdData_cursor.execute("SELECT Term, ClassID, ClassName, Score FROM StdScoreData")
    rows = StdData_cursor.fetchall()
 
    data_dict = {}
    for row in rows:
        term, class_id, class_name, score = row
        if class_id not in data_dict:
            data_dict[class_id] = {'ClassID': class_id, 'ClassName': class_name, 'ScoreList': []}
        data_dict[class_id]['ScoreList'].append(score)
    data = list(data_dict.values())

    processed_data = []
    for item in data:
        ClassID = item["ClassID"]
        ClassName = item["ClassName"]
        ScoreList = item["ScoreList"]
        
        # 平均
        Score_AVG = sum(ScoreList) / len(ScoreList) if len(ScoreList) > 0 else 0
        # 通過率
        PassRate = len([score for score in ScoreList if score >= 60]) / len(ScoreList) * 100 if len(ScoreList) > 0 else 0
        UnPassRate = len([score for score in ScoreList if score < 60]) / len(ScoreList) * 100 if len(ScoreList) > 0 else 0
        # 壓線通過率 60-65
        BorderlinePassRate = len([score for score in ScoreList if 60 <= score <= 65]) / len(ScoreList) * 100 if len(ScoreList) > 0 else 0
        # 資料總數
        ScoreList_Len = len(ScoreList)
        
        processed_data.append({
            'ClassID': ClassID,
            'ClassName': ClassName,
            'Score_AVG': Score_AVG,
            'PassRate': PassRate,
            'UnPassRate': UnPassRate,
            'BorderlinePassRate': BorderlinePassRate,
            'ScoreList_Len': ScoreList_Len
        })

    return render_template('Global_StdData.html', data=processed_data)

@app.route('/api/Global_StdData', methods=['GET'])
def Get_GlobalStdData():
    try:
        StdData_cursor.execute("SELECT Term, ClassID, ClassName, Score FROM StdScoreData")
        rows = StdData_cursor.fetchall()
        
        data_dict = {}
        for row in rows:
            term, class_id, class_name, score = row
            if class_id not in data_dict:
                data_dict[class_id] = {'ClassID': class_id, 'ClassName': class_name, 'ScoreList': []}
            data_dict[class_id]['ScoreList'].append(score)
        result = list(data_dict.values())
        
        cctx = zstd.ZstdCompressor()
        compressed_data = cctx.compress(json.dumps(result).encode('utf-8'))
        return compressed_data, 200, {'Content-Encoding': 'zstd', 'Content-Type': 'application/json'}
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/Global_StdData', methods=['POST'])
def Post_GlobalStdData():
    try:
        StdData_lock.acquire()
        data = get_request_data()
        ScoreData = data["ScoreDataDict"]
        StdID = data["StdID"]
        for i in ScoreData:
            StdData_conn.execute(f"INSERT OR IGNORE INTO StdScoreData (StdID, Term, ClassID, ClassName, Score) VALUES (?, ?, ?, ?, ?)",
                          (StdID, i["學年-學期"], i["課號"], i["科目名稱"], i["成績"]))
            StdData_conn.commit()
        return 'Success'
    except Exception as e:
        return f"Error: {str(e)}", 400
    finally:
        StdData_lock.release()

def get_request_data():
    try:
        content_length = int(request.headers['Content-Length'])
        post_data = request.get_data(as_text=True)
        return json.loads(post_data)
    except:
        return None
