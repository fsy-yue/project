$(function(){

	var error_password = false;
	var error_check_password = false;


	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});



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


	$('#reg_form').submit(function() {

		check_pwd();
		check_cpwd();

		if(error_password == false && error_check_password == false )
		{
			return true;
		}
		else
		{
			return false;
		}

	});

})