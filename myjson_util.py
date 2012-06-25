from bson.objectid import ObjectId

def object_hook(dct):
    if "_id" in dct:
        return ObjectId(str(dct["_id"]))
    return dct

def default(obj):
    if isinstance(obj,ObjectId):
        return str(obj)
    raise TypeError("%r is not JSON serializable" % obj)