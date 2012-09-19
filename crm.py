#-*- coding:utf-8 -*-
from flask import Flask, g, request, session, redirect, url_for, jsonify
from flask import render_template as r_t
import pymongo, hashlib, json, random,time,datetime
from bson.objectid import ObjectId
import dbs,uti
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)
app.secret_key = 'SDFsdf@#$sddf34nsSSWD3422^oiudf%sfwdsfsDSFAS'



# Jinja Filters
@app.template_filter('date')
def filter_convert_datetime_to_string_date(t):
    if type(t) == datetime.datetime:
        return uti.time_datetime_to_string_date(t)
    elif type(t) == str or type(t) ==unicode:
        return t.split(' ')[0]

@app.template_filter('time')
def filter_convert_datetime_to_string_time(t):
    if type(t) == datetime.datetime:
        return uti.time_datetime_to_string_time(t)
    elif type(t) == str or type(t) ==unicode:
        return t.split(' ')[1]

@app.template_filter('datetime')
def filter_convert_datetime_to_string_time(t):
    if type(t) == datetime.datetime:
        return uti.time_datetime_to_string_datetime(t)
    elif type(t) == str or type(t) ==unicode:
        return t

@app.template_filter('howlong')
def filter_how_long(t):
    if int(t) == 10000:
        return u"无联络"
    else:
        return t
@app.template_filter('jsonify')
def filter_jsonify(dic):
    return uti.myjsonify(dic)










# settings
class settings():
    def __init__(self):
        self.navbar = [("/",u"首页"),("/cal",u"日历"),("/customer",u"客户管理"),("/project",u"综合管理"),("#",u"分析")]
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
    if auth() == False:
        return "not_login"
    a = g.db["settings"].find_one({"type":"sector"})
    return uti.myjsonify(a)

@app.route('/api/tags/<tag_type>/<tag_name>/<action>/',methods=['GET'])
def api_tags(tag_type,tag_name,action):
    if auth() == False:
        return "not_login"
    if action == 'add':
        dbs.tags(tag_type).add_tag(tag_name)
        return "OK"

@app.route('/api/customer/add',methods=['POST'])
def api_customer_add():
    if auth() == False:
        return "not_login"
    if request.method == 'POST':
        customer = dbs.customer(request.json)
        customer.save()
        customer.update()
    return "ok"
@app.route('/api/customer/save',methods=['POST'])
def api_customer_save():
    if auth() == False:
        return "not_login"
    if request.method == 'POST':
        i=dbs.customer(request.json).update()
    return uti.myjsonify(i['_id'])

@app.route('/api/cal/save',methods=['POST'])
def api_cal_save():
    if auth() == False:
        return "not_login"
    if request.method == 'POST':
        c=dbs.cal(request.json).save()
    return uti.myjsonify(c.get_python())


@app.route('/api/cal/<_id>/<action>',methods=['GET','POST'])
def api_cal_update(_id,action):
    if auth() == False:
        return "not_login"
    c =dbs.cal(_id)
    if action =='get':
        return uti.myjsonify(c.get_python())
    if action =='done':
        c['finished']= True
        c.update()
    if action == 'not_done':
        c['finished']= False
        c.update()
    if action == 'delete':
        c.delete()
    if action == 'drop' and request.method =='POST':
        change = request.json
        delta = datetime.timedelta(change["day"],change["minute"]*60)
        c["start"] = c["start"] + delta
        c["end"] = c["end"] +delta
        c["allDay"] = change["allDay"]
        c.update()
    if action == 'resize' and request.method =='POST':
        change = request.json
        delta = datetime.timedelta(change["day"],change["minute"]*60)
        c["end"] = c["end"] +delta
        c.update()
    return uti.myjsonify({'doc':'success'})


@app.route('/api/contract/save',methods=['POST'])
def api_contract_save():
    if auth() == False:
        return "not_login"
    if request.method == 'POST':
        i=dbs.contract(request.json).update()
    return uti.myjsonify(i['_id'])
@app.route('/api/contract/<uid>',methods=['GET'])
def api_contract_get(uid):
    if auth() == False:
        return "not_login"
    c = dbs.contract(ObjectId(uid))
    return uti.myjsonify(c.get_python())

@app.route('/api/project/save',methods=['POST'])
def api_project_save():
    if auth() == False:
        return "not_login"
    if request.method == 'POST':
        i=dbs.project(request.json).update()
    return uti.myjsonify(i['_id'])
@app.route('/api/project/<uid>',methods=['GET'])
def api_project_get(uid):
    if auth() == False:
        return "not_login"
    p = dbs.project(ObjectId(uid))
    return uti.myjsonify(p.get_python())

@app.route("/api/cal",methods=['GET'])
def api_cal():
    if auth() == False:
        return "not_login"
    start = dbs.get_datetime_from_stamp(request.args.get('start'))
    end = dbs.get_datetime_from_stamp(request.args.get('end'))
    clist = dbs.cal.objects.find_by_period(start,end)
    clist = clist.get_python()
    return uti.myjsonify(clist)

@app.route('/api/cal/<uid>',methods=['GET'])
def api_cal_get(uid):
    if auth() == False:
        return "not_login"
    c = dbs.cal(ObjectId(uid))
    return uti.myjsonify(c.get_python())

@app.route("/api/todo",methods=['GET'])
def api_todo():
    if auth() == False:
        return "not_login"
    (not_done_today,today) = dbs.cal.objects.find_by_period_ascend(dbs.get_datetime_period()['today'][0],
        dbs.get_datetime_period()['today'][1])
    today = today.get_python()

    (not_done_tomorrow,tomorrow) = dbs.cal.objects.find_by_period_ascend(dbs.get_datetime_period()['tomorrow'][0],
        dbs.get_datetime_period()['tomorrow'][1])
    tomorrow = tomorrow.get_python()

    (not_done_inbox,inbox) = dbs.cal.objects.find_by_period_ascend(datetime.datetime(2000,1,1,5,4),
        datetime.datetime(2000,1,1,5,4))
    inbox = inbox.get_python()
    all = today+tomorrow+inbox
    return uti.myjsonify(all)

@app.route("/api/memorial",methods=['GET'])
def api_memorial():
    if auth() == False:
        return "not_login"
    start = dbs.get_datetime_from_stamp(request.args.get('start'))
    end = dbs.get_datetime_from_stamp(request.args.get('end'))
    mlist = dbs.memorial.objects.find_by_period(start,end)
    mmlist = []
    for m in mlist:
        mmlist.append({'_id':m["_id"],"title":m['title'],'start':m["this_year_start"]})

    return uti.myjsonify(mmlist)

@app.route('/api/customer/list',methods=['POST'])
def api_customer_list():
    if auth() == False:
        return "not_login"
    if request.method == 'POST':
        each_page = 10              # how many items in each page
        page_now = int(request.form['page'])
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
             "list":list.get_python(["_id","name","type","gender","company","sector","vocation","amount","contact_record"]) }
        return uti.myjsonify(r)

    return "ok"
@app.route('/api/customer/contact_list',methods=['GET'])
def api_customer_contact_list():
    if auth() == False:
        return "not_login"
    if request.method == 'GET':
        list = dbs.customer.objects.not_contact_list()
        r = list.get_python(["_id","name","type","gender","company","amount","contact_record","how_long"])
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
    if auth() == False:
        return redirect(url_for('login'))
    return r_t('customer_list.html')

@app.route('/customer/<uid>')
def customer(uid):
    if auth() == False:
        return redirect(url_for('login'))
    customer = dbs.customer(uid).get_python()
    contacts =dbs.cal.objects.find_by_attend(uid).get_python()
    contracts = dbs.contract.objects.find_by_customer_id(uid).get_python()


    return r_t('customer.html',customer=customer,
        contacts=contacts,
        contracts=contracts,
    )

@app.route('/customer_add',methods=['GET','POST'])
def customer_add():
    if auth() == False:
        return redirect(url_for('login'))
    if request.method == 'GET':
        customer_id_list = dbs.get_json_customer_and_id_list()
        return r_t('customer_item.html',customer_id_list = customer_id_list,nav=u"增加客户")
    else:
        return "go"

@app.route('/customer/edit/<uid>')
def customer_edit(uid):
    if auth() == False:
        return redirect(url_for('login'))
    if request.method == 'GET':
        customer = dbs.customer(uid).get_python()
        customer_id_list = dbs.get_json_customer_and_id_list()
        return r_t('customer_item_edit.html',customer = customer,customer_id_list = customer_id_list)
    else:
        return "go"

@app.route('/cal',methods=['GET'])
def cal():
    if auth() == False:
        return redirect(url_for('login'))
    return r_t('cal.html')

@app.route('/project',methods=['GET'])
def project():
    if auth() == False:
        return redirect(url_for('login'))
    project_list = dbs.project.objects.find({})
    return r_t('project.html',project_list = project_list)

@app.route('/settingss',methods=['GET','POST'])
def settingss():
    if auth() == False:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return r_t('settings.html')
    else:
        relation_h = request.form['relation_h']
        relation_s = request.form['relation_s']
        channel = request.form['channel']
        contact_type = request.form['contact_type']

        dbs.tags('relation_h').set_tags_string(relation_h)
        dbs.tags('relation_s').set_tags_string(relation_s)
        dbs.tags('channel').set_tags_string(channel)
        dbs.tags('contact_type').set_tags_string(contact_type)

        return redirect(url_for('settingss'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return r_t('login.html')
    else:
        username = request.form['username']
        passwd = hashlib.md5(request.form['passwd']).hexdigest()
        u = dbs.db['users'].find_one({"username":username,"passwd":passwd})
        if u:
            session['_id'] = u['_id']
            session['name'] = u['name']
            session['type'] = u['type']
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
@app.route('/print_info')
def print_info():
    if auth() == False:
        return redirect(url_for('login'))
    str = session['_id']
    return str

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    #http_server = HTTPServer(WSGIContainer(app))
    #http_server.listen(5000)
    #IOLoop.instance().start()