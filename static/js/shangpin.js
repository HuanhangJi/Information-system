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
    if (user_id==0){window.open("http://localhost:8001", '_self');}
    else{                     

//                            window.open('/get_task/'+user_id+'/'+renwuhao,'_self');
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": token_csrf },
        url: '/get_task/'+user_id+'/'+renwuhao+'/',
        dataType: "json",
        data: '',
        success: function (res) { //data为地址传过来的数据
            if (res['code']!=200){$('#myModal2').text(res['msg']);$('#myModal2').css("color",'red')}
            else {    x = document.getElementById("lingqu");
            x.innerHTML = "领取成功";
            x.className = "btn btn-lg btn-success disabled";}
            }
        });}
                        };
