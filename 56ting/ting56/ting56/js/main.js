
//返回顶部end

function FonHen_JieMa(u){
	var tArr = u.split("*");
	var str = '';
	for(var i=1,n=tArr.length;i<n;i++){
		str += String.fromCharCode(tArr[i]);
	}
	return str;
}

function getParam(strSource) {
	var datas2 =  FonHen_JieMa(strSource).split('&');
	var url = "";
	if(datas2[2]==='tc') {
        url = datas2[0].split('/');
        url = url[0] + '/' + url[1] + '/play_' + url[1] + '_' + url[2] + '.htm';
        console.log('JiemaUrl:', url);
    }

    return {"url":url};
}


// function viewplay(){
// 	if(datas[2]==='tudou'){
// 		fonhen_tudou_player(part,datas[0]);
// 	}else{
// 		fonhen_jplayer_player(part,datas[0]);
// 	}
// }







function getAspParas(suffix){
	var cur_url=location.href;
	var urlParas=location.search;
	if (cur_url.indexOf("?")>0){
		return urlParas.substring(1,urlParas.indexOf(suffix)).split('-')
	}else{
		return cur_url.substring(cur_url.lastIndexOf("/")+1,cur_url.indexOf(suffix)).split('-')	
	}
}

function FonHen_UpData(){
	var n = param[2];
	var u=window.location.href;
	var arr_u=u.split("/");
		u = u.replace(arr_u[arr_u.length-1],"");
    if(n==0){
		alert(unescape('\u5DF2\u7ECF\u662F\u7B2C\u4E00\u96C6\u4E86'));}
	else{ 
		var n=n-1;
		window.location.href = u+param[0]+"-"+param[1]+"-"+n+".html";
	}
}




