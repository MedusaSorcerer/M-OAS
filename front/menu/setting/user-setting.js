layui.use(['form', 'layer', 'okMock', 'okAddlink', 'okUtils', 'okLayer'], function () {
    var form = layui.form;
    var okMock = layui.okMock;
    var okUtils = layui.okUtils;
    var okLayer = layui.okLayer;

    okUtils.ajax(okMock.api.personalSetting, "get").done(function (response) {
        form.val("filter", response.data);
        var okAddlink = layui.okAddlink.init(
            {
                workplace: 'select[name=workplace]',
                jobnumber: 'select[name=jobnumber]',

            },
            response.workplace,
            [response.data['workplace_a'], response.data['workplace_b']],
        );
        okAddlink.render();
        okLoading.close();
    });

    form.on("submit(changeUser)", function (data) {
        okUtils.ajax(okMock.api.personalSetting, "put", data.field).done(function () {
            okLayer.greenTickMsg("更新成功", function () {
                setTimeout(function () {
                    window.location.reload()
                }, 500);
            });
        }).fail(function (error) {
            console.log(error)
        });
        return false;
    });
});























