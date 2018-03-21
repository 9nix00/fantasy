"""
==========================
一些临时的Hacker操作
==========================

"""


def hack_webargs():
    from webargs import validate

    validate.Length.message_min = '长度不能少于{min}位'
    validate.Length.message_max = '长度不能多于{min}位'
    validate.Length.message_all = '长度必须介于{min}到{max}之间'
    validate.Regexp.default_message = '输入的字符不符合规范'
    pass
