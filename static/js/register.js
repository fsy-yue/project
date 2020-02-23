$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;


	$('#username').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});


	function check_user_name(){
		var len = $('#username').val().length;
		if(len<5||len>20)
		{
			$('#username').parent().next().html('请输入5-20个字符的用户名')
			$('#username').parent().next().show();
			error_name = true;
		}
		else
		{
			$('#username').parent().next().hide();
			error_name = false;
		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').parent().next().html('密码最少8位，最长20位')
			$('#pwd').parent().next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').parent().next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').parent().next().html('两次输入的密码不一致')
			$('#cpwd').parent().next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').parent().next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').parent().next().hide();
			error_email = false;
		}
		else
		{
			$('#email').parent().next().html('你输入的邮箱格式不正确')
			$('#email').parent().next().show();
			error_check_password = true;
		}

	}

	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});

})