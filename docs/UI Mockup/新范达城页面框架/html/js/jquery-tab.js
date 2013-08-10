$(function () {
	$('.tabTitle li').click(function () {
		$(this).addClass("tabin").siblings().removeClass();
		$(".tabContent > ul").eq($(".tabTitle li").index(this)).show().siblings().hide();
	});
});