let public_key;

layui.use(['form', 'layer', 'okMock', 'okUtils'], function () {
    var form = layui.form,
        layer = layui.layer,
        $ = layui.jquery,
        okMock = layui.okMock,
        okUtils = layui.okUtils;

    okUtils.ajax(okMock.api.securitySetting, "get").done(function (response) {
        form.val("filter", response.data);
    });

    okUtils.ajax(okMock.api.public, "get", null, null, false).done(function (response) {
        if (response.status === 200) {
            public_key = response.data
        }
    })

    form.verify({
        new: [
            /^[\S]{6,16}$/,
            '密码必须6到16位，且不能出现空格'
        ],
        again: function (value) {
            if (!new RegExp($("#new").val()).test(value)) {
                return "两次输入密码不一致，请重新输入！";
            }
        },
    });

    form.on("submit(changePwd)", function (data) {
        var jsencrypt = new JSEncrypt();
        jsencrypt.setPublicKey(public_key);
        let params = {
            old: jsencrypt.encrypt(data.field.old),
            new: jsencrypt.encrypt(data.field.new),
            again: jsencrypt.encrypt(data.field.again),
        };
        okUtils.ajax(okMock.api.change, "put", params, true).done(function () {
            layer.msg("密码修改成功，即将返回登录界面。", function () {
                window.top.location.href = "../login.html";
            });
        });
        return false;
    });

    okLoading.close();
});

