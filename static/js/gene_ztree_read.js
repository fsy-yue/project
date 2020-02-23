var setting = {
	async:{
		enable: true,
		// url: "/file/show_ztree/"+ztree_id,
		url: getUrl,
		type: 'get',
		dataFilter: filter,
	},
	data: {
		simpleData: {
			enable: true,
			idKey: "id",
			pIdKey: "pid",
			rootPId: 0,
		},
		keep:{
			parent: true,
		}
	},
	view:{
		dblClickExpand: false,  // 取消默认双击展开父节点功能
		selectedMulti: false,   // 设置是否允许同时选中多个节点。默认值: true
	},
	callback:{
		onClick: onClick,
		onAsyncError: onAsyncError,
		onAsyncSuccess: onAsyncSuccess,
		beforeDrag: beforeDrag,    // 禁止拖拽行为
		beforeEditName: beforeEditName,  // 捕获编辑按钮的点击事件，确定是否允许进入编辑状态
	},
	edit: {
		enable: true,
		// 设置是否显示编辑名称按钮
		showRenameBtn: true,
		renameTitle: '查看人物信息',
		showRemoveBtn: false,
		editNameSelectAll: true,
	}
};
function getUrl(treeId, treeNode=null) {
	return "/file/show_ztree/" + ztree_id;
}
function filter(treeId, parentNode, childNodes) {
	if (!childNodes){
		console.log("null");
		return null;
	}
	return childNodes;
}

var InitFlag = true;
function onAsyncSuccess(event, treeId, treeNode, msg) {
	if(InitFlag){			// 初始化
		msg = $.parseJSON(msg);
		if(msg.res == 1){		// 返回值为1，说明返回值中含有数据，
			for(var i=0; i<msg.data.length; i++){
				zNodes.push(msg.data[i]);
				// console.log(msg.data[i].deathday);
			}
			$("#treeDemo").show();
			// $.fn.zTree.init($("#treeDemo"), setting, zNodes);
			console.log(zNodes);
			var treeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
			treeObj.expandAll(true);
		}
		else {
			$('.add_root_person').show();
		}
		InitFlag = false;
	}
}
function onAsyncError(event, treeId, treeNode, XMLHttpRequest, textStatus, errorThrown) {
	alert("异步获取数据出现异常。");
}
function onClick(e,treeId, treeNode) {
	console.log("onClick");
	ztreeObj.expandNode(treeNode);
}
// Demo 中禁止拖拽操作
function beforeDrag(treeId, treeNodes){
	return false;
}

// 让表单同时具有编辑节点的功能
// 利用beforeEditName 回调函数，编辑ztree默认编辑行为
function beforeEditName(treeId, treeNode){
	// 选中指定节点
	// ztreeObj.selectNode(treeNode,addFlag,isSilent);
	ztreeObj.selectNode(treeNode);
	showForm(treeNode);
	return false;  // 阻止后续的beforeReName函数
}

// 组织节点人物信息
function personInfoArrange(treeNode){
	console.log(treeNode);
	$('#lastname').val(treeNode.lastname);
	$('#firstname').val(treeNode.firstname);
	$('#othername').val(treeNode.othername);
	rank = ['独生子','独生子','独生女','第一','第二','第三','第四','第五','第六','第七','第八','第九','第十','第十一','第十二'];
	$('#seniority').text(rank[treeNode.seniority]);
	if(treeNode.sex === false){
		console.log(treeNode.sex);
		$('.sex_char_con .woman').removeClass('person_sex').prev().addClass('person_sex');
	}else {
		$('.sex_char_con .man').removeClass('person_sex').next().addClass('person_sex');
	}
	$('#spouse').val(treeNode.spouse);
	$('#birthday').val(treeNode.birthday);
	$('#deathday').val(treeNode.deathday);
	$('#desc').val(treeNode.desc);
	return true;
}

// 显示结点信息编辑表单
function showForm(treeNode, addNodeFlag){
	if(personInfoArrange(treeNode)){
		newNodeLayer.fadeIn();
	}else {
		alert("人物信息获取失败");
	}
}

// 隐藏结点信息编辑表单
function hideForm(){
	newNodeLayer.fadeOut();
}

var ztreeObj, zNodes=[], newNodeLayer, ztree_id;
$(function () {
	ztree_id = $('.hidden').text();
    // console.log(ztree_id);
	person_node_id = $('.search').attr('nodeid');
	if (person_node_id != ''){
		person_rank = $('.search').attr('rankid');
		$.ajax({
			url: "/search/person",
			type: 'post',
			data: {'node_id': person_node_id},
			success: function (data) {
				if(data.res == 1){
					zNodes = data.successmsg;
					$('.tree_title li').each(function (index, element) {
						if (index < person_rank-1){
							$(this).hide();
						}else {
							$(this).show();
						}
					})
					ztreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
					ztreeObj.expandAll(true);
					$('#treeDemo').show();
				}
				else{
					console.log(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});
	} else {
		ztreeObj = $.fn.zTree.init($("#treeDemo"), setting);
	}
	newNodeLayer = $('#new-node-layer');
	$('.search_result .close').click(function () {
		$('.search_result').hide();
		$('.persons').html('');
	})
	$('.search_input').focus(function () {
		$('.search_result').hide();
		$('.persons').html('');
	})
	$('.search_input').keypress(function () {
		q = $(this).val();
		$.ajax({
			url: "/search/person",
			type: 'get',
			data: {'id': ztree_id,'q': q, 'where': 'ztree'},
			success: function (data) {
				if(data.res == 1){
					persons = data.successmsg;
					$('.persons').html('');
					$('.search_result h1').text('搜索结果');
					for (var i = 0; i<persons.length; i++){
						var li;
						if(persons[i].rank == 1){
							li = '<li class="person" nodeid=" '+ persons[i].node_id +'"><span class="name">'+
								persons[i].name + '</span><span class="desc">第<em>'+ persons[i].rank +'</em>世，根节点人物</span></li>'
						}
						else {
							li = $('<li class="person" nodeid="'+ persons[i].node_id +'"><span class="name">'+
								persons[i].name + '</span><span class="desc">第<em>'+ persons[i].rank +'</em>世，其父为'+
								persons[i].parent+' '+ persons[i].brank + '</span></li>')
						}
						$('.persons').append(li);
					}
				}
				else{
					$('.persons').html('');
					$('.search_result h1').text(data.errmsg);
				}
				$('.search_result').show();
			},
			error: function () {
				console.log('error');
			}
		});
	})
	$('.search_icon').click(function () {
		q = $(this).prev().val();
		$.ajax({
			url: "/search/person",
			type: 'get',
			data: {'id': ztree_id,'q': q, 'where': 'ztree'},
			success: function (data) {
				if(data.res == 1){
					persons = data.successmsg;
					$('.persons').html('');
					for (var i = 0; i<persons.length; i++){
						var li;
						if(persons[i].rank == 1){
							li = '<li class="person" nodeid=" '+ persons[i].node_id +'"><span class="name">'+
								persons[i].name + '</span><span class="desc">第<em>'+ persons[i].rank +'</em>世，根节点人物</span></li>'
						}
						else {
							li = $('<li class="person" nodeid="'+ persons[i].node_id +'"><span class="name">'+
								persons[i].name + '</span><span class="desc">第第<em>'+ persons[i].rank +'</em>世，其父为'+
								persons[i].parent+' '+ persons[i].brank + '</span></li>')
						}
						$('.persons').append(li);
					}
				}
				else{
					$('.search_result h1').text('查无此人');
				}
				$('.search_result').show();

			},
			error: function () {
				console.log('error');
			}
		});
	})
	$('.search_result').delegate('li','click', function () {
		person_node_id = $(this).attr('nodeid');
		person_rank = $(this).find('em').text();
		console.log(person_node_id);
		$.ajax({
			url: "/search/person",
			type: 'post',
			data: {'node_id': person_node_id},
			success: function (data) {
				if(data.res == 1){
					zNodes = data.successmsg;
					// console.log(zNodes);
					console.log(person_rank);
					$('.tree_title li').each(function (index, element) {
						console.log(index);
						if (index < person_rank-1){
							$(this).hide();
						}else {
							$(this).show();
						}
					})
					var treeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
					treeObj.expandAll(true);
				}
				else{
					console.log(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});
	})
	$('.return_cata ').click(function(){
		book_id = $(this).attr("bookid");
		location.href = '/family/read/'+book_id;
	});
})
