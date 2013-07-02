#-*- coding:utf-8 -*-
import pymongo, myjson_util, json, pymongo.cursor,time
from bson.objectid import ObjectId
import uti,calendar,datetime,copy,re

def get_db():
    """return 'fanfan_crm' db
    """
    con = pymongo.Connection('localhost',27017)["crm_demo"]
    return con

db = get_db()

def get_json_customer_list():
    list = db["customer"].find({},{'name':1})
    l = []
    for c in list:
        l.append(c["name"])
    same=[]
    for i in range(len(l)):
        for j in l[i+1:]:
            if l[i] == j:
                try:
                    same.index(l[i])
                except ValueError:
                    same.append(l[i])
    if len(same) == 0:
        return uti.myjsonify(l)
    else:
        for i in same:
            while True:
                try:
                    l.remove(i)
                except ValueError:
                    break
            namel = customer.objects.find_contact_namei_list_by_name(i)
            for i in namel:
                l.append(i)
        return uti.myjsonify(l)
def get_json_customer_and_id_list():
    list = db["customer"].find({},{'_id':1,'name':1})
    l = []
    for c in list:
        l.append({'name':c["name"],'_id':c["_id"]})
    return uti.myjsonify(l)


def get_json_working_project_list():
    list = project.objects.get_working_project_list().get_python(['project_name'])
    l =[]
    for i in list:
        l.append(i['project_name'])
    return uti.myjsonify(l)

def get_json_time_period():
    t = datetime.datetime.today()
    tt = datetime.datetime(t.year,t.month,t.day).timetuple()
    today = (int(time.mktime(tt)))
    return {'today':(today, today + 86400),'tomorrow':(today + 86400, today + 172800)}
def get_datetime_period():
    t = datetime.datetime.today()
    delta = datetime.timedelta(1)
    t1 = datetime.datetime(t.year,t.month,t.day)
    t2 = t1+delta
    t3 = t2+delta
    return {'today':(t1, t2),'tomorrow':(t2, t3)}
def get_datetime_from_stamp(s):
    s = int(s)
    t = time.localtime(s)
    d = datetime.datetime(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
    return d



class tags:
    """
    self.__o is the original mongo object
    """
    def __init__(self,type):
        self.__o = db["settings"].find_one({"type":type})
        if type == "sector":
            self.__search = {'collection':'customer','field':'sector'}
        elif type == "project_sector":
            self.__search = {'collection':'project','field':'project_sector'}
            self.__o = db["settings"].find_one({"type":'sector'})
        elif type == 'vocation':
            self.__search = {'collection':'customer','field':'vocation'}
        elif type == 'likes':
            self.__search = {'collection':'customer','field':'likes'}
        elif type == 'relation_h':
            self.__search = {'collection':'customer','field':'relevance_people.relation'}
        elif type == 'relation_s':
            self.__search = {'collection':'customer','field':'social.relation'}
        elif type == 'channel':
            self.__search = {'collection':'customer','field':'channel.channel'}
        elif type == 'customer':
            self.__search = {'collection':'customer','field':'tags'}
        elif type == 'cal_type':
            self.__search = {'collection':'cal','field':'cal_type'}
        elif type == 'cal_tags':
            self.__search = {'collection':'cal','field':'tags'}
        elif type == 'contact_type':
            self.__search = {'collection':'cal','field':'contact_type'}
        else:
            raise ValueError
    def get_tags(self):
        return self.__o["value"]

    def get_tags_string(self):
        '''
        return tags string,  "tag1 tag2 tag3..."
        '''
        s=''
        for item in self.__o['value']:
            s+=(' '+item)
        return s
    def set_tags_string(self,s):
        '''
        set tags by sting  s:  "tag1 tag2"
        '''
        l=s.strip().split(' ')
        self.__o['value'] =[]
        for i in l:
            if i == '':
                continue
            self.__o['value'].append(i.strip())
        return self.__save()
    def get_count_of_one_tag(self,tag_name):
        return db[self.__search['collection']].find({self.__search['field']:tag_name}).count()
    def get_count_of_tags(self):
        l = []
        for t in self.__o["value"]:
            l.append({'tag':i,'count':self.get_count_of_one_tag(i)})
        return l
    def __save(self):
        return db["settings"].save(self.__o)
    def add_tag(self,tag):
        try:
            self.__o["value"].index(tag)
        except ValueError:
            self.__o["value"].append(tag)
        return self.__save()
    def remove_tag(self,tag_name,sure):
        if sure == "i am sure":
            db[self.__search['collection']].update({self.__search['field']:tag_name},{"$pull":{self.__search['field']:tag_name}})
            self.__o["value"].remove(tag_name)
            self.__save()
        else:
            raise ValueError
    def rename(self,tag,new_name):
        db[self.__search['collection']].update({self.__search['field']:tag_name},{"$push":{self.__search['field']:new_name}})
        db[self.__search['collection']].update({self.__search['field']:tag_name},{"$pull":{self.__search['field']:tag}})
        self.__o["value"].remove(tag)
        self.__o["value"].append(new_name)
        return self.__save()

    def get_json(self):
        return json.dumps(self.__o["value"],default=myjson_util.default)



class querySet:
    def __init__(self,collection, o_set=[]):
        self.__collection = collection
        self.__sets = []
        self.__doc_class = globals()[collection]
        if type(o_set) == pymongo.cursor.Cursor:
            for i in o_set:
                self.__sets.append(self.__doc_class(i))
        else:
            self.__sets = o_set

    def enlargeSet(self,documents):
        if isinstance(documents,pymongo.cursor.Cursor):
            for i in documents:
                self.__sets.append(self.__doc_class(i))
        return self
    def count(self):
        return len(self.__sets)

    def get_python(self,selection=[]):
        self.__python_helper =[]
        for i in self.__sets:
            self.__python_helper.append(i.get_python(selection))
        return self.__python_helper

    def skip(self,num):
        return querySet(self.__collection,self.__sets[num:])
    def limit(self,num):
        return querySet(self.__collection,self.__sets[:num])
    def __len__(self):
        return len(self.__sets)
    def __iter__(self):
        return iter(self.__sets)
    def __str__(self):
        pass
    def __getitem__(self, item):
        return self.__sets[item]


def if_in_list(l,str):
    try:
        l.index(str)
        return True
    except:
        return False

class BaseDocument(object):
    _collection =""
    _doc ={}
    def __init__(self,d):
        if type(d) == dict:
            self._doc = myjson_util.object_hook(d)
        elif d is ObjectId:
            self._doc = db[self._collection].find_one({"_id":ObjectId(d)})
        elif (type(d) == unicode) or (type(d) == str):
            self._doc = db[self._collection].find_one({"_id":ObjectId(d)})
        elif d is None:
            raise ValueError
        else:
            try:
                self._doc = db[self._collection].find_one({"_id":ObjectId(d)})
                if self._doc is None:
                    raise ValueError
            except:
                raise ValueError

        self.__python_helper={}

    def save(self):
        db[self._collection].save(self._doc)
        return self
    def delete(self):
        return db[self._collection].remove(self._doc)
    def reload(self):
        self._doc = db[self._collection].find_one({"_id":ObjectId(self._doc["_id"])})
        return self
    def validate(self):
        """
        only used for debugging
        """
        raise ValueError
    def update(self):
        self.save()
        self.calculate()
        return self.save()

    def get_python(self,selection=[]):
        if selection == []:
            selection =  self._doc.keys()
        for field in selection:
            try:
                self.__python_helper[field]=self._doc[field]
            except :
                self.__python_helper[field]= None
        return self.__python_helper

    def calculate(self):
        if self._doc.has_key('_id') == False:
            self.save()
        return self

    def __iter__(self):
        return iter(self._doc)
    def __str__(self):
        return "%s : ObjectId(%s)" % (self._collection,str(self._doc["_id"]))
    def __getitem__(self, item):
        try:
            return self._doc[item]
        except KeyError:
            return ""
    def __setitem__(self, key, value):
        self._doc[key] = value

class BaseQuery():
    _collection = ""
    def find(self,query={}):
        """
        """
        sets_mongo_cursor = db[self._collection].find(query).sort('_id',pymongo.DESCENDING)
        return querySet(self._collection,sets_mongo_cursor)

    def search(self,query,keys="",field_search=[]):
        """ search collection with queries in fields
        query:      pymongo style query,
        selection:  pymongo style selection
        field_search:    ["name","company"..] field to be searched
        dbs.customer_find({"manager":session['_id'],"$and":[{"$or":[{field:{"regex":"key"}}]}]},
                    {'_id':1,'name':1,'type':1,'gender':1,"company":1,"sector":1,"vocation":1,..})
        same as the g.db["customer"].find()
        """
        if keys != "" or field_search !=[]:
            q_or=[]
            q_and=[]
            keys = keys.split(' ')
            for k in keys:
                k = '.*'+k+'.*'
                q_or =[]
                for  f in field_search:
                    q_or.append({f:{"$regex":k}})
                q_and.append({'$or':q_or})
            query["$and"]= q_and
        return  self.find(query)

class customerQuery(BaseQuery):
    def __init__(self):
        self._collection = "customer"

    def not_contact_list(self):
        today = datetime.datetime.today()
        date_diff = datetime.timedelta(days=10)
        query_day = today - date_diff
        cursor = db[self._collection].find({"contact_record.date":''})
        qS = querySet(self._collection,cursor)
        cursor = db[self._collection].find({"contact_record.date":{"$lt":query_day}}).sort("contact_record.date",pymongo.ASCENDING).limit(15)
        qS.enlargeSet(cursor)
        return qS
    def find_contact_namei_list_by_name(self,name):
        cl = db[self._collection].find({"name":name})
        list = []
        for i in cl:
            c =customer(i)
            list.append(c.get_namei())
        return list

    def find_by_namei(self,namei):
        if namei.find('(') == -1:
            return self._find_by_name(namei)
        else:
            m = re.match(r".*\((.*)\)",namei)
            st = m.group(1)
            if st.find('@') == -1:
                return self._find_by_phone(st)
            else:
                return self._find_by_email(st)
        raise ValueError

    def _find_by_name(self,name):
        c = db[self._collection].find_one({"name":name})
        return customer(c)
    def _find_by_phone(self,phone):
        c = db[self._collection].find_one({"$or":[{"phone.work":phone},{"phone.personal":phone},{"phone.home":phone}]})
        return customer(c)
    def _find_by_email(self,email):
        c = db[self._collection].find_one({"$or":[{"email.work":email},{"email.personal":email}]})
        return customer(c)


class calQuery(BaseQuery):
    def __init__(self):
        self._collection = "cal"

    def find_by_attend(self,uid):
        cursor = db[self._collection].find({"attend._id":ObjectId(uid),"type":u"事务"}).sort("start", pymongo.DESCENDING)
        return querySet(self._collection,cursor)
    def find_by_period(self,start,end):
        """
        start, end : datetime type
        """
        cursor = db[self._collection].find({"start":{"$gte":start,"$lte":end},"type":u"事务"}).sort("start", pymongo.DESCENDING)
        return querySet(self._collection,cursor)

    def find_by_period_ascend(self,start,end):
        """
        start, end : datetime type
        """
        cursor = db[self._collection].find({"start":{"$gte":start,"$lte":end},"type":u"事务"}).sort("start", pymongo.ASCENDING)
        not_done = db[self._collection].find({"start":{"$gte":start,"$lte":end},"type":u"事务","finished":False}).count()
        return (not_done,querySet(self._collection,cursor))


class memorialQuery(BaseQuery):
    def __init__(self):
        self._collection = "memorial"
    def find_by_uid(self,uid):
        cursor = db[self._collection].find({"user_id":ObjectId(uid)})
        return querySet(self._collection,cursor)
    def find_by_period(self,start,end):
        """
        start, end datetime type
        """
        search_helper_start =  start.replace(year = 1901)
        search_helper_end = end.replace(year = 1901)
        cursor = db[self._collection].find({"search_helper":
                                                    {"$gte":search_helper_start,"$lte":search_helper_end}})
        set = []
        for i in cursor:
            mm = memorial(i)
            mm.set_calculate_year(start.year)
            set.append(mm)
        return set

class contractQuery(BaseQuery):
    def __init__(self):
        self._collection = "contract"
    def find_by_customer_id(self,uid):
        cursor = db[self._collection].find({"user_id":ObjectId(uid)})
        return querySet(self._collection,cursor)

class projectQuery(BaseQuery):
    def __init__(self):
        self._collection = 'project'
    def get_working_project_list(self):
        cursor = db[self._collection].find({'working':True})
        return querySet(self._collection,cursor)
    def find_by_project_name(self,project_name):
        p = db[self._collection].find_one({'project_name':project_name})
        try:
            return project(p)
        except :
            return False

class customer(BaseDocument):
    objects = customerQuery()
    def __init__(self,d):
        self._collection = "customer"
        super(customer,self).__init__(d)

    def calculate(self):
        if self._doc.has_key('_id') == False:
            self.save()
        self._c_birthday()
        self._c_amount()
        self._c_contact()
        return self
    def get_namei(self):
        if self._doc['email']['personal'] !="":
            return self._doc['name'] + '(' + self._doc['email']['personal'] +')'
        if self._doc['email']['work'] !="":
            return self._doc['name'] + '(' + self._doc['email']['work'] +')'
        if self._doc['phone']['personal'] !="":
            return self._doc['name'] + '(' + self._doc['phone']['personal'] +')'
        if self._doc['phone']['work'] !="":
            return self._doc['name'] + '(' + self._doc['phone']['work'] +')'
        if self._doc['phone']['home'] !="":
            return self._doc['name'] + '(' + self._doc['phone']['home'] +')'
        return self._doc['name']

    def _c_amount(self):
        amount = 0
        list = db["contract"].find({"user_id":self._doc["_id"]})
        for c in list:
            amount += int(c["amount"])
        self._doc["amount"] = amount
        return
    def _c_contact(self):
        try:
            c = db['cal'].find({"attend._id":self._doc['_id'],"type":u"事务"}).sort("start", pymongo.DESCENDING)[0]
        except:
            c = None
        if c == None:
            self._doc["contact_record"] = {'_id':'','date':''}
        else:
            self._doc["contact_record"] = {"_id":c["_id"],
                                           "date":c["start"]}
        return
    def _c_birthday(self):
        if not self._doc["birthday"].has_key('date'):
            return
        date = self._doc["birthday"]["date"].strip()
        if date == '':
            return
        d = date.split('-')
        if len(d) == 3:
            year = d[0]
            month = d[1]
            day = d[2]
            b = year + '-' + month + '-' + day
        elif len(d) == 2:
            year = 1900
            month = d[0]
            day = d[1]
            b = month + '-' + day
        else:
            return
        t = datetime.datetime(int(year),int(month),int(day))

        if self._doc['birthday'].has_key('_id'):
            try:
                m = memorial(self._doc['birthday']['_id'])
                m['title'] = self._doc["name"]+u"的生日"
                m['start'] = t
                m.update()
                self._doc["birthday"] = {"_id":m['_id'],"date":b}
                return
            except:
                pass
        birthday = {"type":"birthday",
                    "user_id":self._doc["_id"],
                    "title":self._doc["name"]+u"的生日",
                    "allDay":"false",
                    "start":t,
                    "end":0,
                    "editable":"false",
                    "remark":""
        }
        m = memorial(birthday).update()
        self._doc["birthday"] = {"_id":m['_id'],"date":b}
        return




class cal(BaseDocument):
    objects = calQuery()
    def __init__(self,c):
        self._collection = "cal"
        super(cal,self).__init__(c)
    def calculate(self):
        if self._doc.has_key('_id') == False:
            self.save()
        for i in self._doc["attend"]:
            customer(i['_id']).update()
        return self

class memorial(BaseDocument):
    objects = memorialQuery()
    def __init__(self,c):
        self._collection = "memorial"
        self.__this_year = 0
        super(memorial,self).__init__(c)

    def set_calculate_year(self,year):
        d = self._doc["start"].replace(year = year)
        self._doc["this_year_start"] = d
    def _c_search_helper(self):
        d = self._doc["start"].replace(year = 1901)
        self._doc["search_helper"] = d
    def _c_title(self):
        if self._doc['type'] =='birthday':
            user = customer(self._doc['user_id'])
            self._doc['title'] = user['name'] + u'的生日'
    def calculate(self):
        if self._doc.has_key('_id') == False:
            self.save()
        self._c_search_helper()
        self._c_title()
        return self

class contract(BaseDocument):
    objects = contractQuery()
    def __init__(self,c):
        self._collection = "contract"
        super(contract,self).__init__(c)

    def calculate(self):
        if self._doc.has_key('_id') == False:
            self.save()
        self._c_project()
        self._c_customer_amount()
        return self

    def _c_project(self):
        p =  project.objects.find_by_project_name(self._doc['contract_project']['name'])
        if p == False:
            p = project({'project_name':self._doc['contract_project']['name'],"working":True}).save()
        self._doc['contract_project']['_id'] = p['_id']
    def _c_customer_amount(self):
        c = customer(self._doc['user_id']).update()


class project(BaseDocument):
    objects = projectQuery()
    def __init__(self,p):
        self._collection = "project"
        super(project,self).__init__(p)
