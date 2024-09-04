from flask import Flask, render_template, request, redirect, session, g, url_for

import os

svrPath = '/home/LWork/mysite'
devPath = r'C:\Users\weic0\Desktop\test\Web\WebServer'
devpePath = '/storage/emulated/0/Download/Server/'

#os.chdir(devPath)
app = Flask(__name__,
            template_folder=f'{devPath}/web/',
            static_folder=f'{devPath}/web/static/')

app.secret_key = b'1233456789abcdef'

@app.before_request
def before_request():
    g.UserName = session.get('UserName')
    g.UserPermissionLevel = session.get('UserPermissionLevel')
    g.bIsBuy = session.get('bIsBuy')

@app.route('/', methods=['GET'])
def get_Host():
    #UserID = session.get('UserID') 
    UserName = session.get('UserName') 
    bIsLogin=False
    if UserName:
        bIsLogin=True
    return render_template('Home.html', UserName=UserName, bIsLogin=bIsLogin)


@app.route('/QA', methods=['GET'])
def QA():
    return render_template('QA.html')



from DatabaseMgr import *
from API.GlobalStdData import *
from API.Activation import *
import web.Login
import web.ContactUs
import web.Activate
import web.ChangeLog
import web.Shop
import web.Dev_FeedBack
import web.Dev_DBMgr

if __name__ == '__main__':
    app.run(port=8000,debug=True)
