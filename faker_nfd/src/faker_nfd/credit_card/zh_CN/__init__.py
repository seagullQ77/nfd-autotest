# coding=utf-8
from .. import Provider as CreditCardProvider
from .. import CreditCard as CreditCardCn

''' 
add by kangning Yang
'''
class Provider(CreditCardProvider):
    
    prefix_zgjsyh = ['436742', '436745', '622280'] #中国建设银行
    prefix_jtyh = ['458123', '521899', '622260'] #交通银行
    prefix_shyh = ['402674', '622892'] #上海银行
    prefix_zgyzcxyh = ['622188'] #中国邮政储蓄银行
    prefix_zgyh = ['622760','409666 ','438088','622752']#中国银行
    prefix_zggsyh = ['427020','427030','530990','622230','622235','622210','622215','622200','955880']#中国工商银行
    prefix_payh = ['622155 ','622156','528020','526855']#平安银行
    prefix_zsyh = ['622588 ','622575','545947' ,'521302','439229','552534','622577','622579','439227','479229',
                   '356890','356885','545948','545623','552580','552581','552582','552583','552584','552585',
                   '552586','552588','552589','645621','545619','356886','622578','622576' ,'622581','439228',
                   '628262','628362','628362' ,'628262']#招商银行
    '''
    credit_card_types = {
        '中国建设银行': CreditCardCn('中国建设银行',prefix_zgjsyh, 18),
        '交通银行':       CreditCardCn('交通银行',prefix_jtyh, 18),
        '上海银行':       CreditCardCn('上海银行', prefix_shyh,18),
        '中国邮政储蓄银行': CreditCardCn('中国邮政储蓄银行',prefix_zgyzcxyh, 18),
        '中国银行':       CreditCardCn('中国银行',prefix_zgyh, 18),
        '中国工商银行':    CreditCardCn('中国工商银行',prefix_zggsyh,18),
        '平安银行':       CreditCardCn('平安银行', prefix_payh, 18),
        '招商银行':       CreditCardCn('招商银行',prefix_zsyh, 18),
    }
    '''
    '''
    credit_card_types = {
        '中国建设银行': CreditCardCn('中国建设银行',['622280'], 19),
        '交通银行':       CreditCardCn('交通银行',['621335'], 19),
        '上海银行':       CreditCardCn('上海银行', ['621081'],19),
        '中国邮政储蓄银行': CreditCardCn('中国邮政储蓄银行',['621466'], 16),
        '中国银行':       CreditCardCn('中国银行',['621467'], 19),
        '中国工商银行':    CreditCardCn('中国工商银行',['621226'],19),
        '平安银行':       CreditCardCn('平安银行', ['621598'], 19)
    }
    '''
    credit_card_types = {
        '中国建设银行': CreditCardCn('中国建设银行',['622280','622700'], 19),
        '交通银行':       CreditCardCn('交通银行',['621335','622260','622262'], 19),
        '中国银行':       CreditCardCn('中国银行',['621212','623208',], 19),
        '中国工商银行':    CreditCardCn('中国工商银行',['621226','621225','621288','621558'],19),
        '中国农业银行':    CreditCardCn('中国农业银行',['622846', '622848', '622845','622849'],19)
    }


