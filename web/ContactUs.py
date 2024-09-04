from app import app, render_template, session ,LWork_conn,LWork_cursor,LWork_lock
from flask import jsonify, request
import time
from datetime import datetime, timedelta, timezone

# 啟用會員頁面
@app.route('/ContactUs', methods=['GET','POST'])
def ContactUs():

    if request.method == 'POST':
         
        Name = request.form['Name']
        Email = request.form['Email']
        IssueDesc = request.form['IssueDesc']
        TimeStamp = int(time.time())
        with LWork_lock:
            LWork_conn.execute('INSERT INTO FeedBack (Name, Email, IssueDesc, TimeStamp) VALUES (?, ?, ?, ?)', (Name, Email, IssueDesc, TimeStamp))
            LWork_conn.commit()
        return jsonify('success')
    
    
    if request.method == 'GET':

        return render_template('ContactUs.html')

