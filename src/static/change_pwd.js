$(document).ready(function () {
    $('#change-password').click(function () {
        $('#change-password-dialog').removeClass("hide");
    });

    $('#change-password-dialog .cancel').click(function () {
        $('#change-password-dialog').addClass("hide");
    });

    // 修改密码
    $('#pwd-submit').on('click', function () {
        var old_pwd = $('#old-password').val().trim();
        var new_pwd = $('#new-password').val().trim();
        var new_pwd_confirm = $('#confirm-password').val().trim();
        if (old_pwd === '' || new_pwd === '' || new_pwd_confirm === '') {
            $('#pop-message-dialog p').text("旧密码、新密码或确认密码不能为空");
            $('#pop-message-dialog').removeClass("hide");
            return;
        }
        if (new_pwd !== new_pwd_confirm) {
            $('#pop-message-dialog p').text("两次密码输入不一致");
            $('#pop-message-dialog').removeClass("hide");
            return;
        }
        $.ajax({
            url: '/user/change-password',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'old_password': old_pwd,
                'new_password': new_pwd,
                'confirm_password': new_pwd_confirm
            }),
            success: function (response) {
                //console.log(response)
                if (response.code === 200) {
                    $('#change-password-dialog').addClass("hide");
                } else {
                    $('#pop-message-dialog p').text(response.msg);
                    $('#pop-message-dialog').removeClass("hide");
                }
            },
            error: function (xhr, status, error) {
                console.error('请求失败: ', status, error);
            }
        });
    })
});