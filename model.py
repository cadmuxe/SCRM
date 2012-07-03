__author__ = 'cadmuxe'


customer = {
    "type"          :   {'type':'str','required':'True','default':['客户','渠道','其他']},
    "manager"       :   {'type':'objectid','required':'True','default':[]},         # 财富管理师id
    "name"          :   {'type':'str','required':'True','default':[]},
    "gender"        :   {'type':'str','required':'True','default':['女士','先生']},
    "birthday"      :   {'type':'objectid','required':'False','default':[]},        # 存放birthdayid，输出时自动替换为日期
    "memorial_day"  :   {'type':'list','required':'False','default':[]}             # memorial_id list





}

model = [customer,]