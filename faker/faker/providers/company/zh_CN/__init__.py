# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .. import Provider as CompanyProvider


class Provider(CompanyProvider):
    formats = ["{{company_prefix}}{{company_suffix}}", ]

    company_prefixes = ["超艺", "和泰", "九方", "鑫博腾飞", "戴硕电子", "济南亿次元",
                        "海创", "创联世纪", "凌云", "泰麒麟", "彩虹", "兰金电子",
                        "晖来计算机", "天益", "恒聪百汇", "菊风公司", "惠派国际公司",
                        "创汇", "思优", "时空盒数字", "易动力", "飞海科技", "华泰通安",
                        "盟新", "商软冠联", "图龙信息", "易动力", "华远软件", "创亿",
                        "时刻", "开发区世创", "明腾", "良诺", "天开", "毕博诚", "快讯",
                        "凌颖信息", "黄石金承", "恩悌", "雨林木风计算机", "双敏电子",
                        "维旺明", "网新恒天", "数字100", "飞利信", "立信电子", "联通时科",
                        "中建创业", "新格林耐特", "新宇龙信息", "浙大万朋", "MBP软件",
                        "昂歌信息", "万迅电脑", "方正科技", "联软", "七喜", "南康", "银嘉",
                        "巨奥", "佳禾", "国讯", "信诚致远", "浦华众城", "迪摩", "太极",
                        "群英", "合联电子", "同兴万点", "襄樊地球村", "精芯", "艾提科信",
                        "昊嘉", "鸿睿思博", "四通", "富罳", "商软冠联", "诺依曼软件",
                        "东方峻景", "华成育卓", "趋势", "维涛", "通际名联"]
    company_suffixes = [n + "有限公司" for n in ["科技", "网络", "信息", "传媒","农业","畜牧","种植"]]
    
    @classmethod
    def company_prefix(cls):
        return cls.random_element(cls.company_prefixes)
    
    @classmethod
    def corporate_code(cls):
        return cls.numerify("###############")
    
    @classmethod
    def organization_code(cls):
        org = ["0","1","2","3","4","5","6","7","8","9",
               "A","B","C","D","E","F","G","H","I","J",
               "K","L","M","N","O","P","Q","R","S","T",
               "U","V","W","X","Y","Z"]
        base = ""
        for i in range(8):
            base += cls.random_element(org)
        count = 0
        weight = [3, 7, 9, 10, 5, 8, 4, 2] #权重项
        mp_value={"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
                  "A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,
                  "K":20,"L":21,"M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,
                  "U":30,"V":31,"W":32,"X":33,"Y":34,"Z":35}
        for i in range(0,len(base)): 
            count = count +mp_value[base[i]]*weight[i] 
        base +='-'+str(11-count%11) #算出校验码 
        return base
    
