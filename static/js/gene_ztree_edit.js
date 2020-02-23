var setting = {
	async:{
		enable: true,
		// url: "/file/upload_ztree/"+ztree_id,
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
		addHoverDom: addHoverDom,
		removeHoverDom: removeHoverDom,
		selectedMulti: false,   // 设置是否允许同时选中多个节点。默认值: true
	},
	callback:{
		onClick: onClick,
		onAsyncError: onAsyncError,
		onAsyncSuccess: onAsyncSuccess,
		beforeDrag: beforeDrag,    // 禁止拖拽行为
		beforeRemove: beforeRemove,  // 删除操作之前触发， 可阻止删除
		onRemove: onRemove,   // 删除操作结束之后触发
		beforeEditName: beforeEditName,  // 捕获编辑按钮的点击事件，确定是否允许进入编辑状态
	},
	edit: {
		enable: true,
		// 设置是否显示编辑名称按钮
		showRenameBtn: true,
		renameTitle: '编辑人物',
		removeTitle: '删除人物',
		// 节点编辑名称 input 初次显示时,设置 txt 内容是否为全选状态。
		editNameSelectAll: true,
	}
};

function getUrl(treeId, treeNode=null) {
	return "/file/upload_ztree/" + ztree_id;
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
				console.log(msg.data[i].deathday);
			}
			$("#treeDemo").show();
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
	showForm(treeNode, false);
	return false;  // 阻止后续的beforeReName函数
}

// 删除结点之前，判断是否该删除
function beforeRemove(treeId, treeNode){
	// console.log("beforeRemove");
	$('.delete_pop_title').show();
	node_id = treeNode.id;
	Node = treeNode;
	return false;
}

// 删除节点时，若是正在编辑的结点，就直接隐藏表单
function onRemove(e, treeId, treeNode){
	if(newNodeLayer.curNode == treeNode){
		hideForm();
	}
}

// 新增按钮的处理
var newCount = 1;
function addHoverDom(treeId, treeNode){
	// addHoverDom 回调函数可能会被多次触发
	var sObj = $("#" + treeNode.tId + "_span");

	// 所以一定要先判断该节点的新增按钮是否已经添加
	if ( treeNode.editNameFlag || $("#addBtn_"+treeNode.tId).length>0){
		return;
	}
	// 生成新增按钮的 html
	// 新增按钮的主要样式用ztree默认样式
	var addStr = "<span class='button add' id='addBtn_" + treeNode.tId + "'title='添加人物' onfocus='this.blur();'></span>";
	// 获取结点名称的DOM
	sObj.after(addStr);

	// 对 新增按钮绑定事件
	var btn = $("#addBtn_"+treeNode.tId);
	if(btn){
		btn.bind("click", function(){
			showSelectForm(treeNode);
			return false;
		});
	};
}

// 判断添加子节点还是兄弟节点
function addNodeType(treeNode, select){
	if(select)
		if (select == 'son') {
			// 添加子节点
			showForm(treeNode, true);
			return false;
		}
		else{ //添加兄弟节点
			// var zTree = $.fn.zTree.getZTreeObj("treeDemo");

			// 判断是否为独生子女
			// if(treeNode.seniority == 1 || treeNode.seniority == 2){
			// 	alert("该人物为独生子女，不可添加兄弟节点");
			// 	return;
			// }
			treeNode = treeNode.getParentNode();
			showForm(treeNode, true);
			return false;
		}

}
// 移除新增按钮
function removeHoverDom(treeId, treeNode){
	// 移除 新增按钮
	$("#addBtn_"+treeNode.tId).unbind().remove();
};

// 节点人物信息表单阅读
function personInfoShow(treeNode, addNodeFlag){
	console.log('personInfoShow');
	console.log(treeNode);
	// console.log("newNodeLayer.addNodeFlag " + newNodeLayer.addNodeFlag);
	console.log(treeNode.sex);
	if(!newNodeLayer.addNodeFlag){
		console.log(treeNode.firstname);
		$('#lastname').val(treeNode.lastname);
		$('#firstname').val(treeNode.firstname);
		$('#othername').val(treeNode.othername);
		$('#seniority').val(treeNode.seniority);
		console.log(treeNode.sex);
		if(treeNode.sex === false || treeNode.sex === 0){
			$('.sex_char_con .woman').removeClass('person_sex').prev().addClass('person_sex');
		}else {
			$('.sex_char_con .man').removeClass('person_sex').next().addClass('person_sex');
		}
		$('#spouse').val(treeNode.spouse);
		$('#birthday').val(treeNode.birthday);
		$('#deathday').val(treeNode.deathday);
		$('#desc').val(treeNode.desc);
		console.log(treeNode.birthday);
	}else{
		$('#lastname').val('王');
		$('#firstname').val('');
		$('#othername').val('');
		$('#seniority').val('');
		$('#new-node-layer input[type="radio"]').val('0');
		$('#spouse').val('');
		$('#birthday').val('');
		$('#deathday').val('');
		$('#desc').val('');
	}
}

// 显示结点信息编辑表单
function showForm(treeNode, addNodeFlag){
	console.log("showForm");
	// console.log(treeNode);
	treeNode = treeNode || {};
	newNodeLayer.curNode = treeNode;
	newNodeLayer.addNodeFlag = addNodeFlag;
	if(newNodeLayer.curNode){
		add_id = newNodeLayer.curNode.id;
	}
	// 判断是否是在添加子节点的过程中编辑表单
	// addNodeFlag 为true，则是； 为false，则只是纯粹编辑表单
	personInfoShow(treeNode, addNodeFlag);

	newNodeLayer.fadeIn();
	// 获取第一个nodeNameObj元素的焦点
	newNodeLayer.get(0).focus();
}

// 结点信息获取
function personInfoArrange(){
	var infoDict = {};
	infoDict.lastname= $('#lastname').val();
	infoDict.firstname = $('#firstname').val();
	infoDict.othername = $('#othername').val();
	infoDict.seniority = $('#seniority').val();
	infoDict.sex = sex;
	console.log(infoDict.sex);
	infoDict.spouse= $('#spouse').val();
	infoDict.birthday = $('#birthday').val();
	infoDict.deathday= $('#deathday').val();
	infoDict.desc = $('#desc').val();

	// 数据校验
	if(infoDict['lastname'].length === 0){
		alert('请填写人物姓氏');
		$('#lastname').focus();
		return;
	}
	if(infoDict['firstname'].length === 0){
		alert('请填写人物名字');
		$('#firstname').focus();
		return;
	}
	if(infoDict['seniority'].length === 0){
		alert('请选择人物排行');
		$('#seniority').focus();
		return;
	}
	infoDict['name'] = infoDict['lastname']+infoDict['firstname'];
	return infoDict;
}

// 节点属性的更新
function nodeUpdate(treeNode, zNode) {
	// console.log("nodeUpdate");
	treeNode.lastname = zNode.lastname;
	treeNode.firstname = zNode.firstname;
	treeNode.name = zNode.lastname + zNode.firstname;
	treeNode.othername = zNode.othername;
	treeNode.seniority = zNode.seniority;
	treeNode.sex = zNode.sex;
	if(zNode.sex === false){
		$('.sex_char_con .woman').removeClass('person_sex').prev().addClass('person_sex');
	}else {
		$('.sex_char_con .man').removeClass('person_sex').next().addClass('person_sex');
	}
	treeNode.spouse = zNode.spouse;
	treeNode.birthday = zNode.birthday.substr(0,10);
	treeNode.deathday = zNode.deathday.substr(0,10);
	treeNode.desc = zNode.desc;
	ztreeObj.updateNode(treeNode);
	return true;
}
// 结点信息编辑表单提交
function submitNewNode(){
	console.log("submitNewNode");
	// console.log(newNodeLayer.curNode);
	personInfo = personInfoArrange();
	// console.log(personInfo);

	// 首先判断是否在添加子节点的过程中编辑表单
	// addNodeFlag 为true，则是； 为false，则只是纯粹编辑表单
	if( newNodeLayer.addNodeFlag){
		// 判断是否是添加根节点, jQuery.isEmptyObject(newNodeLayer.curNode) 判定对象是否为空；若不是，进行后续判断
		if($.isEmptyObject(newNodeLayer.curNode)){
			newNodeLayer.curNode = null;
			add_id = 0;
		}
		// console.log(add_id);
		personInfo['id'] = add_id;
		personInfo['operate'] = 'add';

		// console.log(personInfo);

		$.ajax({
			url: "/file/upload_ztree/"+ ztree_id,
			type: 'post',
			// data: {'id': add_id, 'operate':'add', 'name': nodeName, 'desc': nodeInfo},
			data: personInfo,
			success: function (data) {
				if(data.res == 1){
					zNodes = data.successmsg[1];
					// console.log(zNodes);
					ztreeObj.addNodes(newNodeLayer.curNode, zNodes);
					ztreeObj.expandNode(newNodeLayer.curNode, true);
					storeFlag=false;
				}
				else{
					console.log(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});
	}
	else{
		console.log("edit_node");
		personInfo['id'] = newNodeLayer.curNode.id;
		personInfo['operate'] = 'edit';
		// console.log(personInfo);
		$.ajax({
			url: "/file/upload_ztree/"+ztree_id,
			type: 'post',
			data: personInfo,
			success: function (data) {
				// console.log(data);
				if(data.res == 1){
					// newNodeLayer.curNode = data.successmsg[1];
					// console.log(newNodeLayer.curNode);
					// ztreeObj.updateNode(newNodeLayer.curNode);
					// console.log(ztreeObj.updateNode(newNodeLayer.curNode));
					if (nodeUpdate(newNodeLayer.curNode, data.successmsg[1])){
						storeFlag=false;
					}
				}
				else{
					console.log(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});
	}
	// 保存后，隐藏表单
	hideForm();
}

// 隐藏结点信息编辑表单
function hideForm(){
	newNodeLayer.fadeOut();
}
// 显示根节点信息编辑表单
function showRootForm() {
	rootNodeLayer.fadeIn();
}
// 显示根节点信息组织
function rootPersonInfoArrange(){
	var infoDict = {};
	infoDict.lastname = $('#rootlastname').val();
	infoDict.firstname = $('#rootfirstname').val();
	infoDict.othername = $('#rootothername').val();
	infoDict.seniority = $('#rootseniority').val();
	// infoDict.sex = $('#root-node-layer input[type="radio"]:checked').val();
	infoDict.sex = sex;
	infoDict.spouse = $('#rootspouse').val();
	infoDict.birthday = $('#rootbirthday').val();
	infoDict.deathday = $('#rootdeathday').val();
	infoDict.desc = $('#rootdesc').val();

	console.log(infoDict.sex);
	// 数据校验
	if(infoDict['lastname'].length === 0){
		alert('请填写人物姓氏');
		$('#rootlastname').focus();
		return;
	}
	if(infoDict['firstname'].length === 0){
		alert('请填写人物名字');
		$('#rootfirstname').focus();
		return;
	}
	if(infoDict['seniority'].length === 0){
		alert('请选择人物排行');
		$('#rootseniority').focus();
		return;
	}
	infoDict.name = infoDict['lastname']+infoDict['firstname'];

	return infoDict;
}
// 根结点信息编辑表单提交
function submitRootNode(){
	rootPersonInfo = rootPersonInfoArrange();
	rootPersonInfo.id = 0;
	rootPersonInfo.operate = 'add';
	console.log(rootPersonInfo);
	$.ajax({
			url: "/file/upload_ztree/"+ ztree_id,
			type: 'post',
			data: rootPersonInfo,
			success: function (data) {
				if(data.res == 1){
					rootPersonInfo.pid = data.successmsg[1].pid;
					rootPersonInfo.id = data.successmsg[1].id;
					zNodes = rootPersonInfo;
					ztreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
					$('.add_root_person').hide();
					$("#treeDemo").show();
					storeFlag=false;
				}
				else{
					console(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});

	// 保存后，隐藏表单
	hideRootForm();
}

// 隐藏根结点信息编辑表单
function hideRootForm(){
	$('.add_root_person').fadeIn();
	rootNodeLayer.fadeOut();
}

// 显示添加节点类型选择表单显示
function showSelectForm(treeNode){
	treeNode = treeNode || {};
	selectLayer.curNode = treeNode;
	selectLayer.fadeIn();
}

// 节点类型选择表单提交
function submitSelect(nodetype){
	// 获取选择的结点类型
	select = nodetype;
	console.log(select);
	// 调用添加节点操作
	if(select){
		// 隐藏表单
		if(hideSelectForm()){
			addNodeType(selectLayer.curNode, select);
		}
	}
	else{
		flag = confirm('您的节点类型选择不正确，是否重新选择？');
		if(flag){
			return;
		}
	}
}

// 隐藏结点类型选择表单
function hideSelectForm(){
	selectLayer.fadeOut();
	return true;
}

var ztreeObj, zNodes=[], newNodeLayer,rootNodeLayer, selectLayer, storeFlag=true,add_id=0, ztree_id, sex=0,node_id,Node;
$(function () {
	ztree_id = $('.hidden').text();
	ztreeObj = $.fn.zTree.init($("#treeDemo"), setting);
	newNodeLayer = $('.new_node_layer_con');
	rootNodeLayer = $('.root_node_layer_con');
	selectLayer = $('.select_layer_con');
	$('.add_root_person').click(function () {
		showRootForm();
	});
	$('.man').click(function () {
		$('.sex_char_con .woman').removeClass('person_sex').prev().addClass('person_sex');
		sex = 0;
	});
	$('.woman').click(function () {
		$('.sex_char_con .man').removeClass('person_sex').next().addClass('person_sex');
		sex = 1;
	});

	$('.main_con .img_top .btn').click(function () {
		// console.log($('#article_title').val());
		if($('#article_title').val() == ''){
			alert("请填写世系表名称");
			return;
		}else {
			data = ztreeObj.getNodes();
			storeFlag = true;
			setTimeout(alert("保存成功"), 3000);
		}
	})
	$('.delete_pop_title .delete').click(function () {
		$.ajax({
			url: "/file/upload_ztree/" + ztree_id,
			type: 'post',
			data: {'id': node_id, 'operate':'delete'},
			success: function (data) {
				console.log(data);
				if(data.res == 1){
					ztreeObj.removeNode(Node);
					if(ztreeObj.getNodes() === null){
						$('.add_root_person').show();
					}
					storeFlag=false;
					$('.delete_pop_title').hide();
				}
				else{
					alert(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});
	})
});


