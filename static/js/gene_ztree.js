var setting = {
	// async:{
	// 	enable: true,
	// 	url: "/family/ztree",
	// 	type: 'get',
	// 	dataFilter: filter,
	// },
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

function getUrl(treeId, treeNode=null,operate) {
	// operate: 1.删除，2.添加，3，编辑
	var param;
	if(treeNode){
		param = "id="+treeNode.id+"&operate=1";
		// param = "id="+treeNode.id+"&operate=1"+ operate;
	}
	else {
		param = "id=0";
	}
	console.log(param);
	return "/family/ztree?" + param;
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
	data = $.parseJSON(msg);  // 使用Ajax的转换对象
	for(var i=0; i<data.zNodes.length; i++){
		zNodes.push(data.zNodes[i]);
	}
	console.log(zNodes);
	if(InitFlag){
		$.fn.zTree.init($("#treeDemo"), setting, zNodes);
		var i,j,node;
		// 加载根节点时， treeNode是不存在的，需要处理
		var nodes = treeNode?treeNode.children: ztreeObj.getNodes();
		console.log(nodes);
		for(i=0, j=nodes.length; i<j; i++){
			node = nodes[i];
			if(node.isParent){
				ztreeObj.expandNode(node,true,false,false);
			}
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
	console.log("beforeRemove");
	if(treeNode.children){
		 if(!confirm("该节点仍有子孙节点，您确定要删除吗？")){
			return false;
		 }
	}
	$.ajax({
		url: "/family/ztree",
		type: 'post',
		data: {'id': treeNode.id, 'operate':'delete'},
		success: function (data) {
			console.log(data);
			if(data.res == 1){
				ztreeObj.removeNode(treeNode);
				// alert(data.successmsg);
			}
			else{
				// alert(data.errmsg);
			}
		},
		error: function () {
			console.log('error');
		}
	});
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
			var zTree = $.fn.zTree.getZTreeObj("treeDemo");
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

// 显示结点信息编辑表单
function showForm(treeNode, addNodeFlag){
	treeNode = treeNode || {};
	newNodeLayer.curNode = treeNode;
	newNodeLayer.addNodeFlag = addNodeFlag;
	if(newNodeLayer.curNode){
		add_id = newNodeLayer.curNode.id;
	}
	// 判断是否是在添加子节点的过程中编辑表单
	// addNodeFlag 为true，则是； 为false，则只是纯粹编辑表单
	if(!newNodeLayer.addNodeFlag){
		nodeNameObj.val(treeNode.name);
		nodeInfoObj.val(treeNode.info);
	}else{
		nodeNameObj.val('');
		nodeInfoObj.val('');
	}

	newNodeLayer.fadeIn();
	// 获取第一个nodeNameObj元素的焦点
	nodeNameObj.get(0).focus();
}

// 结点信息编辑表单提交
function submitNewNode(){
	var nodeName = nodeNameObj.val();
	var nodeInfo = nodeInfoObj.val();
	// 数据校验
	if(nodeName.length === 0){
		alert('名称不允许为空！');
		return;
	}
	// 首先判断是否在添加子节点的过程中编辑表单
	// addNodeFlag 为true，则是； 为false，则只是纯粹编辑表单
	if( newNodeLayer.addNodeFlag){
		// 判断是否是添加根节点, jQuery.isEmptyObject(newNodeLayer.curNode) 判定对象是否为空；若不是，进行后续判断
		if($.isEmptyObject(newNodeLayer.curNode)){
			newNodeLayer.curNode = null;
			add_id = 0;
		}

		$.ajax({
			url: "/family/ztree",
			type: 'post',
			data: {'id': add_id, 'operate':'add', 'name': nodeName, 'desc': nodeInfo},
			success: function (data) {
				if(data.res == 1){
					ztreeObj.addNodes(newNodeLayer.curNode, data.successmsg[1]);
					console.log(data.successmsg[0]);
					console.log(data.successmsg[1]);

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
		$.ajax({
			url: "/family/ztree",
			type: 'post',
			data: {'id': newNodeLayer.curNode.id, 'operate':'edit', 'name': nodeName, 'desc': nodeInfo},
			success: function (data) {
				if(data.res == 1){
					// console.log(data.successmsg);
				}
				else{
					// alert(data.errmsg);
				}
			},
			error: function () {
				console.log('error');
			}
		});
		// 编辑节点操作
		newNodeLayer.curNode.name = nodeName;
		newNodeLayer.curNode.info = nodeInfo;
		// ztreeObj.updateNode 更新某节点数据，主要用于该节点显示属性的更新。
		ztreeObj.updateNode(newNodeLayer.curNode);
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
// 根结点信息编辑表单提交
function submitRootNode(){
	var rootName = rootNameObj.val();
	var rootInfo = rootInfoObj.val();
	// 数据校验
	if(nodeName.length === 0){
		alert('名称不允许为空！');
		return;
	}
	$.ajax({
			url: "/family/ztree",
			type: 'post',
			data: {'id': 0, 'operate':'add', 'name': rootName, 'desc': rootInfo},
			success: function (data) {
				if(data.res == 1){
					zNodes = data.successmsg[1];
					$('.add_root_person').hide();
					ztreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
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
	rootNodeLayer.fadeOut();
}

// 显示添加节点类型选择表单显示
function showSelectForm(treeNode){
	treeNode = treeNode || {};
	selectLayer.curNode = treeNode;
	selectLayer.fadeIn();
}

// 节点类型选择表单提交
function submitSelect(){
	// 获取选择的结点类型
	select = $("input[type='radio']:checked").val();
	// 调用添加节点操作
	if(select){
		addNodeType(selectLayer.curNode, select);
	}
	else{
		flag = confirm('您的节点类型选择不正确，是否重新选择？');
		if(flag){
			return;
		}
	}
	// 隐藏表单
	selectLayer.fadeOut();
}

// 隐藏结点类型选择表单
function hideSelectForm(){
	selectLayer.fadeOut();
}

var ztreeObj, zNodes=[], newNodeLayer,rootNodeLayer, selectLayer, nodeNameObj, nodeInfoObj, add_id=0;
$(function () {
	newNodeLayer = $('#new-node-layer');
	rootNodeLayer = $('#root-node-layer');
	nodeNameObj = $('#nodeName');
	rootNameObj = $('#rootName');
	nodeInfoObj = $('#nodeInfo');
	rootInfoObj = $('#rootInfo');
	selectLayer = $('#select-layer');
	$('.add_root_person').click(function () {
		rootNodeLayer.fadeIn();
	})
})
