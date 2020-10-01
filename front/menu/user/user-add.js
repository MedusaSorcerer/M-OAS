layui.use(["element", "form", "laydate", "okUtils", "okMock", 'okLayer'], function () {
    let form = layui.form;
    let okUtils = layui.okUtils;
    let okMock = layui.okMock;
    let okLayer = layui.okLayer;
    let public_key;

    okUtils.ajax(okMock.api.public, "get", null, null, false).done(function (response) {
        if (response.status === 200) {
            public_key = response.data
        }
    })

    okUtils.ajax(okMock.api.department, "get").done(function (response) {
        for (var val of response.data) {
            document.getElementById('department').append(new Option(val.name, val.id));
        }
        form.render('select');
    }).fail(function (error) {
        console.log(error);
    });

    form.on("submit(commit)", function (data) {
        var params = data.field;
        params['is_active'] = params['is_active'] === 'yes';
        params['head_of_department'] = params['head_of_department'] === 'yes';
        params['work_management'] = params['work_management'] === 'yes';
        params['is_admin'] = params['is_admin'] === '1';

        var jsencrypt = new JSEncrypt();
        jsencrypt.setPublicKey(public_key);
        params['password'] = jsencrypt.encrypt(data.field.password);

        okUtils.ajax(okMock.api.listUser, "post", params).done(function () {
            okLayer.greenTickMsg("添加成功", function () {
                parent.layer.close(parent.layer.getFrameIndex(window.name));
            });
        }).fail(function (error) {
            console.log(error);
        });
        return false;
    });

    okLoading.close();
})