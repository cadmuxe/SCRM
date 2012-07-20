from bson.objectid import ObjectId
import copy,datetime,uti

def object_hook(dct):
    if "_id" in dct:
        dct["_id"] = ObjectId(dct["_id"])
    if "manager" in dct:
        dct["manager"] = ObjectId(dct["manager"])

    if "user_id" in dct:
        dct['user_id'] = ObjectId(dct['user_id'])
    if "attend" in dct:
        l=[]
        for i in dct["attend"]:
            l.append({'id':ObjectId(i['id'])})
        dct["attend"] = l
    if "start" in dct:
        if type(dct["start"]) != datetime.datetime and dct["start"]:
            dct["start"] = uti.time_string_to_datetime(dct["start"])
    if "end" in dct:
        if type(dct["end"]) != datetime.datetime and dct['end']:
            dct["end"] = uti.time_string_to_datetime(dct["end"])
    return dct

def string_hook(d):
    d = copy.copy(d)
    if type(d) == dict:
        for i in d:
            if type(d[i]) == unicode:
                continue
            if type(d[i]) == ObjectId:
                d[i] = unicode(d[i])
                continue
            if type(d[i]) == dict:
                d[i]  = string_hook(d[i])
                continue
            if type(d[i]) == list:
                d[i] = string_hook(d[i])
                continue
        return d
    elif type(d) == list:
        for l in range(0,len(d)):
            if type(d[l]) == unicode:
                continue
            if type(d[l]) == ObjectId:
                d[l] = unicode(d[l])
                continue
            if type(d[l]) == dict:
                d[l] = string_hook(d[l])
                continue
            if type(d[l]) == list:
                d[l] = string_hook(d[l])
                continue
        return d

def default(obj):
    if isinstance(obj,ObjectId):
        return str(obj)
    if isinstance(obj,datetime.datetime):
        return uti.time_datetime_to_string_datetime(obj)
    raise TypeError("%r is not JSON serializable" % obj)