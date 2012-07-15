#-*- coding:utf-8 -*-
import json,pymongo,time,myjson_util
from bson.objectid import ObjectId

# helps


def myjsonify(dic):
    """ convert  dic object to json string
    """
    return json.dumps(dic,default=myjson_util.default)
    #return json.dumps(dic,default=json_util.default,ensure_ascii=False)

def get_pure_dict(dic):
    for key in dic:
        if isinstance(dic[key],ObjectId):
            dic[key] = str(dic[key])
            continue
        if isinstance(dic[key],dict):
            dic[key]=get_pure_dict(dic[key])
            continue
    return dic


def time_convert_to_utc_date(epoch):
    t = time.gmtime(int(epoch))
    return str(t.tm_year) + "-"+ str(t.tm_mon) + "-"+str(t.tm_mday)
def time_convert_to_utc_time(epoch):
    t = time.gmtime(int(epoch))
    return str(t.tm_hour) + ':' + str(t.tm_min)
def print_dict(dic):
    for i in dic:
        print i + " : " + dic[i] + "\n"
