function previewFile(){
	var preview = document.querySelector('.book_img img');
	var file = document.querySelector('input[type=file]').files[0];
	if (!/image\/\w+/.test(file.type)){
		alert("请确保文件为图像类型");
		return false;
	};
	var reader = new FileReader();//创建一个FileReader实例
　　 reader.readAsDataURL(file);//将文件内容进行base64编码后输出
　　	reader.onload = function(e) {
　　　　　preview.src = reader.result;
　　　　　formData.append('file',file);
　　　　　console.log(formData.getAll('file'));
　　};
}

function UserInfo(){
	var username = $("#username").val();
	var telephone = $('#telephone').val();
	var address = $('#address').val();
	var userdesc = $('#userdesc').val();
	// if(username.length<5||username.length>20){
	// 	alert("请输入5-20个字符的用户名");
	// 	return false;
	// }
	if (telephone) {
		if(!(/^1(3|4|5|7|8)\d{9}$/.test(telephone))){
			alert("手机号码有误，请重填");
			return false;sss
		}
	}
	formData.append('username', username);
	formData.append('telephone', telephone);
	formData.append('usersex', usersex);
	formData.append('address', address);
	formData.append('userdesc', userdesc);
	return true;
}

function Confirmpwd(){
	var old_pwd = $('#old_pwd').val();
	var new_pwd = $('#new_pwd').val();
	var new_cpwd = $('#new_cpwd').val();
	if (old_pwd.length<8||old_pwd.length>20) {
		alert("旧密码：密码最少8位，最长20");
		return false;
	}
	if (new_pwd.length<8||new_pwd.length>20) {
		alert("新密码：密码最少8位，最长20");
		return false;
	}
	if (new_pwd != new_cpwd) {
		alert("两次输入的密码不一致");
		return false;
	}
	var data = {}
	data.old_pwd = old_pwd;
	data.new_pwd = new_pwd;
	data['type'] = 'pwd';
	return data;
}

function Confirmemail(){
	var new_email = $('#new_email').val();
	var my_pwd = $('#my_pwd').val();

	if(!(/^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/.test(new_email)))
	{
		alert("你输入的邮箱格式不正确");
		return false;
	}
	if (my_pwd.length<8||my_pwd.length>20) {
		alert("密码最少8位，最长20");
		return false;
	}
	var data = {}
	data.new_email = new_email;
	data.my_pwd = my_pwd;
	data['type'] = 'email';
	return data;
}

var usersex = 0, formData = new FormData();
$(function(){
	usersex = parseInt($('.hidden').text());
	$('.user_body .base_info h1 span').click(function(){
		$('.info_pop_con').fadeIn();
	})
	$('.man').click(function () {
		$('.sex_char_con .woman').removeClass('user_sex').prev().addClass('user_sex');
		usersex = 0;
	});
	$('.woman').click(function () {
		$('.sex_char_con .man').removeClass('user_sex').next().addClass('user_sex');
		usersex = 1;
	});
	$('.info_pop .reset').click(function(){
		$('.info_pop_con').fadeOut();
	})
	$('.my_email span').click(function(){
		$(this).parent().next().fadeIn();
	})
	$('.info_pop .submit').click(function(){
		if(UserInfo()){
			formData.append('type','info');
			console.log(formData);
			$.ajax({
				url :"/user/info",
				type : 'post',
				dataType:"json",
				data:formData,
				cache: false,
				processData : false,// 告诉jQuery不要去处理发送的数据
				contentType : false,// 告诉jQuery不要去设置Content-Type请求头
				success : function(data, status, xhr) {
					formData = new FormData();
					$('.info_pop_con').fadeOut();
					// alert("您已保存成功，请到您的私人谱书中查看");
					if(data.res == 1){
						alert(data.successmsg);
						location.href = "/user/info";
					}else {
						alert(data.errmsg);
					}
				},
				error : function(xhr, errorType, error) {
					formData = new FormData();
					alert("数据保存失败，请重试");
				}
			})
		}
	})
	$('.change_pwd .submit').click(function(){
		data = Confirmpwd();
		if (data) {
			console.log(data);
			$.ajax({
				url :"/user/info",
				type : 'post',
				dataType:"json",
				data:data,
				success : function(data, status, xhr) {
					if(data.res == 1){
						alert('密码修改成功，请用新密码重新登录');
						location.href = "/user/login";
					}else {
						alert(data.errmsg);
					}
				},
				error : function(xhr, errorType, error) {
					alert("密码修改失败，请重试");
				}
			})
		}
	})
	$('.change_email .submit').click(function(){
		send_data = Confirmemail();
		if (send_data) {
			console.log(send_data);
			$.ajax({
				url :"/user/info",
				type : "post",
				data: send_data,
				success : function(data, status, xhr) {
					if(data.res == 1){
						alert(data.successmsg);
						$('.change_email div.form').fadeOut();
						$('.my_email').text('邮箱地址：'+send_data.new_email);
						$('.user_head .email').text(send_data.new_email);
					}else {
						alert(data.errmsg);
					}
				},
				error : function(xhr, errorType, error) {
					alert("邮箱修改失败，请重试");
				}
			})
		}
	})
	$('.reset').click(function(){
		$(this).parent().find("input").each(function(){
			$(this).val("");
		});
	})
})