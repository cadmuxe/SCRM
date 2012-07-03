#-*- coding:utf-8 -*-
import pymongo, myjson_util, json, pymongo.cursor,time
from bson.objectid import ObjectId
import uti

def get_db():
    """return 'fanfan_crm' db
    """
    return pymongo.Connection('localhost',27017)["fanfan_crm"]

db = get_db()

def get_json_customer_and_id_list():
    list = db["customer"].find({},{'_id':1,'name':1})
    l = []
    for c in list:
        l.append({'name':c["name"],'id':c["_id"]})
    return uti.myjsonify(l)


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

def mongo_find(col,query, selection={},keys="",field_search=[]):
    """ search collection with queries in fields
    collection: collection to be searched
    query:      pymongo style query,
    selection:  pymongo style selection
    field_search:    ["name","company"..] field to be searched
    dbs.customer_find({"manager":session['_id'],"$or":query,..},
                {'_id':1,'name':1,'type':1,'gender':1,"company":1,"sector":1,"vocation":1,..})
    same as the g.db["customer"].find()
    """
    if keys != "" or field_search !=[]:
        q_or=[]
        keys = keys.split(' ')
        for k in keys:
            k = '.*'+k+'.*'
            for  f in field_search:
                q_or.append({f:{"$regex":k}})
        query["$or"]= q_or
    if selection =={}:
        return col.find(query)
    else:
        return col.find(query,selection)


class querySet:
    def __init__(self,collection,oset):
        self.__collection = collection
        self.__sets = []
        self.__doc_class = globals()[collection]
        if type(oset) == pymongo.cursor.Cursor:
            for i in oset:
                self.__sets.append(self.__doc_class(i))
        else:
            self.__sets = oset

    def enlargeSet(self,set):
        self.__sets += set
    def count(self):
        return len(self.__sets)
    def get_json(self,selection=[]):
        self.__json_helper =[]
        for i in self.__sets:
            self.__json_helper.append(i.get_python(selection))
        return json.dumps(self.__json_helper,default=myjson_util.default)

    def get_python(self,selection=[]):
        self.__json_helper =[]
        for i in self.__sets:
            self.__json_helper.append(i.get_python(selection))
        return self.__json_helper

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
    _json_helper={}
    def __init__(self,d):
        if type(d) == dict:
            self._doc = d
        else:
            try:
                self._doc = db[self._collection].find_one({"_id":ObjectId(d)})
            except:
                print "Error"
                raise ValueError
        self.calculate()
    def save(self):
        return db[self._collection].save(self._doc)
    def delete(self):
        return db[self._collection].remove(self._doc)
    def reload(self):
        self._doc = db[self._collection].find_one({"_id":ObjectId(self._doc["_id"])})
        self.calculate()
        return self._doc["_id"]
    def validate(self):
        raise ValueError
    def _selector_helper(self,selection):
        """
        为输出的json 添加，修改各字段值
        """
        return selection
    def __selector(self,selection):
        if selection == []:
            selection =  self._doc.keys()
        selection = self._selector_helper(selection)
        for field in selection:
            self._json_helper[field]=self._doc[field]
    def get_json(self,selection=[]):
        """
        """
        self.__selector(selection)
        return json.dumps(self._json_helper,default=myjson_util.default)
    def get_python(self,selection=[]):
        self.__selector(selection)
        return self._json_helper

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
        dbs.customer_find({"manager":session['_id'],"$or":query,..},
                    {'_id':1,'name':1,'type':1,'gender':1,"company":1,"sector":1,"vocation":1,..})
        same as the g.db["customer"].find()
        """
        if keys != "" or field_search !=[]:
            q_or=[]
            keys = keys.split(' ')
            for k in keys:
                k = '.*'+k+'.*'
                for  f in field_search:
                    q_or.append({f:{"$regex":k}})
            query["$or"]= q_or
        return  self.find(query)

class customerQuery(BaseQuery):
    def __init__(self):
        self._collection = "customer"

class calQuery(BaseQuery):
    def __init__(self):
        self._collection = "cal"

    def find_by_attend(self,uid):
        cursor = db[self._collection].find({"attend":ObjectId(uid)})
        return querySet(self._collection,cursor)
    def find_by_period(self,start,end):
        cursor = db[self._collection].find({"start":{"$gt":start,"$lt":end}})
        return querySet(self._collection,cursor)

class memorialQuery(BaseQuery):
    def __init__(self):
        self._collection = "memorial"
    def find_by_uid(self,uid):
        cursor = db[self._collection].find({"user_id":ObjectId(uid)})
        return querySet(self._collection,cursor)
    def find_by_period(self,start,end):
        cursor = db[self._collection].find({"this_year_date":{"$gt":start,"$lt":end}})
        return querySet(self._collection,cursor)

class contractQuery(BaseQuery):
    def __init__(self):
        self._collection = "contract"
    def find_by_customer_id(self,uid):
        cursor = db[self._collection].find({"user_id":ObjectId(uid)})
        return querySet(self._collection,cursor)

class customer(BaseDocument):
    objects = customerQuery()
    def __init__(self,d):
        self._collection = "customer"
        super(customer,self).__init__(d)

    def __get_customer_total_contract_amount(self):
        """ get customer's totally contract amount
        """
        amount = 0
        list = db["contract"].find({"_id":self._doc["_id"]})
        for c in list:
            amount += int(c["amount"])
        return amount

    def _selector_helper(self,selection):

        if if_in_list(selection,"contact_record"):
            if self._doc.has_key("contact_record"):
                self._json_helper["contact_record"] = cal(self._doc["contact_record"])["start_date"]
            else:
                self._json_helper["contact_record"] = u"无联络信息"
            selection.remove("contact_record")

        if if_in_list(selection,"birthday"):
            self._json_helper["birthday"] =  memorial(self._doc["birthday"])["start_date"]
            selection.remove("birthday")
        return selection
    def calculate(self):
        self._doc["amount"] = self.__get_customer_total_contract_amount()

    def insert_birthday(self,time):
        """ Insert customer to dbs, customer is a dict object
        replace the birthday with the memorial_id.
        return customer_id
        """
        if self._doc.has_key("id") == False:
            raise ValueError
        birthday = {"type":"birthday",
                    "user_id":self._doc["_id"],
                    "title":self._doc["name"]+u"的生日",
                    "allDay":"false",
                    "start":time,
                    "end":0,
                    "editable":"false",
                    "remark":""
        }
        self._doc["birthday"] = memorial(birthday).save()
        self.save()
        return True
    def insert_memorial_day(self,dict):
        i = cal(dict).save()
        self._doc["memorial_days"].append(i)
        self.save()

    def insert_contact(self,dict):
        i = contact(dict).save()
        self._doc["contact_record"] = i
        self.save()

    def insert_social(self,dict):
        dict["customer_id"] = ObjectId(dict["customer_id"])
        self._doc["social"].append(dict)
        self.save()

class cal(BaseDocument):
    objects = calQuery()
    def __init__(self,c):
        self._collection = "cal"
        super(cal,self).__init__(c)

    def calculate(self):
        self._doc["start_date"] = uti.time_convert_to_utc_date(self._doc["start"])
        self._doc["start_time"] = uti.time_convert_to_utc_time(self._doc["start"])
        self._doc["end_date"] = uti.time_convert_to_utc_date(self._doc["end"])
        self._doc["end_date"] = uti.time_convert_to_utc_time(self._doc["end"])

    def have_done(self):
        self._doc["is_ok"] = "true"
        self.save()
    def do_not_done(self):
        self._doc["is_ok"] = "false"
        self.save()

class memorial(BaseDocument):
    objects = calQuery()
    def __init__(self,c):
        self._collection = "cal"
        super(memorial,self).__init__(c)

    def calculate(self):
        t = time.localtime(int(self._doc["start"]))
        self._doc["start_date"] = uti.time_convert_to_utc_date(self._doc["start"])
        tt = time.localtime().tm_year +" " + t.tm_mon + " " + t.tm_mday
        self._doc["this_year_date"] = int( time.mktime( time.strptime(tt,"%Y %m %d") ))

    def have_done(self):
        self._doc["is_ok"] = "true"
        self.save()
    def do_not_done(self):
        self._doc["is_ok"] = "false"
        self.save()

class contract(BaseDocument):
    objects = contractQuery()
    def __init__(self,contract):
        self._collection = "contract"
        super(contract,self).__init__(contract)

    def calculate(self):
        self._doc["contract_project"] = project(self._doc["contract_project_id"])["project_name"]




class project(BaseDocument):
    def __init__(self,p):
        self._collection = "project"
        super(project,self).__init__(p)
