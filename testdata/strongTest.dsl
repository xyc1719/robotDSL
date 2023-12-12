step main
    stepto phonenumberadd
    speak '你好，请用标准普通话表达您的需求：1.查询电话号码 2.查询机器人工号 3.查询今日天气 4.退出'
    listen '30'
    switch $inputBuffer
    case '查询电话号码' stepto phonenumberquery
    case '查询机器人工号' speak '为您服务的机器人工号是' + $_robotID
    case '退出' exit
    case 'exit' exit
    case '查询今日天气' stepto weather
    case 'weather' stepto weather
    case '' speak '糟糕，无输入'
    default speak '很抱歉暂无此功能'
    endswitch
endstep

step phonenumberadd
    $zhangsan = '1234567890'
    $lisi = '5324544231'
    $gxy = '原神，启动！'
endstep

step phonenumberquery
    speak '请用标准普通话说出 被查询人名字'
    listen '30'
    switch $inputBuffer
    case '张三' speak '张三的电话号码是   ' + $zhangsan
    case '李四' speak '李四的电话号码是   ' + $lisi
    case '郭栩源' speak $gxy
    default speak '抱歉，查无此人'
    endswitch
endstep

step weather
    speak '请用标准普通话说出 需要查询天气的城市'
    listen '30'
    call weather $inputBuffer
    speak $ret
endstep