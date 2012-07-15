from bson.objectid import ObjectId
import copy

def object_hook(dct):
    if "_id" in dct:
        dct["_id"] = ObjectId(str(dct["_id"]))
    if "manager" in dct:
        dct["manager"] = ObjectId(str(dct["manager"]))
    if "attend" in dct:
        l=[]
        for i in dct["attend"]:
            l.append(ObjectId(i))
        dct["attend"] = l
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
    raise TypeError("%r is not JSON serializable" % obj)