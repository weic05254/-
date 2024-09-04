from app import app, render_template, session,LWork_conn,LWork_cursor,LWork_lock
from flask import jsonify, request

import time




@app.route('/api/ActivationStatus', methods=['GET'])
def Get_ActivationStatus():

    hwid = request.json.get('HWID')
    if not hwid:
        return {'error': '參數錯誤'}, 400

    LWork_cursor.execute('SELECT Activated, ExpiryDate FROM ActivationCodes WHERE HWID = ?', (hwid,))
    result = LWork_cursor.fetchone()

    if result:
        Activated, ExpiryDate = result
        return {'ExpiryDate': ExpiryDate, 'Activated': bool(Activated)}
    else:
        ExpiryDate = int(time.time()) + 15  # 單位/秒 
        try:
            LWork_lock.acquire()
            LWork_conn.execute('INSERT INTO ActivationCodes (HWID, ExpiryDate) VALUES (?, ?)', (hwid, ExpiryDate))
            LWork_conn.commit()
            return {'ExpiryDate': ExpiryDate, 'Activated': False}
        except Exception as e:
            return f"Error: {str(e)}", 500
        finally:
            LWork_lock.release()




if __name__ == '__main__':

    app.run(debug=True)

