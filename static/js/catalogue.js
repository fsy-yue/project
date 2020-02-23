function addTitle(title){
	if(book_id){
		if (addTypeFlag == 'title') {
			$.ajax({
				url :"/family/title",
				type : 'post',
				dataType:"json",
				data:{'book_id': book_id, 'cata_id': cata_id, 'type':addElemType, 'operate': 'add', 'title': title},
				success : function(data, status, xhr) {
					if(data.res == 1){
						var a_url;
						if(addElemType == 'img'){
							a_url = "/file/upload_img/" + data.successmsg;
						}
						if(addElemType == 'article'){
							a_url = "/file/upload_file/" + data.successmsg;
						}
						if(addElemType == 'ztree'){
							a_url = "/file/upload_ztree/" + data.successmsg;
						}
						console.log(a_url);
						var add_elem= $('<ul class="title_level title_level_' + addTitleRank + '"><li type="' + addElemType +'"><a href="'+ a_url + '" bookid="'+ data.successmsg +'">' +
										'<span class="article_title" >'+ title + '</span></a><span class="article_edit">' +
										'</span><span class="article_delete"></span></li></ul>');
						addInitiatorElem.parent().next().append(add_elem);
						addInitiatorElem.parent().next().slideDown();
					}else {
						alert(data.errormsg);
					}
				},
				error : function(xhr, errorType, error) {
					alert("数据保存失败，请重试");
				}
			})
		}
		else{
			if (addTypeFlag == 'cata') {
				$.ajax({
					url :"/family/catalogue",
					type : 'post',
					dataType:"json",
					data:{'book_id': book_id, 'type':addElemType, 'operate': 'add', 'title': title},
					success : function(data, status, xhr) {
						if(data.res == 1){
							console.log(data.successmsg);
							// alert(data.successmsg);
							var add_elem= $('<ul class="cata_level"><li type="' + addElemType +'"><span class="cata_drop_up" asyncid="1"></span>' +
											'<span class="cata_title" bookid="'+ data.successmsg +'">'+ title+ '</span><span class="cata_edit"></span>' +
											'<span class="cata_delete"></span><span class="cata_add_title"></span></li>' +
											'<div class="div_2"></div></ul>');
							addInitiatorElem.parent().next().append(add_elem);
							addInitiatorElem.parent().next().slideDown();
						}else {
							alert(data.errormsg);
						}
					},
					error : function(xhr, errorType, error) {
						alert("数据保存失败，请重试");
					}
				})
			}
			else{
				return;
			}
		}
		if (addTitleRank == 1) {
			addInitiatorElem.parent().find('.drop_down').removeClass('drop_down').addClass('drop_up');
		}
		else{
			if(addTitleRank == 2){
				addInitiatorElem.parent().find('.cata_drop_up').removeClass('cata_drop_up').addClass('cata_drop_down');
			}
		}
	}else {
		alert("请先添加谱书信息");
	}
	return true;			
}
function editTitle(title){
	if (editTypeFlag == 'cata'){
		$.ajax({
			url :"/family/catalogue",
			type : 'post',
			dataType:"json",
			data:{'cata_id': cata_id, 'type':editElemType, 'operate': 'edit', 'title': title},
			success : function(data, status, xhr) {
				if(data.res == 1){
					console.log(data.successmsg);
					// alert(data.successmsg);
					editInitiatorElem.prev().text(title);
				}else {
					alert(data.errormsg);
				}
			},
			error : function(xhr, errorType, error) {
				alert("修改失败，请重试");
			}
		})
	}
	else {
		if(editTypeFlag == 'article'){
			$.ajax({
				url :"/family/title",
				type : 'post',
				dataType:"json",
				data:{'article_id': article_id, 'type':editElemType, 'operate': 'edit', 'title': title},
				success : function(data, status, xhr) {
					if(data.res == 1){
						console.log(data.successmsg);
						// alert(data.successmsg);
						editInitiatorElem.prev().children().text(title);
					}else {
						alert(data.errormsg);
					}
				},
				error : function(xhr, errorType, error) {
					alert("修改失败，请重试");
				}
			})
		}
		else {
			return false;
		}
	}
	return true;
}
function deleteTitle(){
	if (deleteTypeFlag == 'cata'){
		$.ajax({
			url :"/family/catalogue",
			type : 'post',
			dataType:"json",
			data:{'cata_id': cata_id, 'type':deleteElemType, 'operate': 'delete'},
			success : function(data, status, xhr) {
				if(data.res == 1){
					console.log(data.successmsg);
					// alert(data.successmsg);
					deleteInitiatorElem.parent().parent().remove();
				}else {
					alert(data.errormsg);
				}
			},
			error : function(xhr, errorType, error) {
				alert("修改失败，请重试");
			}
		})
	}
	else {
		if(deleteTypeFlag == 'article'){
			$.ajax({
				url :"/family/title",
				type : 'post',
				dataType:"json",
				data:{'article_id': article_id, 'type':deleteElemType, 'operate': 'delete'},
				success : function(data, status, xhr) {
					if(data.res == 1){
						console.log(data.successmsg);
						// alert(data.successmsg);
						deleteInitiatorElem.parent().parent().remove();
					}else {
						alert(data.errormsg);
					}
				},
				error : function(xhr, errorType, error) {
					alert("修改失败，请重试");
				}
			})
		}
		else {
			return false;
		}
	}
	return true;
}
function closeInput(){
	$('.input_pop').fadeOut();
	inputShowFlag = false;
}

var addTypeFlag, editTypeFlag, deleteTypeFlag, addElemType, editElemType, deleteElemType, cata_id='0', article_id,
	addInitiatorElem,editInitiatorElem,deleteInitiatorElem, addTitleRank=0, inputShowFlag=false;
$(function(){
	//  添加目录和文章标题部分
	$('.add_title').click(function(){
		if (!inputShowFlag) {
			addInitiatorElem = $(this);
			addElemType = $(this).parent().prop('type');
			addTypeFlag = 'title';    // 用于判断发起何种ajax请求
			addTitleRank = 1;		// 用于判断添加标题的等级
			// cata_id = '';      // 添加一级标题，cata_id为空
			inputShowFlag = true;
			$('.input_pop').show();
		}else{
			alert("请先关闭标题输入弹窗");
		}
	});
	$('.add_cata').click(function(){
		if(!inputShowFlag){
			addInitiatorElem = $(this);
			addElemType = $(this).parent().prop('type');
			addTypeFlag = 'cata';
			addTitleRank = 0;
			$('.input_pop').show();
		}else{
			alert("请先关闭标题输入弹窗");
		}
	});
	// 目录是后来加进去的，所以需要事件委托
	$('.catalogue_con').delegate('.cata_add_title', 'click', function(){
		console.log(".cata_add_title");
		if (!inputShowFlag) {
			$('.input_pop').show();
			addInitiatorElem = $(this);
			addElemType = $(this).parent().prop('type');
			addTypeFlag = 'title';
			addTitleRank = 2;
			cata_id = $(this).parent().find('.cata_title').attr('bookid');
			console.log(cata_id);
			inputShowFlag = true;
			$('.input_pop').show();
		}else{
			alert("请先关闭标题输入弹窗");
		}
	})
	$('.input_pop .reset').click(function(){
		closeInput();
	});
	$('.input_pop .submit').click(function(){
		title = $('.input_pop .title').val();
		if (addTitle(title)) {
			closeInput();
		}
	});

	//  编辑目录标题和文章标题部分
	$('.catalogue_con').delegate('.article_edit', 'click', function(){
		editInitiatorElem = $(this);
		editElemType = $(this).parent().prop('type');
		editTypeFlag = 'article';
		article_id = $(this).prev().attr('bookid');
		// console.log(article_id);
		console.log($(this).prev().text());
		$('.title_edit_con input').val($(this).parent().find('.article_title').text());
		$('.title_edit_con').show();
	})
	$('.catalogue_con').delegate('.cata_edit', 'click', function(){
		editInitiatorElem = $(this);
		editElemType = $(this).parent().prop('type');
		editTypeFlag = 'cata';
		cata_id = $(this).prev().attr('bookid');
		console.log($(this).prev().text());
		$('.title_edit_con input').val($(this).parent().find('.article_title').text());
		$('.title_edit_con').show();
	})	
	$('.title_edit_con .submit').click(function(){
		title = $('.title_edit .title').val();
		if (editTitle(title)) {
			$('.title_edit_con').hide();
		}
	})
	$('.title_edit_con .reset').click(function(){
		$('.title_edit_con').hide();
	})

	// 删除目录和文章部分
	$('.catalogue_con').delegate('.article_delete', 'click', function(){
		deleteInitiatorElem = $(this);
		deleteElemType = $(this).parent().prop('type');
		deleteTypeFlag = 'article';       // 用于前端发起何种ajax请求使用
		article_id = $(this).parent().find('a').attr('bookid');
		$('.delete_pop_title').show();
	})
	$('.catalogue_con').delegate('.cata_delete', 'click', function(){
		deleteInitiatorElem = $(this);
		deleteElemType = $(this).parent().prop('type');
		deleteTypeFlag = 'cata';    // 用于前端发起何种ajax请求使用
		cata_id = $(this).parent().find('.cata_title').attr('bookid');
		$('.delete_pop_cata').show();
	})

	$('.delete_pop_cata .delete').click(function(){
		if (deleteTitle()) {
			$('.delete_pop_cata').hide();
		}
	})
	$('.delete_pop_title .delete').click(function(){
		if (deleteTitle()) {
			$('.delete_pop_title').hide();
		}
	})

	$('.delete_pop_cata .reset').click(function(){
		$('.delete_pop_cata').hide();
	})
	$('.delete_pop_title .reset').click(function(){
		$('.delete_pop_title').hide();
	})
	

	//  目录和文章伸展收缩部分
	$('.catalogue_con').delegate('.drop_up', 'click', function(){
		$(this).parent().next().slideUp(500);
		$(this).removeClass('drop_up').addClass('drop_down');
	})
	$('.catalogue_con').delegate('.drop_down', 'click', function(){
		$(this).parent().next().slideDown(500);
		$(this).removeClass('drop_down').addClass('drop_up');
	})
	$('.catalogue_con').delegate('.cata_drop_down', 'click', function(){
		$(this).parent().next().slideUp(500);
		$(this).removeClass('cata_drop_down').addClass('cata_drop_up');
	})
	$('.catalogue_con').delegate('.cata_drop_up', 'click', function(){
		thisCon = $(this);
		asyncFlag = parseInt($(this).attr("asyncid"));
		if (asyncFlag){
			cata_id = $(this).parent().find('.cata_title').attr('bookid');
			asyncElem = $(this).parent().prop('type');
			$.ajax({
				url :"/family/catalogue",
				type : 'get',
				dataType:"json",
				data:{'cata_id': cata_id, 'type':asyncElem},
				success : function(data, status, xhr) {
					if(data.res == 1){

						if($('.hidden').text()){     // $('.hidden').text()不为空，表示为创建家谱异步加载
							var a_url;
							if(asyncElem == 'img'){
								a_url = "/file/upload_img/"
							}
							if(asyncElem == 'article'){
								a_url = "/file/upload_file/"
							}
							if(asyncElem == 'ztree'){
								a_url ="/file/upload_ztree/"
							}
							for (var i=0; i<data.successmsg.length; i++){
								var add_elem= $('<ul class="title_level title_level_2"><li type="' + asyncElem +'"><a href="'+ a_url +data.successmsg[i].id +'" bookid="'+ data.successmsg[i].id +'">' +
											'<span class="article_title" >'+ data.successmsg[i].name + '</span></a><span class="article_edit">' +
											'</span><span class="article_delete"></span></li></ul>');
								thisCon.parent().next().append(add_elem);
							}
						}else {				// $('.hidden').text()为空，表示为查看家谱异步加载
							var a_url;
							if(asyncElem == 'img'){
								// a_url = "'file:show_img'"
								a_url = "/file/show_img/"
							}
							if(asyncElem == 'article'){
								// a_url = "'file:show_file'"
								a_url = "/file/show_file/"
							}
							if(asyncElem == 'ztree'){
								a_url ="/file/show_ztree/"
							}
							for (var i=0; i<data.successmsg.length; i++){
								var add_elem= $('<ul class="title_level title_level_2"><li type="' + asyncElem +'"><a href="'+ a_url +data.successmsg[i].id +'" bookid="'+ data.successmsg[i].id +'">' +
											'<span class="article_title" >'+ data.successmsg[i].name + '</span></a></li></ul>');
								thisCon.parent().next().append(add_elem);
							}
						}
						thisCon.attr("asyncid", 0);
						thisCon.parent().next().slideDown();
						thisCon.removeClass('cata_drop_up').addClass('cata_drop_down');
				}else {
						alert(data.errormsg);
					}
				},
				error : function(xhr, errorType, error) {
					alert("数据保存失败，请重试");
				}
			})
		} else {
			$(this).parent().next().slideDown(200);
			$(this).removeClass('cata_drop_up').addClass('cata_drop_down');
		}
	})

	// 移入移出变色部分
  	$('.catalogue_con').delegate('li','mouseenter',function(){
        $(this).css('backgroundColor', '#f2f2f2');
        $('.li_1').css('backgroundColor', '#E8EAF6');
        return false;
    })
    $('.catalogue_con').delegate('li','mouseleave',function(){
        $(this).css('backgroundColor', 'white');
        $('.li_1').css('backgroundColor', '#E8EAF6');
        return false;
    })
})
