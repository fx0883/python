
function inithead() {
    if (IsLoginIn() == true) {
        $("#goCenter").attr("style", "background-position: -10px -40px;");
        $("#goCenter").click(function () {
            headHideAll("jsLogined");
            $("#jsLogined").toggle("fast")
        });
        $("#jsusername").html(getCookiesWithKey("21rednet", "JSUserName"));
        if (getCookiesWithKey("21rednet", "IsVipLogin") == "true") {
            $("#jsVipClass").html(getVipClass(getCookiesWithKey("21rednet", "jsVipClass")));
            $("#jsHXB").html(getCookiesWithKey("21rednet", "Vip_TrueExpense"));
        } else {
            $("#jsvip").hide();
        }
        $("#jsloginout").click(function () {
            loginout()
        });
    }
    else {
        $("#goCenter").click(function () {
            headHideAll("jsUnlogin");
            $("#jsUnlogin").toggle("fast");
        });
    }
    $("#goSearch").click(function () {
        headHideAll("jsSearch");
        $("#jsSearch").toggle("fast")
    });
}
function getVipClass(i) {
    if (i == 0)return "普通VIP会员"; else if (i == 1)return "初级VIP会员"; else if (i == 2)return "高级VIP会员"; else if (i == 3)return "至尊VIP会员"; else return ""
}
function headHideAll(obj) {
    if (obj != "jsUnlogin") $("#jsUnlogin").hide();
    if (obj != "jsLogined") $("#jsLogined").hide();
    if (obj != "jsSearch") $("#jsSearch").hide();
}
var baseHotIndex = 1;
function initmid() {
    showReadHistory();
    setInterval("daojishi()", 1000);
    $("#hot1").click(function () {
        midShow(1)
    });
    $("#hot2").click(function () {
        midShow(2)
    });
    $("#hot3").click(function () {
        midShow(3)
    });
    $("#hot4").click(function () {
        midShow(4)
    });
}
var baseTheTime = new Date();
function daojishi() {
    baseTheTime.setTime(baseTheTime.getTime() + 1000);
    var h = 23 - baseTheTime.getHours();
    if (h >= 22)
        return;
    var m = 59 - baseTheTime.getMinutes();
    if (m < 10) m = "0" + m;
    var s = 59 - baseTheTime.getSeconds();
    if (s % 5 == 0)
        baseTheTime = new Date();
    if (s < 10) s = "0" + s;
    $(".daojishi").html("(倒计时" + h + ":" + m + ":" + s + ")");
}
function midShow(i) {
    if (i == baseHotIndex)
        return;
    $("#hot" + baseHotIndex).removeClass("click");
    var _left = (i - 1) * 25;
    var o = $("#hotbg");
    o.animate({marginLeft: _left + '%'}, 200, function () {
        $("#hot" + i).addClass("click");
    });
    var _baseleft = (i > baseHotIndex) ? "-100%" : "100%";
    var _ileft = (i > baseHotIndex) ? "100%" : "-100%";
    $("#hotinfo" + baseHotIndex).animate({"marginLeft": _baseleft}, 200, function () {
        $(this).hide()
    });
    $("#hotinfo" + i).show().css("marginLeft", _ileft);
    $("#hotinfo" + i).animate({marginLeft: "0"}, 200);
    baseHotIndex = i;
}
function getCookiesWithKey(key, c_name) {
    if (document.cookie.length > 0) {
        var k_start = document.cookie.indexOf(key + "=");
        if (k_start == -1)
            return "";
        k_start = k_start + key.length + 1
        var k_end = document.cookie.indexOf(";", k_start);
        if (k_end == -1) k_end = document.cookie.length;
        var cookiesWithKey = unescape(document.cookie.substring(k_start, k_end));
        if (c_name == "")return cookiesWithKey;
        var cookies = cookiesWithKey.split("&");
        for (var i = 0; i < cookies.length; i++) {
            if (cookies[i].split("=")[0] == c_name) {
                return cookies[i].split("=")[1];
            }
        }
    }
    return ""
}
function IsLoginIn() {
    var uname = getCookiesWithKey("21rednet", "UserName");
    if (uname == null)
        return false; else if (uname == "")
        return false; else
        return true;
}
function getSystem() {
    var ua = navigator.userAgent.toLowerCase();
    if (ua.indexOf("iphone") > 0 || ua.indexOf("ipad") > 0)
        return "Iphone"; else if (ua.indexOf("windows") > 0)
        return "Win"; else if (ua.indexOf("android") > 0 || ua.indexOf("linux") > 0)
        return "And"; else
        return "Unknow";
}
function getReadHistory() {
    var cookieString = new String(document.cookie);
    var cookieHeader = "ReadHistory=";
    var beginPosition = cookieString.indexOf(cookieHeader);
    var myvalue = "";
    if (beginPosition != -1) {
        myvalue = cookieString.substring(beginPosition + cookieHeader.length);
        var SemiPos = myvalue.indexOf('\;');
        if (SemiPos > 0)
            myvalue = myvalue.substring(0, SemiPos);
    }
    return myvalue;
}
function showReadHistory() {
    var _readjson = getReadHistory();
    if (_readjson == "")
        return;
    var _list = eval("(" + _readjson + ")");
    var _len = _list.length;
    if (_readjson == "" || _list == null || _len == 0)
        return
    $("#jsdivHistory").show();
    $("#jsreaddown").click(function () {
        $("#divHistorymore").slideDown(200);
        $("#jsreadup").show();
        $(this).hide();
    });
    $("#jsreadup").click(function () {
        $("#divHistorymore").slideUp(200);
        $("#jsreaddown").show();
        $(this).hide();
    });
    var _readTemp = $("#divHistory").html();
    $("#divHistory").html(_readTemp.replace(/aid/g, _list[_len - 1].aid).replace("{name}", unescape(_list[_len - 1].name)).replace("{bid}", (_list[_len - 1].bid) > 0 ? _list[_len - 1].bid : "index").replace("{title}", (_list[_len - 1].bid > 0) ? "（续读）" : ""));
    var _html = "";
    var i = 0;
    _list.forEach(function (o) {
        if (i < _len - 1)
            _html += _readTemp.replace(/aid/g, o.aid).replace("{name}", unescape(o.name)).replace("{bid}", (o.bid > 0) ? o.bid : "index").replace("{title}", (o.bid > 0) ? "（续读）" : "");
        i++;
    });
    if (_html != "")
        $("#divHistorymore").html(_html);
}
function loginout() {
    var _url = top.location.href;
    _url = "http://login.sns.hongxiu.com/comloginout.aspx?url=" + escape(_url);
    setTimeout("window.location='" + _url + "'", 0);
}
function isVertical() {
    var _or = window.orientation;
    if (_or == 0 || _or == 180)
        return true; else
        return false;
}
function gotourl() {
    document.cookie = "beginrootpage=1;domain=hongxiu.com;path=/";
    window.location = "http://www.hongxiu.com";
}
function donewtips() {
    var ua = navigator.userAgent;
    var low = ua.toLowerCase();
    if (low.indexOf("android") > 0 || low.indexOf("linux") > 0) {
        $("#tip_download").css('display', 'block')
        $("#adownload").attr("href", "http://hongxiu.cn/clientdown/");
        $("#adownload").html("<img src=\"/images/wapiphone/ad3.gif\" width=\"100%\" />");
    } else if (low.indexOf("windows phone") > 0) {
        $("#tip_download").css('display', 'block')
        $("#adownload").attr("href", "http://www.windowsphone.com/zh-cn/store/app/%E7%BA%A2%E8%A2%96%E4%B9%A6%E5%9F%8E/93534dd1-6a6e-45ae-8887-1bc79611ea6c");
        $("#adownload").html("<img src=\"/images/wapiphone/ad3.gif\" width=\"100%\" />");
    }
    else if (low.indexOf("iphone") > 0 || low.indexOf("ipad") > 0 || low.indexOf("ios") > 0) {
        $("#tip_download").css('display', 'block')
        $("#adownload").attr("href", "http://hongxiu.cn/clientdown/");
        $("#adownload").html("<img src=\"/images/wapiphone/iosad.gif\" width=\"100%\" />");
    }
    else
        $("#tip_download").css('display', 'none');
}
function getStore() {
    if (IsLoginIn() == false)
        return;
    var _mycnt = getCookiesWithKey("SystemTipCount", "");
    var _msg = "";
    var _favcnt = 0;
    var Then = new Date()
    Then.setTime(Then.getTime() + 10 * 60 * 1000);
    if (_mycnt == "") {
        $.getScript("http://user.api.hongxiu.com/tip/?echo=json", function () {
            try {
                _msg = SystemTipCount.SystemLastMessageTip;
                _favcnt = SystemTipCount.StoreUpdateCount;
                document.cookie = "SystemTipCount={\"StoreUpdateCount\":" + _favcnt + ",\"SystemLastMessageTip\":\"" + _msg + "\"};expires=" + Then.toGMTString() + ";domain=" + document.domain + ";path=/";
            } catch (e) {
            }
        });
    }
    else {
        var _tips = eval('(' + _mycnt + ')');
        _msg = _tips.SystemLastMessageTip;
        _favcnt = _tips.StoreUpdateCount;
    }
    if (_msg != "") {
        $("#jsstorecnt").html(_msg);
        $("#jsstorebg,#jsstoretxt").slideDown(1000);
        $("#jsstorecnt").attr("href", "http://login.sns.hongxiu.com/systemmessage/readmessage.aspx");
        setTimeout("jsstoreup()", 10000);
    }
    else if (_favcnt > 0) {
        $("#jsstorecnt").html("您的藏书架里有" + _favcnt + "本作品已经更新了");
        $("#jsstorebg,#jsstoretxt").slideDown(1000);
        setTimeout("jsstoreup()", 10000);
    }
    $("#jsstoreclose").click(function () {
        jsstoreup();
        document.cookie = "SystemTipCount={\"StoreUpdateCount\":0,\"SystemLastMessageTip\":\"\"};expires=" + Then.toGMTString() + ";domain=" + document.domain + ";path=/";
    });
}
function jsstoreup() {
    $('#jsstorebg,#jsstoretxt').slideUp(1000);
}
function addCookie(objName, objValue, objHours) {
    var str = objName + "=" + escape(objValue);
    if (objHours > 0) {
        var date = new Date();
        var ms = objHours * 3600 * 1000;
        date.setTime(date.getTime() + ms);
        str += "; expires=" + date.toGMTString();
    }
    document.cookie = str + ";domain=hongxiu.com;path=/";
    $("#pop_xz").css('display', 'none');
}
function getCookie(objName) {
    var arrStr = document.cookie.split("; ");
    for (var i = 0; i < arrStr.length; i++) {
        var temp = arrStr[i].split("=");
        if (temp[0] == objName)return unescape(temp[1]);
    }
}
function CheckDivClientCookie(name) {
    var str = getCookie(name);
    if (str == "1")
        $("#pop_xz").css('display', 'none'); else {
        addCookie(name, '1', '24');
        $("#pop_xz").css('display', 'block');
    }
}