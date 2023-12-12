step main
    stepto phoneNumberAdd
    speak '你好，请用标准普通话表达您的需求：1.查询电话号码 2.查询机器人工号 3.查询今日天气 4.退出'
    listen '30'
    switch $inputBuffer
    case '查询电话号码' stepto phoneNumberQuery
    case '查询机器人工号' stepto robotIDQuery
    case '退出' exit
    case 'exit' exit
    case '查询今日天气' stepto weather
    case 'weather' stepto weather
    case '' speak '输入超时'
    default speak '很抱歉暂无此功能'
    endswitch
endstep

step phoneNumberAdd
    $zhangsan = '1234567890'
    $lisi = '5324544231'
    $gxy = '原神，启动！'
endstep

step phoneNumberQuery
    speak '请用标准普通话说出 被查询人名字'
    listen '30'
    switch $inputBuffer
    case '张三' speak '张三的电话号码是   ' + $zhangsan
    case '李四' speak '李四的电话号码是   ' + $lisi
    case '郭栩源' speak $gxy
    case '' speak '输入超时'
    default speak '抱歉，查无此人'
    endswitch
endstep

step robotIDQuery
    speak '为您服务的机器人工号是' + $_robotID
    stepto main
endstep

step weather
    speak '请用标准普通话说出 需要查询天气的城市'
    listen '30'
    call weather $inputBuffer
    speak $ret
endstep