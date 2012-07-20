#-*- coding:utf-8 -*-
import json,pymongo,time,myjson_util,calendar,datetime
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

def time_string_to_datetime(s):
    """
    convert  string to datetime type
    "2012-1-1 12:00" to datetime
    """
    if type(s) != datetime.datetime:
        [a,b] = s.split(' ')
        a = a.split('-')
        b = b.split(':')
        return datetime.datetime(int(a[0]),int(a[1]),int(a[2]),int(b[0]),int(b[1]))
    return s
def time_string_to_string_time(d):
    return d.split(' ')[1]
def time_datetime_to_string_date(d):
    return d.strftime("%Y-%m-%d")
def time_datetime_to_string_time(d):
    return d.strftime("%H:%M")
def time_datetime_to_string_datetime(d):
    return d.strftime("%Y-%m-%d %H:%M")

def print_dict(dic):
    for i in dic:
        print i + " : " + dic[i] + "\n"
