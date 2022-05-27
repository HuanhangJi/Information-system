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

function lingqu() {
                            x = document.getElementById("lingqu");
                            x.innerHTML = "领取成功";
                            x.className = "btn btn-lg btn-success disabled";
                            window.open('//{{user_id}}/{{task_id}}/','_self');
                        };