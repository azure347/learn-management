// 文件上传
$(document).ready(function () {
    $('#upload-file').on('click', function () {
        if ($('#upload_file').val() === '') {
            $('#pop-message-dialog p').text("请选择要上传的文件");
            $('#pop-message-dialog').removeClass("hide");
            return;
        }
        var form_data = new FormData();
        form_data.append('file', $('#upload_file')[0].files[0]);
        console.log(form_data);
        $.ajax({
            url: '/file/upload',
            type: 'POST',
            data: form_data,
            contentType: false, // 不设置内容类型
            processData: false, // 不处理发送的数据
            success: function (response) {
                console.log('File uploaded successfully:', response);
                if (response.code === 200) {
                    console.log('kkk', response.data['filename'])
                    $('#file_name').val(response.data['filename'])
                    var imgs = ['png', 'jpg', 'jpeg'];
                    $('.preview').empty()
                    if (imgs.includes(response.data['filename'].split('.')[1])) {
                        $('.preview').append(`<img src="http://127.0.0.1:8080/static/uploads/${response.data['filename']}" alt="Preview" width="100%" height="100%">`)
                    } else if ('pdf' === response.data['filename'].split('.')[1]) {
                        $('.preview').append(`<embed src="http://127.0.0.1:8080/static/uploads/${response.data['filename']}" width="100%" height="100%" type="application/pdf">`)
                    } else {
                        $('.preview').append(`<iframe src="http://127.0.0.1:8080/static/uploads/${response.data['filename']}" width="100%" height="100%"></iframe>`)
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log('File upload failed:', textStatus);
            }
        });
    })
});