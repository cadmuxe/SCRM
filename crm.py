#-*- coding:utf-8 -*-
from flask import Flask, g, request, session, redirect, url_for, jsonify
from flask import render_template as r_t
import pymongo, hashlib, json, random
from bson import BSON, json_util

app = Flask(__name__)
app.secret_key = 'SDFsdf@#$sddf34nsSSWD3422^oiudf%sfwdsfsDSFAS'

# settings
class settings():
    def __init__(self):
        self.navbar = [("/",u"首页"),("#",u"日历"),("/customer",u"客户管理"),("#",u"综合管理"),("#",u"分析")]
    def refresh(self):
        self.__init__
        
# DBs
# Every request has a g.db object
# collection = g.db['test-collection']
def get_db():
    connection = pymongo.Connection('localhost',27017)
    return connection['fanfan_crm']
def db_customer_add(customer):
    print type(customer)
    db = get_db()
    customer_id = db.customer.insert(customer)
    if customer["birthday"] != "0":
        birthday = {"type":"birthday",
                "user_id":customer_id,
                "title":customer["name"]+u"的生日",
                "allDay":"false",
                "start":customer["birthday"],
                "end":0,
                "repeat":"1y",
                "remind":0,
                "editable":"false",
                "remark":""
                }
        birthday_id = db.cal.insert(birthday)
        db.customer.update({"_id":customer_id},{"$set": {"birthday": birthday_id}})
    return customer_id

# helps
def get_pure_dic(bson):
# convert bson object to python dic (mainly the id object)
    if bson.has_key('_id'):
        id = bson.pop('_id')
        bson['_id'] = str(id)
    return bson

def myjsonify(dic):
    return json.dumps( get_pure_dic(dic) )
    #return json.dumps(dic,default=json_util.default,ensure_ascii=False)
    
def print_dict(dic):
    for i in dic:
        print i + " : " + dic[i] + "\n"


@app.before_request
def before_request():
    g.db = get_db()
    g.settings = settings()
    g.myjsonify = myjsonify
    g.get_pure_dic = get_pure_dic

def auth():
    if 'name' not in session:
        return False

# JSON API
@app.route('/api/<type>/<action>',methods=['GET','POST'])
def api(type,action):
    a = g.db["settings"].find_one({"type":"sector"})
    return myjsonify(a)

@app.route('/api/customer/token')
def api_customer_token():
    return "hi"

@app.route('/api/customer/add',methods=['POST'])
def api_customer_add():
    if request.method == 'POST':
        customer = request.json
        db_customer_add(customer) 
        return str(customer)
    return "ok"


@app.route('/')
def home():
    if auth() == False:
        return redirect(url_for('login'))
    return r_t('index.html',navbar_n=0)

# Customer
@app.route('/customer')
def customer_list():
    return r_t('customer_list.html')

@app.route('/customer/<id>')
def customer(id):
    return r_t('customer.html')

@app.route('/customer_add',methods=['GET','POST'])
def customer_add():
    if request.method == 'GET':
        return r_t('customer_add.html')
    else:
        print request.data
        return "go"

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return r_t('login.html')
    else:
        username = request.form['username']
        passwd = hashlib.md5(request.form['passwd']).hexdigest()
        u = g.db['users'].find_one({"username":username,"passwd":passwd})
        u = get_pure_dic(u)
        if u:
            session['_id'] = u['_id']
            session['name'] = u['name']
            session['type'] = u['type']
            return redirect(url_for('home'))
        else:
            return "no"
@app.route('/print_info')
def print_info():
    str = session['_id']
    return str

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
