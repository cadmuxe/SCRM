#-*- coding:utf-8 -*-
import pymongo, myjson_util, json, pymongo.cursor,time
from bson.objectid import ObjectId
import uti,calendar,datetime,copy

def get_db():
    """return 'fanfan_crm' db
    """
    con = pymongo.Connection('localhost',27017)["fanfan_crm"]
    print id(con)
    return con

db = get_db()

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
    def __init__(self,collection,oset=[]):
        self.__collection = collection
        self.__sets = []
        self.__doc_class = globals()[collection]
        if type(oset) == pymongo.cursor.Cursor:
            for i in oset:
                self.__sets.append(self.__doc_class(i))
        else:
            self.__sets = oset

    def enlargeSet(self,document):
        if isinstance(document,self.__doc_class) == False:
            raise ValueError
        else:
            self.__sets.append(document)
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
        elif d is None:
            raise ValueError
        else:
            try:
                self._doc = db[self._collection].find_one({"_id":ObjectId(d)})
                if self._doc is None:
                    self._doc = {"doc":"NONE"}
            except:
                print "Error"
                raise ValueError
        self.__python_helper={}

    def save(self):
        if self._doc.has_key("_id"):
            self.calculate()
            db[self._collection].save(self._doc)
        else:
            db[self._collection].save(self._doc)
            self.save()
        return self
    def delete(self):
        return db[self._collection].remove(self._doc)
    def reload(self):
        self._doc = db[self._collection].find_one({"_id":ObjectId(self._doc["_id"])})
        self.calculate()
        return self
    def validate(self):
        """
        only used for debugging
        """
        raise ValueError

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
        raise ValueError

    def __iter__(self):
        return iter(self._doc)
    def __str__(self):
        return "%s : ObjectId(%s)" % (self._collection,str(self._doc["_id"]))
    def __getitem__(self, item):
        return self._doc[item]
    def __setitem__(self, key, value):
        self._doc[key] = value

class BaseQuery():
    _collection = ""
    def find(self,query={}):
        """
        """
        sets_mongo_cursor = db[self._collection].find(query)
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
        print query
        return  self.find(query)

class customerQuery(BaseQuery):
    def __init__(self):
        self._collection = "customer"

    def not_contact_list(self):
        cursor = db[self._collection].find({"how_long":{"$gte":10}}).sort("how_long",pymongo.DESCENDING)
        return querySet(self._collection,cursor)

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
        search_helper_start =  start.replace(year = datetime.datetime.today().year)
        search_helper_end = end.replace(year = datetime.datetime.today().year)
        cursor = db[self._collection].find({"this_year_start":
                                                    {"$gte":search_helper_start,"$lte":search_helper_end}})
        set = querySet(self._collection)
        for i in cursor:
            mm = memorial(i)
            mm.set_calculate_year(start.year)
            set.enlargeSet(mm)
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
        self.save()

    def __get_customer_total_contract_amount(self):
        """ get customer's totally contract amount
        """
        amount = 0
        list = db["contract"].find({"user_id":self._doc["_id"]})
        for c in list:
            amount += int(c["amount"])
        return amount
    def calculate(self):
        if self._doc.has_key('_id') == False:
            self.save()
        self._doc["amount"] = self.__get_customer_total_contract_amount()
        try:
            contact_record = db['cal'].find({"attend._id":self._doc['_id'],"type":u"事务"}).sort("start", pymongo.DESCENDING)[0]
            print contact_record["_id"]
            self._doc["contact_record"] = {"_id":contact_record["_id"],
                                           "date":uti.time_datetime_to_string_date(contact_record["start"])}
        except:
            self._doc["contact_record"]={}
        if self._doc["contact_record"] !={}:
            start = cal(self._doc["contact_record"]["_id"])["start"]
            self._doc["how_long"] = (datetime.datetime.today() - start).days
        else:
            self._doc["contact_record"] = {'_id':None,'date':u"无联络信息"}
            self._doc["how_long"] = 10000
        return self


class cal(BaseDocument):
    objects = calQuery()
    def __init__(self,c):
        self._collection = "cal"
        super(cal,self).__init__(c)

    def calculate(self):
        l=[]
        if self._doc.has_key("attend"):
            for i in self._doc['attend']:
                i['name'] = db['customer'].find_one(i['_id'])['name']

class memorial(BaseDocument):
    objects = memorialQuery()
    def __init__(self,c):
        self._collection = "memorial"
        self.__this_year = 0
        super(memorial,self).__init__(c)

    def set_calculate_year(self,year):
        self.__this_year = year
        self.calculate()
    def calculate(self):
        if self.__this_year == 0:
            self.__this_year = datetime.datetime.today().year
        d = self._doc["start"].replace(year = self.__this_year)
        self._doc["this_year_start"] = d

class contract(BaseDocument):
    objects = contractQuery()
    def __init__(self,c):
        self._collection = "contract"
        super(contract,self).__init__(c)

    def calculate(self):
        if project.objects.find_by_project_name(self._doc['contract_project']) == False:
            project({'project_name':self._doc['contract_project'],"working":True}).save()


class project(BaseDocument):
    objects = projectQuery()
    def __init__(self,p):
        self._collection = "project"
        super(project,self).__init__(p)
    def calculate(self):
        pass
