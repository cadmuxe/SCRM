#-*- coding:utf-8 -*-
from flask import Flask, g, request, session, redirect, url_for
from flask import render_template as r_t
import pymongo, hashlib

app = Flask(__name__)
app.secret_key = 'SDFsdf@#$sddf34nsSSWD3422^oiudf%sfwdsfsDSFAS'

# settings
class settings():
    def __init__(self):
        self.navbar = [("/",u"首页"),("#",u"日历"),("#",u"客户管理"),("#",u"综合管理"),("#",u"分析")]
    def refresh(self):
        self.__init__
        
# DBs
def get_db():
    connection = pymongo.Connection('localhost',27017)
    return connection['fanfan_crm']

@app.before_request
def before_request():
    g.db = get_db()
    g.settings = settings()

def auth():
    if 'name' not in session:
        return False

@app.route('/')
def hello_world():
    if auth() == False:
        return redirect(url_for('login'))
    return r_t('index.html',navbar_n=0)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return r_t('login.html')
    else:
        username = request.form['username']
        passwd = hashlib.md5(request.form['passwd']).hexdigest()
        u = g.db['users'].find_one({"username":username,"passwd":passwd})
        if u:
            session['id'] = u['_id']
            session['name'] = u['name']
            session['type'] = u['type']
            return 'yes'
        else:
            return "no"
@app.route('/logout')
def logout():
    session.clear()
    return "Logout"

if __name__ == '__main__':
    app.run(debug=True)