// 登录设置
$(document).ready(function(){
    if (user_id != 0){$("#log_in_0").css('display','none');$("#log_in_1").css('display','inline');};
    if (page == 1){$("#previous").attr('disabled','"disabled"');};
});

// 设置任务进度
$(document).ready(function(){
    $("#jindu").text(jindu);
    $('#jindu2').attr('aria-valuenow',jindu);
    $("#jindu2").css("width", jindu+'%');
    });
// 上一页函数
function previous_task(){
    var previous_page = page-1;
    $.ajax({type:'get',
        // /user_id/task_id/?page=
        url:'/jdzz_work1/'+user_id+'/'+task_id+'/?page='+previous_page,
        dataType:'json',
        async: false,
        success:function(res){
            data = res['data'];
            page = data['new_page'];
            if (page == 1){$("#previous").attr('disabled','"disabled"');};
            if ((page != page_max) && ($("#next").attr('disabled') =="disabled")){
                $("#next").removeAttr('disabled');
                $('.btn-primary').removeAttr('style','display');
                $('#end').css('display','none');
                };
            $("#neirong").text(data['content']);
            $("#jindu").text(data['jindu']);
            $("#jindu2").attr("style","width: "+data['jindu']+"%");
            },
    });
};
// 下一页的函数
function next_task(){
    var next_page = page+1;
    $.ajax({type:'get',
        // /user_id/task_id/?page=    
        url:'/jdzz_work1/'+user_id+'/'+task_id+'/?page='+next_page,
        dataType:'json',
        async: false,
        success:function(res){
//            $("#neirong").text('555');
            data = res['data'];
            page = data['new_page'];
            if ((page != 1) && ($("#previous").attr('disabled') =="disabled")){$("#previous").removeAttr('disabled');};
            if (page == page_max){$("#next").attr('disabled','"disabled"');$('#choices .btn-primary').css('display','none');$('#end').removeAttr('style','display');};
            $("#neirong").text(data['content']);
            $("#jindu").text(data['jindu']);
            $("#jindu2").attr("style","width: "+data['jindu']+"%");
            },
    });
};
function choice1(){
    var token_csrf = csrf;
    var JSON_data = { "choice": '开心','user_id':user_id,'task_id':task_id,'page':page };
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": token_csrf },
        url: "/jdzz_work1_post/",
        dataType: "json",
        data: JSON.stringify(JSON_data), //传进views里的数据
        success: function () { //data为地址传过来的数据
            next_task();
            }
        });
    };
function choice2(){
    var token_csrf = csrf;
    var JSON_data = { "choice": '难过','user_id':user_id,'task_id':task_id,'page':page };
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": token_csrf },
        url: "/jdzz_work1_post/",
        dataType: "json",
        data: JSON.stringify(JSON_data), //传进views里的数据
        success: function () { //data为地址传过来的数据
            next_task();
            }
        });
    };
function choice3(){
    var token_csrf = csrf;
    var JSON_data = { "choice": '生气','user_id':user_id,'task_id':task_id,'page':page };
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": token_csrf },
        url: "/jdzz_work1_post/",
        dataType: "json",
        data: JSON.stringify(JSON_data), //传进views里的数据
        success: function () { //data为地址传过来的数据
            next_task();
            }
        });
    };
function choice4(){
    var token_csrf = csrf;
    var JSON_data = { "choice": '其他','user_id':user_id,'task_id':task_id,'page':page };
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": token_csrf },
        url: "/jdzz_work1_post/",
        dataType: "json",
        data: JSON.stringify(JSON_data), //传进views里的数据
        success: function () { //data为地址传过来的数据
            next_task();
            }
        });
    };