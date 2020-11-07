layui.use(["table", "form", "okUtils", "okMock", "okLayer"], function () {
    let util = layui.util;
    let table = layui.table;
    let form = layui.form;
    let okLayer = layui.okLayer;
    let okUtils = layui.okUtils;
    let okMock = layui.okMock;
    let cols = [];
    let COLS = {};
    let toolID = '';

    okUtils.ajax(okMock.api.analyze, 'get').done(function (response) {
        if (response.status === 200) {
            var inner = '';
            for (var val of response.data) {
                inner += '<option value="' + val.id + '" class="layui-this">' + val.name + '</option>';
                COLS[val.id] = val.fields;
            }
            document.getElementById('tool').innerHTML += inner;
            form.render('select');
        }
    })

    util.event('lay-active', {
        upload: function () {
            okLayer.open("上传日志源", "upload-analyze.html", "90%", "90%", null, function () {
                window.location.reload();
            })
        },
        management: function () {
            okLayer.open("解析规则管理", "management.html", "90%", "90%", null, function () {
                window.location.reload();
            })
        }
    })

    function tool() {
        table.render({
            elem: '#tableId',
            url: okMock.api.analyze + '/' + toolID,
            limit: 20,
            page: true,
            size: "sm",
            headers: {'Authorization': okUtils.local('M&OAS-token')},
            cols: [cols],
            error: function (data) {
                console.log(data)
            },
            success: function (data) {
                console.log(data)
            },
            complete: function () {
                console.log(data)
            },
        });
    }

    form.on('select(source)', function (data) {
        toolID = data.value;
        if (toolID) {
            cols = [];
            for (var val in COLS[toolID]) {
                cols.push({
                    field: val,
                    title: COLS[toolID][val],
                    width: val === '__all__' ? 500 : 150,
                })
            }
        }
    });

    form.on("submit(search)", function () {
        if (toolID) {
            tool();
        }
        return false;
    });

    okLoading.close();
})