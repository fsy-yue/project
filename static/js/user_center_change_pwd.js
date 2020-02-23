$(function(){
    var error_old_password = false;
	var error_password = false;
	var error_check_password = false;

	$('#old_pwd').blur(function() {
		check_old_pwd();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	function check_old_pwd(){
		var len = $('#old_pwd').val().length;
		if(len<8||len>20)
		{
			$('#old_pwd').next().html('密码最少8位，最长20位')
			$('#old_pwd').next().show();
			error_old_password = true;
		}
		else
		{
			$('#old_pwd').next().hide();
			error_old_password = false;
		}
	}


	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	}


	$('#reg_form').submit(function() {
	    check_old_pwd();
		check_pwd();
		check_cpwd();

		if(error_old_password == false && error_password == false && error_check_password == false )
		{
			return true;
		}
		else
		{
			return false;
		}

	});

})