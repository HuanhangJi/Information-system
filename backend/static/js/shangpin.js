// 登录设置
$(document).ready(function(){
    if (user_id != 0){$("#log_in_0").css('display','none');$("#log_in_1").css('display','inline');}});
// 设置任务星级
layui.use(['rate'], function(){
    var rate = layui.rate;
        rate.render({
        elem: '#star'
        ,value: star1
        ,readonly: true
    })});

