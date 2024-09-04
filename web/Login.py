from app import app, render_template, session, redirect, LWork_conn, LWork_cursor, LWork_lock
from flask import jsonify, request, url_for
from flask_mail import Message, Mail
import time
import hashlib

app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('maoyan', 'm@mz'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='d1104241041@gm.lhu.edu.tw',
    MAIL_PASSWORD=''
)
mail = Mail(app)


def GetMD5(input):
    md5_hash = hashlib.md5()
    md5_hash.update(input.encode('utf-8'))
    return md5_hash.hexdigest()


@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = GetMD5(request.form['password'])

        LWork_cursor.execute('SELECT id, IsVerified, V_ExpirationTime, Email, PermissionLevel FROM Members WHERE UserName = ? AND Pwd = ?', (username, password))
        result = LWork_cursor.fetchone()
        # 帳號存在
        if result:
            UserID, IsVerified, expirationTime, Email, PermissionLevel = result[0], result[1], result[2], result[3], result[4]
            # 尚未完成信箱驗證
            if not IsVerified:
                # 驗證碼 已過期
                if expirationTime > time.time():
                    return f'帳號還在驗證中，請至您的信箱({Email})進行驗證'
                else:
                    verification_code,expirationTime_epoch = Register_SendMail(Email)
                    LWork_cursor.execute('UPDATE Members SET VerificationCode = ?, V_ExpirationTime = ? WHERE UserName = ?', 
                                         (verification_code, expirationTime_epoch, username))
                    LWork_conn.commit()
                    return f'驗證碼已過期，新的驗證碼已發送至您的信箱:({Email})'
                
            # 完成信箱驗證&帳密正確
            else:
                with LWork_lock:
                    LWork_cursor.execute('SELECT id FROM Purchases WHERE Member_id = ? AND ShopItem_id = ?', (UserID, 1))
                    result = LWork_cursor.fetchone()
                    if result:
                        session['bIsBuy'] = 1
                session['UserID'] = UserID
                session['UserName'] = username
                session['UserPermissionLevel'] = PermissionLevel
                return redirect('/')
            
        else:
            return '帳號或密碼錯誤'
    return render_template('Login.html')


@app.route('/Logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


import random
import string

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        # 密碼不一致
        if password != confirm_password:
            return '密碼不一致'
        
        # 檢測 UserName
        LWork_cursor.execute('SELECT id FROM Members WHERE UserName = ?', (username,))
        if LWork_cursor.fetchone():
            return '帳號已存在'
        # 檢測 Email
        LWork_cursor.execute('SELECT id FROM Members WHERE Email = ?', (email,))
        if LWork_cursor.fetchone():
            return '電子郵件已被使用'

        # 傳送驗證mail
        verification_code,expirationTime_epoch = Register_SendMail(email)
        # 儲存帳號資料
        LWork_cursor.execute('INSERT INTO Members (UserName, Pwd, Email, VerificationCode, V_ExpirationTime, IsVerified) VALUES (?, ?, ?, ?, ?, ?)',
                            (username, GetMD5(password), email, verification_code, expirationTime_epoch, 0))
        LWork_conn.commit()
        return '註冊成功，請至信箱驗證'

    return render_template('Register.html')


def Register_SendMail(email):
    #生成 驗證碼|驗證到期時間(epoch)|驗證url
    verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    expirationTime_epoch = int(time.time()) + 300  # 300 秒
    verification_url = url_for('Register_VerifyEmail', verification_code=verification_code, _external=True)
    #寄信
    msg = Message('信箱驗證', recipients=[email])
    msg.body = f'點擊以下連結進行驗證:\n {verification_url}'
    mail.send(msg)

    return verification_code,expirationTime_epoch


@app.route('/verify/<verification_code>', methods=['GET'])
def Register_VerifyEmail(verification_code):
    # 檢查驗證碼是否有效
    LWork_cursor.execute('SELECT UserName, V_ExpirationTime FROM Members WHERE VerificationCode = ?', (verification_code,))
    result = LWork_cursor.fetchone()
    #print(result)
    if result:
        username, expirationTime = result[0], result[1]
        if expirationTime > time.time():
            LWork_cursor.execute('UPDATE Members SET IsVerified = 1 WHERE UserName = ?', (username,))
            LWork_conn.commit()
            return '驗證成功'
        else:
            return '驗證碼已過期，請登入後重新取得驗證碼'
    else:
        return '驗證碼無效或已過期'