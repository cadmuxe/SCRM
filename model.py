#-*- coding:utf-8 -*-

__author__ = 'cadmuxe'
import copy

__customerM = {
    "type"          :   {'type':'str','required':'True','default':['客户','渠道','其他']},
    "manager"       :   {'type':'objectid','required':'True','default':[]},         # 财富管理师id
    "name"          :   {'type':'str','required':'True','default':[]},
    "gender"        :   {'type':'str','required':'True','default':['女士','先生']},
    "birthday"      :   {'type':'objectid','required':'False','default':[]},        # 存放birthdayid，输出时自动替换为日期
    "memorial_day"  :   {'type':'list','required':'False','default':[]}             # memorial_id list
}

__customerO={
    'type':'',
    'manager':'',
    'name':'',
    'gender':'',
    'birthday':{},
    'memorial_day':{},
    'tags':'',
    'sector':'',
    'vocation':'',
    'phone':{'work':'','personal':'','home':''},
    'email':{'work':'','personal':''},
    'company':'',
    'home_addr':'',
    'likes':[],
    'wishs':[],
    'remark':'',
    'contact_record':{},
    'relevance_people':[],
    'social':[],
    'channel':{}
}
def getCustomerModel():
    return copy.deepcopy(__customerO)