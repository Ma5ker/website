//文档加载完成时启动js渲染
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
			$("html,body").animate({scrollTop:"0px"},1000);
	});
});



//生成右下角导航栏
$(function(){

	var guide_content = `<li class="nav-item">`;
	var h2_href = `<a class="nav-link" href="#top-level-interfaces">第一部分</a>`;
	var h3_href = `
	<ol class="nav-item">
	<a class="nav-link" href="#the-loader">第1.1部分</a>
  	</ol>
	`;

	var h_tag = $("h2,h3");
	var len = h_tag.length;
	if (len==0){
		return;
	}
	var h2_index = 0;
	var h3_index = 1;
	for(var i=0;i<len;i++){
		cur_tag = h_tag[i];
		var id_href = "#"+cur_tag.id;
		var text_href = cur_tag.innerText;
		if (cur_tag.tagName=="H2"){
			if (h2_index!=0){
				guide_content += `
				</li>
				<li class="nav-item">
				`;
			}
			h2_index += 1;
			var h2_href = `<a class="nav-link" href="${id_href}">${h2_index} ${text_href}</a>`;
			guide_content += h2_href;
			h3_index = 1;
		}else{
			//二级标题放进去导致过长，暂时没想好怎么展示
			// var h3_href = `
			// 	<ol class="nav-item">
			// 	<a class="nav-link" href="${id_href}">${h2_index}.${h3_index} ${text_href}</a>
  			// 	</ol>
			// `;
			// guide_content += h3_href;
			// h3_index +=1;
		}
	}
	guide_content += `</li>`;
	$("ul#post_guide_gen").append(guide_content);
});
