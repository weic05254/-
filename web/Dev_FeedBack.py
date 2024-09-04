from app import app, render_template, session, redirect ,LWork_conn,LWork_cursor,LWork_lock
from flask import jsonify, request
from datetime import datetime, timedelta, timezone

@app.route('/Dev_FeedBack', methods=['GET', 'POST', 'DELETE'])
def Dev_FeedBack():
    if request.method == 'GET':
        # 檢測 帳戶權限 0：一般用戶, 1：DEV
        member_id = session.get('UserID')
        iPermissionID = GetPermissionsByID(member_id)
        if iPermissionID:
            with LWork_lock:
                LWork_cursor.execute("SELECT * FROM FeedBack ORDER BY TimeStamp DESC")
                rows = LWork_cursor.fetchall()
            data = []

            for row in rows:
                id, name, email, issue_desc, timestamp = row
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
                formatted_time = dt.strftime('%Y年%m月%d日 %H:%M:%S')
                data.append((id, name, email, issue_desc, formatted_time))

            return render_template('Dev_FeedBack.html', data=data)
        else:
            return redirect('/')

def GetPermissionsByID(member_id):
    LWork_cursor.execute('SELECT PermissionLevel FROM Members WHERE id = ?', (member_id,))

    result = LWork_cursor.fetchone()
    return result[0]
