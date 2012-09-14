#-*- coding:utf-8 -*-

import dbs

db = dbs.get_db()

sector = {"type" : "sector", "value" : [ u"医药", u"金融", u"房地产", u"矿业", u"运输", u"教育" ]}
vocation = {"type" : "vocation", "value" : [ u"经理", u"会计", u"雇员", u"企业主", u"销售" ]}
likes = {"type" : "likes", "value" : [ u"舞蹈", u"高尔夫", u"酒会", u"唱歌", u"足球", u"古董", u"集邮" ]}
customer = {"type" : "customer", "value" : [ ]}
cal_tags = {"type" : "cal_tags", "value" : [ ] }
cal_type = {"type" : "cal_type", "value" : [ u"工作", u"生活", u"想法" ] }
contact_type = {"type" : "contact_type", "value" : [ u"无", u"电话", u"会面", u"礼物" ] }
relation_h = {"type" : "relation_h", "value" : [ u"丈夫", u"妻子", u"儿子", u"女儿", u"父亲", u"母亲", u"孙女", u"孙子" ] }
relation_s = {"type" : "relation_s", "value" : [ u"同事",u"竞争对手", u"朋友", u"亲戚" ] }
channel = {"type" : "channel", "value" : [ u"渠道", u"客户推荐", u"朋友推荐" ] }

# passwd: 123456 hashlib.md5("123456").hexdigest()
admin = {"name" : u"张轶凡", "passwd" : "0bc47a1885546da321e215fc6261f79a", "type" : u"用户", "username" : "zhangyifan" }

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