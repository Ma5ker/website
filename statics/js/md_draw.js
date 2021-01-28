//渲染js
$(document).ready(() => {
    showdown.setFlavor('github');
    var src = $('#post_content').text();
    var converter = new showdown.Converter({tables: true,'ghCodeBlocks': true});
    var html = converter.makeHtml(src);
    $('#post_content').html(html);
	//hljs.initHighlightingOnLoad();

	//设置table样式 -> bootstrap
	var tb = document.getElementsByTagName("table");
	for(var i=0;i<tb.length;i++){
		tb[i].classList.add("table");
		tb[i].classList.add("table-hover");
		tb[i].classList.add("table-responsive");
	}
	
	// 渲染完成后设置内容可见
	document.getElementById("post_content").style.display = "block";
})

//右下角返回顶部按钮
$(function(){
	$(window).scroll(function(){  //只要窗口滚动,就触发下面代码 
		var scrollt = document.documentElement.scrollTop + document.body.scrollTop; //获取滚动后的高度 
		if( scrollt >200 ){  //判断滚动后高度超过200px,就显示  
			$("#back_top").fadeIn(400); //淡出     
		}else{      
			$("#back_top").stop().fadeOut(400); //如果返回或者没有超过,就淡入.必须加上stop()停止之前动画,否则会出现闪动   
		}
	});
	$("#back_top").click(function(){ //当点击标签的时候,使用animate在200毫秒的时间内,滚到顶部
			$("html,body").animate({scrollTop:"0px"},200);
	});
});



