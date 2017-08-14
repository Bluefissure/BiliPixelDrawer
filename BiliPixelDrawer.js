// ==UserScript==
// @name         BiliPixelDrawer
// @namespace    
// @version      1.2
// @description  BiliPixelDrawer Client(Script)
// @author       Bluefissure
// @match        live.bilibili.com/pages/1702/pixel-drawing
// @grant        GM_addStyle
// @grant        GM_xmlhttpRequest
// ==/UserScript==
var version = "v1.2";
var style_btn = 'float:right;background:rgba(228,228,228,0.4); cursor:pointer; margin:0px 1px 0px 0px; padding:0px 3px;color:black; border:2px ridge black;border:2px groove black;';
var style_win_top = 'z-index:998; padding:6px 10px 8px 15px;background-color:lightGrey;position:fixed;left:5px;top:100px;border:1px solid grey; ';
var style_win_buttom = 'z-index:998; padding:6px 10px 8px 15px;background-color:lightGrey;position:fixed;right:5px;bottom:5px;border:1px solid grey;  ';

var timer;
var res_time;
var host;
var token;
var total;
var solve;
var info;
var control;
function finishpixel(x,y,color){
    GM_xmlhttpRequest({
        method: "GET",
        url: host.value+"/?token="+token.value+"&&finx="+x+"&&finy="+y,
        headers: {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'referer': '',
            'Cookie': document.cookie
        },
        onload: function(response) {
            var res=JSON.parse(response.responseText);
            if(res.msg=="success"){
                console.log("Callback success");
            }else{
                console.log(res);
            }
        }
    });
}
function drawpixel(x,y,color){
    var formData = new FormData();

    formData.append("x_min", x);
    formData.append("y_min", y);
    formData.append("x_max", x);
    formData.append("y_max", y);
    formData.append("color", color);
    GM_xmlhttpRequest({
        method: "POST",
        url: "http://api.live.bilibili.com/activity/v1/SummerDraw/draw",
        data: formData,
        headers: {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'referer': 'https://account.bilibili.com/site/record.html',
            'Cookie': document.cookie
        },
        onload: function(response) {
            var res;
            try{
                res=JSON.parse(response.responseText);
            }catch(e){
                info.innerHTML="Error:"+e.message;
                return;
            }
            if(res.msg=="success"){
                console.log("Draw at ("+x+","+y+") color:"+color+" success");
                info.innerHTML="Draw at ("+x+","+y+") color:"+color+" success";
                finishpixel(x,y,color);
            }else{
            info.innerHTML="Error:"+res.msg;
            }
        }
    });
}
function getpixel(x,y,color){
    GM_xmlhttpRequest({
        method: "GET",
        url: host.value+"/?token="+token.value,
        headers: {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'referer': '',
            'Cookie': document.cookie
        },
        onload: function(response) {
            var res;
            try{
                res=JSON.parse(response.responseText);
            }catch(e){
                if(e.name=="SyntaxError"){
                    info.innerHTML="Error:Server response failed.";
                }else{
                    info.innerHTML="Error:"+e.message;
                }
                return;
            }
            if(res.msg=="success"){
                x=res.x;
                y=res.y;
                color=res.color;
                var solve_cnt=res.total-res.unsolve;
                total.innerHTML="Total pixel(s):"+res.total;
                solve.innerHTML="Drawed pixel(s):"+solve_cnt;
                drawpixel(x,y,color);
            }else if(res.msg=="finish"){
                console.log("Project finish.");
                info.innerHTML="Project finish.";
                var solve_cnt=res.total-res.unsolve;
                total.innerHTML="Total pixel(s):"+res.total;
                solve.innerHTML="Drawed pixel(s):"+solve_cnt;
                console.log("Stop Auto Drawing");
                clearInterval(timer);
                control.innerHTML = "开始脚本";
            }else{
                info.innerHTML="Error:"+res.msg;
                console.log(res);
            }
        }
    });
}
function draw() {
    var x=0,y=0,color=0;
    GM_xmlhttpRequest({
        method: "GET",
        url: "http://api.live.bilibili.com/activity/v1/SummerDraw/status",
        headers: {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'referer': 'https://account.bilibili.com/site/record.html',
            'Cookie': document.cookie
        },
        onload: function(response) {
            var res=JSON.parse(response.responseText);
            res_time = res.data.time;
            if(res.msg!="success"){
                console.log(res);
                info.innerHTML="Error:"+res.msg;
            }else{
                console.log("left time:"+res_time);
                info.innerHTML="Time left:"+res_time;
            }
            if(res_time==0){
                getpixel(x,y,color);
            }
        }
    });


}
(function() {
    'use strict';
    // Your code here...
    if(window.location.href=="http://live.bilibili.com/pages/1702/pixel-drawing"||
       window.location.href=="https://live.bilibili.com/pages/1702/pixel-drawing"){
        var newDiv = document.createElement("div");
        newDiv.id = "controlWindow";
        newDiv.align = "left";
        document.body.appendChild(newDiv);
        GM_addStyle("#controlWindow{" + style_win_top + " }");
        var table = document.createElement("table");
        newDiv.appendChild(table);
        var th = document.createElement("th");
        th.id = "headTd";
        var thDiv = document.createElement("span");
        thDiv.id = "thDiv";
        thDiv.innerHTML = "BiliPixelDrawer "+version;
        GM_addStyle("#thDiv{color:red;font-size: 12pt;}");
        th.appendChild(thDiv);
        table.appendChild(th);
        var tr = document.createElement("tr");
        table.appendChild(tr);
        var td = document.createElement("td");
        td.id = "footTd";
        tr.appendChild(td);

        host = document.createElement("input");
        host.innerHTML = "Host";
        host.id = "host";
        host.placeholder = "Host";
        token = document.createElement("input");
        token.innerHTML = "Host";
        token.id = "token";
        token.placeholder = "Token";
        td.appendChild(host);
        td.appendChild(document.createElement("p"));
        td.appendChild(token);
        td.appendChild(document.createElement("p"));
        total=document.createElement("p");
        solve=document.createElement("p");
        td.appendChild(total);
        td.appendChild(solve);
        info = document.createElement("span");
        info.id = "info";
        info.innerHTML = "info";
        GM_addStyle("#info{color:red;font-size: 8pt;}");
        td.appendChild(info);
        td.appendChild(document.createElement("p"));

        control = document.createElement("span");
        control.id = "control";
        control.innerHTML = "开始脚本";
        control.addEventListener("click", function () {
            //document.body.removeChild(document.getElementById("controlWindow"));
            if (control.innerHTML == "开始脚本"){
                console.log("Enable Auto Drawing");
                draw();
                timer = setInterval(draw, 10000);
                control.innerHTML = "停止脚本";
            }else{
                console.log("Stop Auto Drawing");
                clearInterval(timer);
                control.innerHTML = "开始脚本";
            }


        }, false);
        td.appendChild(control);
        GM_addStyle("#control{" + style_btn + "}");


    }
})();