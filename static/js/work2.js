// 设置任务号
// $(document).ready(function(){
//     $("#renwuhao").text('8525846');});
// 设置任务目标
// $(document).ready(function(){
//     $("#target").text('奥特曼');});
// 设置任务进度
// $(document).ready(function(){
//     $("#jindu").text('90');
//     $('#jindu2').attr('aria-valuenow','90');
//     $("#jindu2").attr("style","width: 90%");});

// 登录设置
$(document).ready(function(){
    if (user_id != 0){$("#log_in_0").css('display','none');$("#log_in_1").css('display','inline');};
    if (page == 1){$("#previous").attr('disabled','"disabled"');};
});
// 上一页函数
function previous_task(){
    var previous_page = page-1;
    $.ajax({type:'get',
        // /user_id/task_id/?page=
        url:'/jdzz_work2/'+user_id+'/'+task_id+'/?page='+previous_page,
        dataType:'json',
        async: false,
        success:function(res){
            data = res['data'];
            page = data['new_page'];
            task_img = data['task_img'];
            if (page == 1){$("#previous").attr('disabled','"disabled"');};
            if ((page != page_max) && ($("#next").attr('disabled') =="disabled")){
                $("#next").removeAttr('disabled');
                $('#imgform').removeAttr('style','display');
                $('#end').css('display','none');
                };
            $("#task_img").attr("src",data['task_img']);
            $("#target").text(data['target']);
            $("#jindu").text(data['new_page']);
            $("#jindu2").attr("style","width: "+data['jindu']+"%");
            },
    });
};
// 下一页的函数
function next_task(){
    var next_page = page+1;
    $.ajax({type:'get',
        // /user_id/task_id/?page=    
        url:'/jdzz_work2/'+user_id+'/'+task_id+'/?page='+next_page,
        dataType:'json',
        async: false,
        success:function(res){
            data = res['data'];
            page = data['new_page'];
            task_img = data['task_img'];
            if ((page != 1) && ($("#previous").attr('disabled') =="disabled")){$("#previous").removeAttr('disabled','disabled');};
            if (page == page_max){$("#next").attr('disabled','"disabled"');$('#imgform').css('display','none');$('#end').removeAttr('style','display');};
            $("#task_img").attr("src",data['task_img']);
            $("#target").text(data['target']);
            $("#jindu").text(data['new_page']);
            $("#jindu2").attr("style","width: "+data['jindu']+"%");
            },
    });
};
// 提交图片标注结果
function post_result(t){
    var token_csrf = csrf_token;
    var JSON_data = { "result":t,'user_id':user_id,'task_id':task_id,'page':page };
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": token_csrf },
        url: "/jdzz_work2_post/",
        dataType: "json",
        data: JSON.stringify(JSON_data), //传进views里的数据
        success: function (data) { //data为地址传过来的数据
            // 可以点第二次
            // $('.imageLabel-box').remove();
            next_task();
            new $.zui.Messager('标注成功', {
                icon: 'ok-sign',
                type: 'success',
                // time: 3
            }).show(); 
        }
        });
};

// 进入标注模式
function click_button(){
    $('.addpic').click();
    // var img_div = $('.imageLabel-box-active').html();
};

function end_window(){
    window.opener=null;
    // var img_div = $('.imageLabel-box-active').html();
};
function end_task(){
    var JSON_data = {};
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        headers: { "X-CSRFToken": csrf_token },
        url: "/commit_task_2/"+user_id+'/'+task_id+'/'+page+'/',
        dataType: "json",
        data: JSON.stringify(JSON_data), //传进views里的数据
        success: function (res) { //data为地址传过来的数据
            if (res['code']!=200){$('#myModal2').text(res['msg']);$('#myModal2').css("color",'red')}
            else {$('#myModal2').css("color",'#0b68fb');$('#myModal2').text(res['msg']);}
            }
        });
}