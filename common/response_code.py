# coding: utf-8

# 响应成功，状态码200
CODE_SUCCESS = '000000'
MSG_SUCCESS = '成功'
# token失效或权限认证错误，状态码401
CODE_AUTH_ERROR = '000001'
MSG_AUTH_ERROR = 'Token认证失败, 请重新登录'
# 业务上的错误
CODE_BUSSINESS_ERROR = '000002'
MSG_BUSSINESS_ERROR = ''
# 服务器内部错误，状态码500
CODE_SERVER_ERROR = '000003'
MSG_SERVER_ERROR = '网络操作失败，请稍后重试'
# 未发现接口
CODE_NOT_FOUND_ERROR = '000004'
MSG_NOT_FOUND_ERROR = '服务器没有此接口'
# 未知错误
CODE_UNKNOWN_ERROR = '000005'
MSG_UNKNOWN_ERROR = '未知错误'
# 拒绝访问
CODE_REJECT_ERROR = '000006'
MSG_REJECT_ERROR = '拒绝访问'
# 拒绝访问
CODE_METHOD_ERROR = '000007'
MSG_METHOD_ERROR = '请求方法错误'
# 缺少参数
CODE_PARAMETER_ERROR = '000008'
MSG_PARAMETER_ERROR = '缺少参数'

from enum import Enum, unique


@unique
class MiracleLove(Enum):
    MON = '林志玲'
    TUS = '陈意涵'
    WEN = '张柏芝'
    THU = '辛芷蕾'
    FRI = '周冬雨'


mon = MiracleLove.MON
tus = MiracleLove.TUS
wen = MiracleLove.WEN
print(mon, tus, wen)

print(mon is MiracleLove.MON)
print(mon == MiracleLove.MON)
print(mon is tus)
print(wen != MiracleLove.TUS)
# 不等于任何非本枚举类的值
print(mon == 0)

print(mon.name, ':', mon.value)


class Attr(Enum):
    name = 'NAME'
    value = 'VALUE'


print(Attr.name.value, Attr.value.name)
