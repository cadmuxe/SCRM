#-*- coding:utf-8 -*-
import pymongo
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

def __get_customer_total_contract_amount(customer_id):
    """ get customer's totally contract amount
    """
    amount = 0
    if type(customer_id) == str:
        customer_id = ObjectId(customer_id)
    list = db["contract"].find({"_id":customer_id})
    for c in list:
        amount += int(c["amount"])
    return amount

def list_differ(new,old):
    diff={"add":[],"sub":[]}
    for i in new:
        try:
            old.index(i)
        except ValueError:
            diff["add"].append(i)
    for i in old:
        try:
            new.index(i)
        except ValueError:
            diff["old"].append(i)
    return diff

def tags_update_add(tag_type,value):
    t = db["settings"].find({"type":tag_type})
    if t["value"].has_key(value):
        t["value"][value] = int(t["value"][value]) + 1
    else:
        t["value"][value] = 1
    db["settings"].save(t)

def tags_update_sub(tag_type,value):
    value = unicode(value)
    t = db["settings"].find({"type":tag_type})
    if t["value"].has_key(value):
        t["value"][value] = int(t["value"][value]) - 1
    else:
        raise ValueError
    if int(t["value"][value]) == 0:
        t["value"].pop(value)
    db["settings"].save(t)

def tags_update(tag_type,diff):
    for i in diff["add"]:
        tags_update_add(tag_type,i)
    for i in diff["sub"]:
        tags_update_sub(tag_type,i)

class customer:
    def __init__(self, c):
        """
        created by id or customer dict
        """
        if type(c) == dict:
            self.__customer = c
        elif type(c) == unicode:
            db = get_db()
            self.__customer = db["customer"].find_one({"_id":ObjectId(c)})
        elif type(c) == ObjectId:
            db = get_db()
            self.__customer = db["customer"].find_one({"_id":c})
        else:
            raise ValueError

    def save(self):
        return db["customer"].save(self.__customer)

    def __get_customer_total_contract_amount(self):
        """ get customer's totally contract amount
        """
        amount = 0
        customer_id = self.__customer["_id"]
        if type(customer_id) == str:
            customer_id = ObjectId(customer_id)
        list = db["contract"].find({"_id":customer_id})
        for c in list:
            amount += int(c["amount"])
        return amount

    def __getattr__(self, item):
        return self.__customer[item]
    def __getitem__(self, item):
        return self.__customer[item]
    def __setitem__(self, key, value):
        self.__customer[key] = value

    def get_pure_dict(self,selection=[]):
        """
        selection: ["",""] set the return fields
        """
        if selection ==[]:
            for f in self.__customer:
                selection.append(f)
        n_value={}
        for field in selection:
            if field == "contact_record":
                if self.__customer.has_key("contact_record"):
                    n_value["contact_record"] = cal(self.__customer[field]).get_date()
                else:
                    n_value["contact_record"] = u"无联络信息"
                continue
            if field == "amount":
                n_value["amount"] = self.__get_customer_total_contract_amount()
                continue
            if field == "birthday":
                n_value["birthday"] = cal(self.__customer["birthday"]).get_date()
                continue
            n_value[field]=self.__customer[field]
        return uti.get_pure_dict(n_value)


    def insert_new(self):
        """ Insert customer to dbs, customer is a dict object
        replace the birthday with the memorial_id.
        return customer_id
        """
        self.save()
        if self.__customer["birthday"] != "0":
            birthday = {"type":"birthday",
                        "user_id":self.__customer["_id"],
                        "title":self.__customer["name"]+u"的生日",
                        "allDay":"false",
                        "start":self.__customer["birthday"],
                        "end":0,
                        "repeat":"1y",
                        "remind":0,
                        "editable":"false",
                        "remark":""
            }
            self.__customer["birthday"] = cal(birthday).save()
            self.save()
        return self.__customer["_id"]
    def insert_memorial_day(self,dict):
        i = cal(dict).save()
        self.__customer["memorial_days"].append(i)
        self.save()

    def insert_contact(self,dict):
        i = contact(dict).save()
        self.__customer["contact_record"] = i
        self.save()

    def insert_social(self,dict):
        self.__customer["social"].append(dict)
        self.save()





class customer_list:
    def __init__(self,query, keys="", field_search=[], field_selection=[]):
        self.__customers_o = mongo_find(db["customer"],query, keys = keys, field_search=field_search)
        self.__customers_pure = []
        self.__customers = []
        for i in self.__customers_o:
            self.__customers.append(customer(i))
        for c in self.__customers:
            self.__customers_pure.append(c.get_pure_dict(field_selection))


    def __iter__(self):
        return self.__customers.__iter__()
    def __len__(self):
        return  self.__customers.count()
    def pagination(self,skip,limit=10):
        return self.pure_dict()[skip:skip+limit]
    def pure_dict(self):
        """  convert all the ObjectId to string in the customer list
        """
        return self.__customers_pure


class cal:
    def __init__(self,c):
        if type(c) == dict:
            self.__cal = c
        elif type(c) == unicode:
            db = get_db()
            self.__cal = db["cal"].find_one({"_id":ObjectId(c)})
        elif type(c) == ObjectId:
            db = get_db()
            self.__cal = db["cal"].find_one({"_id":c})
        else:
            raise ValueError
        self.__cal["start_date"] = uti.time_convert_to_utc_date(self.__cal["start"])
        self.__cal["start_time"] = uti.time_convert_to_utc_date(self.__cal["start"])
        self.__cal["end_date"] = uti.time_convert_to_utc_date(self.__cal["end"])
        self.__cal["end_time"] = uti.time_convert_to_utc_date(self.__cal["end"])
    def __getattr__(self, item):
        return self.__cal[item]
    def __getitem__(self, item):
        return self.__cal[item]
    def __setitem__(self, key, value):
        self.__cal[key] = value
    def get_date(self):
        return uti.time_convert_to_utc_date(self.__cal["start"])
    def get_time(self):
        return uti.time_convert_to_utc_time(self.__cal["start"])
    def save(self):
        return db["cal"].save(self.__cal)
    def get_pure_dict(self):
        return uti.get_pure_dict(self.__cal)
    def have_done(self):
        self.__cal["is_ok"] = "true"
        self.save()
    def do_not_done(self):
        self.__cal["is_ok"] = "false"
        self.save()


class cal_list:
    def __my_init(self):
        self.__cal_pure = []
        self.__cal = []
        for i in self.__cal_o:
            self.__cal.append(cal(i))
        for c in self.__cal:
            self.__cal_pure.append(c.get_pure_dict(field_selection))

    def __init__(self, customer_id=0,start = 0,end = 0):
        if customer_id != 0:
            if type(customer_id) == unicode:
                customer_id = ObjectId(customer_id)
            self.__cal_o = db["cal"].find({"attend":customer_id})
        elif start != 0 and end != 0:
            self.__cal_o = db["cal"].find({"start":{"$gt":start,"$lt":end}})
        else:
            raise ValueError
        self.__my_init()

    def __iter__(self):
        return self.__cal.__iter__()
    def __len__(self):
        return  self.__cal.count()
    def pagination(self,skip,limit=10):
        return self.pure_dict()[skip:skip+limit]
    def pure_dict(self):
            """  convert all the ObjectId to string in the customer list
            """
            return self.__cal_pure


class contract:
    def __init__(self,contract):
        if type(contract) == ObjectId:
            db = get_db()
            self.__contract = db["contract"].find_one({"_id":contract})
        elif type(contract) == unicode:
            db = get_db()
            self.__contract = db["contract"].find_one({"_id":ObjectId(contract)})
        elif type(contract) ==dict:
            self.__contract = contract
        else:
            self.__contract ={}
        self.__contract["contract_project"] = project(self.__contract["contract_project_id"])["project_name"]
    def __getattr__(self, item):
            return self.__contract[item]
    def __getitem__(self, item):
        return self.__contract[item]
    def __setitem__(self, key, value):
        self.__contract[key] = value
    def save(self):
        return db["contract"].save(self.__contract)
    def get_pure_dict(self):
        return uti.get_pure_dict(self.__contract)

class contract_list:
    def __init__(self,customer_id="",start=0,end=0):
        if customer_id !="":
            customer_id = ObjectId(customer_id)
            self.__contracts_o = db["contract"].find({"user_id":customer_id})
        elif start != 0:
            self.__contracts_o = db["contract"].find({"date":{"$gt":start,"$lt":end}})

        self.__contracts_pure = []
        self.__contracts = []
        for i in self.__contracts_o:
            self.__contracts.append(contract(i))
        for c in self.__contracts:
            self.__contracts_pure.append(c.get_pure_dict())


    def __iter__(self):
        return self.__contracts.__iter__()
    def __len__(self):
        return  self.__contracts.count()
    def pagination(self,skip,limit=10):
        return self.pure_dict()[skip:skip+limit]
    def pure_dict(self):
        """  convert all the ObjectId to string in the customer list
        """
        return self.__contracts_pure



class project:
    def __init__(self,c):
        if type(c) == dict:
            self.__project = c
        elif type(c) == ObjectId:
            db = get_db()
            self.__project = db["project"].find_one({"_id":c})
        elif type(c) == unicode:
            db = get_db()
            self.__project = db["project"].find_one({"_id":ObjectId(c)})
        else:
            self.__project = {}
    def __getattr__(self, item):
        return self.__project[item]
    def __getitem__(self, item):
        return self.__project[item]
    def __setitem__(self, key, value):
        self.__project[key] = value

    def save(self):
        return db["project"].save(self.__project)
    def get_pure_dict(self):
        return uti.get_pure_dict(self.__project)
