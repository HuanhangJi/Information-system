// 修改文本任务标题
$(document).ready(function(){
    let txt = "文本标注任务1";
    $("#wenbenming1").text(txt);}); 
// 修改文本任务标志
$(document).ready(function(){
    $("#wenbenbiao1").text("文本");
    $("#wenbenbiao1").class("label label-warning");}); 
// 修改任务星级
$(document).ready(function(){
    layui.use(['rate'], function(){
        var rate = layui.rate;
        rate.render({
            elem: '#test1'
            ,value: 1
            ,readonly: true})
        });
    }); 
// 修改任务图片
// $(document).ready(function(){   
//     let path = "./img/7.png";
//     $("#wenbentu1").attr('src',path);});

// 修改图片任务标题
$(document).ready(function(){
    let txt = "图片标注任务1";
    $("#tupianming1").text(txt);}); 
// 修改图片任务标志
$(document).ready(function(){
    $("#tupianbiao1").text("图片");
    $("#tupianbiao1").class("label label-info");}); 
// 修改任务星级
$(document).ready(function(){
    layui.use(['rate'], function(){
        var rate = layui.rate;
        rate.render({
            elem: '#test2'
            ,value: 3
            ,readonly: true})
        });
    }); 

// 修改视频任务标题
$(document).ready(function(){
    let txt = "视频标注任务1";
    $("#shipinming1").text(txt);}); 
// 修改视频任务标志
$(document).ready(function(){
    $("#shipinbiao1").text("视频");
    $("#shipinbiao1").class("label label-success");}); 
// 修改任务星级
$(document).ready(function(){
    layui.use(['rate'], function(){
        var rate = layui.rate;
        rate.render({
            elem: '#test3'
            ,value: 5
            ,readonly: true})
        });
    }); 


// 修改任务星级
$(document).ready(function(){
    layui.use(['rate'], function(){
        var rate = layui.rate;
        rate.render({
            elem: '#test4'
            ,value: 2
            ,readonly: true})
        });
    }); 
// 修改任务星级
$(document).ready(function(){
    layui.use(['rate'], function(){
        var rate = layui.rate;
        rate.render({
            elem: '#test5'
            ,value: 4
            ,readonly: true})
        });
    }); 
// 修改任务星级
$(document).ready(function(){
    layui.use(['rate'], function(){
        var rate = layui.rate;
        rate.render({
            elem: '#test6'
            ,value: 5
            ,readonly: true})
        });
    }); 