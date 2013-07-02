#-*- coding:utf-8 -*-

import dbs

db = dbs.get_db()

sector = {"type" : "sector", "value" : [ u"Education", u"IT", u"state", u"Mining" ]}
vocation = {"type" : "vocation", "value" : [ u"Manager", u"Accounting", u"Employee", u"Business owners" u"Sales" ]}
likes = {"type" : "likes", "value" : [ u"Dance", u"Golf", u"Cocktail Party", u"Singing", u"Football", u"Antique", u"Philately" ]}
customer = {"type" : "customer", "value" : [ ]}
cal_tags = {"type" : "cal_tags", "value" : [ ] }
cal_type = {"type" : "cal_type", "value" : [ u"Work", u"Life" ] }
contact_type = {"type" : "contact_type", "value" : [ u"None", u"Phone", u"Meeting", u"Gift" ] }
relation_h = {"type" : "relation_h", "value" : [ u"Husband",u"Wife", u"Son", u"Daughter", u"Father", u"Mother", u"Granddaughter", u"Grandson" ] }
relation_s = {"type" : "relation_s", "value" : [ u"Colleagues", u"Competitors", u"Friends", u"Relatives" ] }
channel = {"type" : "channel", "value" : [ u"Channel", u"customer recommended", u"Friend recommended" ] }

# passwd: 123456 hashlib.md5("123456").hexdigest()
admin = {"name" : u"user", "passwd" : "e10adc3949ba59abbe56e057f20f883e", "type" : u"用户", "username" : "user" }

db["settings"].save(sector)
db["settings"].save(vocation)
db["settings"].save(likes)
db["settings"].save(customer)
db["settings"].save(cal_tags)
db["settings"].save(cal_type)
db["settings"].save(contact_type)
db["settings"].save(relation_h)
db["settings"].save(relation_s)
db["settings"].save(channel)

db["users"].save(admin)