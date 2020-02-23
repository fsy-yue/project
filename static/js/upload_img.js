var imgSrc = []; //保存图片url地址
var imgFile = []; //保存图片流
var imgName = []; //保存图片名称
var imgDetail = []; //保存file描述信息
var formFile = new FormData();  //用于向后台传送数据
var pageCount = 0;   //分页数量
var imgCount = 0;   //记录上传图片的个数
var imgContainer = [];   // 所有上传的imgContainer
var delElem,imgdb_id,img_id;
//上传图片
function imgUpload(obj) {
	var oInput = '#' + obj.inputId;
	var imgBox = '#' + obj.imgBox;
	var btn = '#' + obj.buttonId;

	$(oInput).on("change", function() {
		var fileImg = $(oInput)[0];
		var fileList = fileImg.files;
		for(var i = 0; i < fileList.length; i++) {
			var imgSrcI = getObjectURL(fileList[i]);
			imgName.push(fileList[i].name);
			imgSrc.push(imgSrcI);
			imgFile.push(fileList[i]);
		}
		addNewContent(imgBox);
		storeFlag = false;
	})
}
	
//向imgBox中添加元素，实现图片预览
function addNewContent(obj) {
	for(var a = 0; a < imgSrc.length; a++) {
		var oldBox = $(obj).html();
		$(obj).html( oldBox + '<div class="imgContainer"" >' +
			'\<img imgid="0" title=' + imgName[a] + ' alt=' + imgName[a] + ' src=' + imgSrc[a] + '>' +
			'<span class="imgDelete" deleteid="'+ a +'">删除</span>' +
			'<span class="discription">点击添加图片描述</span><div class="img_dis_pop_con">' +
			'<div class="img_dis_pop"><h4>添加图片描述<span class="close">x</span></h4>' +
			'<textarea name="img_dis" value="" placeholder="请输入图片描述"></textarea>' +
			'<button class="btn btn-default submit">确定</button>' +
			'<button class="btn btn-default reset">取消</button></div>' +
			'<div class="mask"></div></div></div>');
	}
	imgSrc = [];  // 添加完成，清除图片源
	imgName = []; // 添加完成，清除图片源
	imgContainer = $('.imgContainer');
	pageShow(imgBox);
}

function pageShow(obj){

	imgCount = parseInt(imgContainer.length);
	if(imgCount%12 == 0){
		pageCount = parseInt(imgCount/12);
	}else{
		pageCount = parseInt(imgCount/12)+1;
	}
	$("#page").paging({
		pageNo:1,
		totalPage: pageCount,
		totalSize: imgCount,
		callback: function(num) {
			var i=parseInt((num-1)*12);

			var left = imgCount - i;
			if(left > 12){ left = 12;}

			var top = parseInt(i) + parseInt(left);

			$(imgBox).html("");
			while(i < top){
				obj.appendChild(imgContainer[i]);
				i++;
			}
		}
	})	
}

//删除结点
function closePicture(obj) {
	$(obj).parent("div").remove();
}

//获取图片路径
function getObjectURL(file) {
	var url = null;
	if(window.createObjectURL != undefined) { // basic
		url = window.createObjectURL(file);
	} else if(window.URL != undefined) { // mozilla(firefox)
		url = window.URL.createObjectURL(file);
	} else if(window.webkitURL != undefined) { // webkit or chrome
		url = window.webkitURL.createObjectURL(file);
	}
	return url;
}

//组织向后台传送的数据
function Data(){
	imgDetail = [];    // 每一次传输数据，都将上一次的清空

	$(".discription").each(function(){
		var imgid = $(this).parent().find('img').attr('imgid');
		if (imgid == '0'){
			var detail = $(this).text();
			if(!detail || detail == "点击添加图片描述"){
				detail = "该图片无描述信息"
			};
			imgDetail.push(detail);
		}
	});
	// console.log(imgDetail);

	$.each(imgFile, function(i, file){
		formFile.append('files', file);
	});
	$.each(imgDetail, function (i, file) {
		formFile.append('details',file);
	});
	// eachFormData(formFile);

	return true;
}

function eachFormData(formData) {
    var entriesObj = formData.entries();
    var loopEntrie = entriesObj.next();
    var loopValue = "";
    /** done 为 true 时 表示已经遍历完毕 */
    while (!loopEntrie["done"]) {
        loopValue = loopEntrie["value"];
        loopEntrie = entriesObj.next();
        console.log(loopValue[0] + "=" + loopValue[1]);
    }
}

function DelePicture(){
	console.log(img_id);
	console.log(delElem);
	if (img_id == "0"){
		index = delElem.attr('deleteid');
		imgSrc.splice(index, 1);
		imgFile.splice(index, 1);
		imgName.splice(index, 1);
		$('.delete_pop_title').fadeOut();
		delElem.remove();
	} else {
		$.ajax({
			url: "/file/upload_img/"+imgdb_id,
			type: "post",
			headers:{"X-CSRFToken":$.cookie('csrftoken')},  //这是把csrf传入服务器.
			data: {'operate': 'delete', 'img_id': img_id},
			dataType: 'json',
			success: function (data) {
				if (data.res == 1) {
					console.log(data.successmsg);
					storeFlag = true;
					location.href = "/file/upload_img/"+imgdb_id;
				} else {
					alert(data.errmsg);
				}
			}
		});
	}
	return true;
}

$(function(){
	
	$('.return span ').click(function(){
		if(storeFlag){
			book_id = $(this).attr("bookid");
			location.href = '/family/create/'+book_id;
		}else{
			$('.return_pop_con').fadeIn();
		}
		return false;
	});

	$('.return_pop').click(function(){
		return false;
	})
	$('img_dis_pop').click(function(){
		return false;
	})
	
	$('.close').click(function(){
		$(this).parent().parent().parent().fadeOut();
	})

	$('.return_pop .reset').click(function(){
		$(this).parent().parent().fadeOut();
	})
	$('.return_pop .submit').click(function(){
		book_id = $('.return span').attr("bookid");
		location.href = '/family/create/'+book_id;
	});

	// 事件委托
	$('#imgBox').delegate('.discription', 'click', function(){
		// $(this).parent().parent().parent().fadeOut();
		console.log($(this));
		var discription = $(this).text();
		console.log(discription);
		$(this).next().find('textarea').val(discription);
		$(this).next().fadeIn();
		return false;
	})
	
	$('#imgBox').delegate('.img_dis_pop .close', 'click', function(){
		$(this).next().fadeIn();
		return false;
	})

	$('#imgBox').delegate('.img_dis_pop .reset', 'click', function(){
		// discription = $(this).parent().parent().prev();
		$(this).prev().prev().val("");
		// discription.text('点击添加图片描述');
		$(this).parent().parent().fadeOut();
	})

	$('#imgBox').delegate('.img_dis_pop .submit', 'click', function(){
		imgdb_id = $('.hidden').attr('imgdbid');
		detail = $(this).prev().val();
		discription = $(this).parent().parent().prev();
		img_id = $(this).parents('.imgContainer').find('img').attr('imgid');
		if(detail){
			if (img_id == "0"){
				discription.text(detail);
			} else {
				$.ajax({
					url: "/file/upload_img/"+imgdb_id,
					type: "post",
					headers:{"X-CSRFToken":$.cookie('csrftoken')},  //这是把csrf传入服务器.
					data: {'operate': 'edit', 'detail': detail,'img_id': img_id},
					dataType: 'json',
					success: function(data) {
						if (data.res == 1){
							console.log(data.successmsg);
							discription.text(detail);
							storeFlag = true;
						}else {
							alert(data.errmsg);
						}
					}
				});
			}
		}else{
			discription.text('点击添加图片描述');
		}
		$(this).parents('.img_dis_pop_con').hide();
	});

	$('#imgBox').delegate('.imgDelete','click', function () {
		imgdb_id = $('.hidden').attr('imgdbid');
		img_id = $(this).parents('.imgContainer').find('img').attr('imgid');
		delElem = $(this);
		console.log(img_id);
		$('.delete_pop_title').fadeIn();
	})

	$('.delete_pop .delete').click(function () {
		DelePicture();
	})

	$('#page a').click(function(){
		$('.imgContainer').fadeOut();
	})

})


