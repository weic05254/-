from app import app, render_template, session ,LWork_conn,LWork_cursor,LWork_lock
from flask import jsonify, request

# 啟用會員頁面
@app.route('/activate', methods=['GET', 'POST', 'DELETE'])
def activate():
    member_id = session.get('UserID')
    item_id = 1
    if request.method == 'DELETE':
        hwid = request.args.get('hwid')
        deactivate_hwid(member_id, hwid)

    if request.method == 'POST':   
        hwid = request.form['hwid']        
        if not member_id:
            return '您尚未登入'

        result = activate_hwid(member_id, hwid, item_id)
        #if result:
        return result

    if request.method == 'GET':
        # [ex]檢測 是否已付款

        LWork_cursor.execute('SELECT id FROM Purchases WHERE Member_id = ? AND ShopItem_id = ?', (member_id, item_id))
        result = LWork_cursor.fetchone()
        if not result:
            return f'您尚未購買{item_id}'
        else:
            LWork_cursor.execute('SELECT id FROM Purchases WHERE Member_id = ? AND ShopItem_id = ?', (member_id, item_id))
            result = LWork_cursor.fetchone()


    hwids = Member_Query_HWID(member_id, item_id)
    return render_template('Activate.html', hwids=hwids)



# 測試會員新增指定 HWID
def activate_hwid(member_id, hwid, item_id):
    LWork_cursor.execute('SELECT id,Activated FROM ActivationCodes WHERE HWID = ?', (hwid,))
    result = LWork_cursor.fetchone()
    if result:
        if CheckHWIDLimitExc(member_id):
            return f'您已超過序號啟用最大限制'

        if result[1] == 1:
            return f'錯誤：{hwid} 已是起用狀態'


        with LWork_lock:
            LWork_conn.execute('INSERT INTO MemberHWID (Member_id, Item_id, HWID) VALUES (?, ?, ?)', (member_id, item_id, hwid))
            LWork_conn.execute('UPDATE ActivationCodes SET Activated = 1 WHERE HWID = ?', (hwid,))
            LWork_conn.commit()
        return f'{hwid} 啟用成功'
    else:

        return f'錯誤：HWID不存在'
#是否超出限制    
def CheckHWIDLimitExc(Member_id,Limit=2):
    with LWork_lock:
        LWork_cursor.execute('SELECT id FROM MemberHWID WHERE Member_id = ?', (Member_id,))
        result = LWork_cursor.fetchall()
    
    if len(result) >= Limit:
        return 1

    return 0

# 測試會員移除指定 HWID
def deactivate_hwid(member_id, hwid):
    with LWork_lock:
        LWork_conn.execute('DELETE FROM MemberHWID WHERE Member_id = ? AND HWID = ?', (member_id, hwid))
        LWork_conn.execute('UPDATE ActivationCodes SET Activated = 0 WHERE HWID = ?', (hwid,))
        LWork_conn.commit()


# Member查 hwid
def Member_Query_HWID(member_id, item_id):
    
    LWork_cursor.execute('SELECT HWID FROM MemberHWID WHERE Member_id = ? AND Item_id = ?', (member_id, item_id))
    results = LWork_cursor.fetchall() 
    return results if results else []
