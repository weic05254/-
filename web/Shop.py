from app import app, render_template, session, redirect, LWork_conn, LWork_cursor, LWork_lock
from flask import jsonify, request, url_for, flash
import time




@app.route('/Shop', methods=['GET'])
def Shop():
    # 登入檢測
    member_id = session.get('UserID')
    if not member_id:
        return redirect('/')
    #已購買
    LWork_cursor.execute('SELECT id FROM Purchases WHERE Member_id = ? AND ShopItem_id = ?', (member_id, 1))
    result = LWork_cursor.fetchone()
    if result:
        return redirect('/activate')
    
    return render_template('Shop.html')


@app.route('/ShopMid', methods=['GET'])
def ShopMid():
    return render_template('ShopMid.html')


@app.route('/ShopFinal', methods=['GET'])
def ShopFinal():
    CurrTime  = int(time.time())
    member_id = session.get('UserID')
    with LWork_lock:
        LWork_conn.execute('INSERT INTO Purchases (Member_id, ShopItem_id, PurchaseDate) VALUES (?, ?, ?)', (member_id, 1, CurrTime))
        LWork_conn.commit()
    return render_template('ShopFinal.html')

