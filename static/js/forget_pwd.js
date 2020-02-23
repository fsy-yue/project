$(function(){

	var error_email = false;

	$('#email').blur(function() {
		check_email();
	});


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
			error_email = true;
		}

	}

	$('#reg_form').submit(function() {

		check_email();

		if(error_email == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});

})