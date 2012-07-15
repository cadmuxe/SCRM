#-*- coding:utf-8 -*-
from flask import Flask, g, request, session, redirect, url_for, jsonify
from flask import render_template as r_t
import pymongo, hashlib, json, random
from bson.objectid import ObjectId
import dbs,uti


app = Flask(__name__)
app.secret_key = 'SDFsdf@#$sddf34nsSSWD3422^oiudf%sfwdsfsDSFAS'

# settings
class settings():
    def __init__(self):
        self.navbar = [("/",u"首页"),("/cal",u"日历"),("/customer",u"客户管理"),("#",u"综合管理"),("#",u"分析")]
    def refresh(self):
        self.__init__()



@app.before_request
def before_request():
    g.settings = settings()
    g.myjsonify = uti.myjsonify
    g.dbs = dbs

def auth():
    if 'name' not in session:
        return False

# JSON API
@app.route('/api/<type>/<action>',methods=['GET','POST'])
def api(type,action):
    a = g.db["settings"].find_one({"type":"sector"})
    return uti.myjsonify(a)

@app.route('/api/tags/<tag_type>/<tag_name>/<action>/',methods=['GET'])
def api_tags(tag_type,tag_name,action):
    if action == 'add':
        dbs.tags(tag_type).add_tag(tag_name)
        return "OK"

@app.route('/api/customer/<query>')
def api_customer_token(query):
    return "hi"

@app.route('/api/customer/add',methods=['POST'])
def api_customer_add():
    if request.method == 'POST':
        customer = dbs.customer(request.json)
        customer.save()
        if customer["birthday"] != "0":
            customer.insert_birthday(customer["birthday"]).save()
        return str(customer)
    return "ok"

@app.route('/api/cal/save',methods=['POST'])
def api_cal_add():
    if request.method == 'POST':
        dbs.cal(request.json).save()
        print request.json
    return "ok"

@app.route("/api/cal",methods=['GET'])
def api_cal():
    start = request.args.get('start')
    end = request.args.get('end')
    clist = dbs.cal.objects.find_by_period(start,end)
    cclist = []
    for c in clist:
        cclist.append({'id':c["_id"],"title":c['title'],'start':c["start"],'end':c["end"]})
    return uti.myjsonify(cclist)
@app.route("/api/memorial",methods=['GET'])
def api_memorial():
    start = request.args.get('start')
    end = request.args.get('end')
    mlist = dbs.memorial.objects.find_by_period(start,end)
    mmlist = []
    for m in mlist:
        mmlist.append({'id':m["_id"],"title":m['title'],'start':m["this_year_start"]})
    return uti.myjsonify(mmlist)

@app.route('/api/customer/list',methods=['POST'])
def api_customer_list():
    if request.method == 'POST':
        each_page = 10              # how many items in each page
        page_now = request.form['page']
        list = dbs.customer.objects.search({"manager":ObjectId(session['_id'])},
                request.form['query'],
                ["name","type","gender","company","sector","vocation"],
                )
        total = list.count()
        p = total %10
        if p == 0:
            pages = total/10
        else:
            pages = total/10 +1
        if page_now > pages:
            page_now =pages
        if page_now < 1:
            page_now =1
        list= list.skip((page_now-1)*each_page).limit(each_page)
        if pages == 0:
            now = 0
            noww = 0
        else:
            now = (page_now-1)*each_page+1
            noww = (page_now-1)*each_page + len(list)

        r = {"total":total,"now":str(now)+'-'+str(noww),"pages":pages,"page_now":page_now,
             "list":list.get_readable_python(["_id","name","type","gender","company","sector","vocation","amount","contact_record"]) }
        print r
        return uti.myjsonify(r)

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

@app.route('/customer/<uid>')
def customer(uid):

    customer = dbs.customer(uid).get_readable_python()
    contacts =dbs.cal.objects.find_by_attend(uid).get_readable_python()
    contracts = dbs.contract.objects.find_by_customer_id(uid).get_readable_python()


    return r_t('customer.html',customer=customer,
        contacts=contacts,
        contracts=contracts,
    )

@app.route('/customer_add',methods=['GET','POST'])
def customer_add():
    if request.method == 'GET':
        customer_id_list = dbs.get_json_customer_and_id_list()
        return r_t('customer_add.html',customer_id_list = customer_id_list)
    else:
        print request.data
        return "go"

@app.route('/cal',methods=['GET'])
def cal():
    return r_t('cal.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return r_t('login.html')
    else:
        username = request.form['username']
        passwd = hashlib.md5(request.form['passwd']).hexdigest()
        u = dbs.db['users'].find_one({"username":username,"passwd":passwd})
        u = uti.get_pure_dict(u)
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