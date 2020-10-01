layui.use(["element", "jquery", "table", "form", "okLayer", "okUtils", "okMock"], function () {
    let table = layui.table;
    let form = layui.form;
    let okLayer = layui.okLayer;
    let okUtils = layui.okUtils;
    let okMock = layui.okMock;
    let $ = layui.jquery;

    okLoading.close($);
    let userTable = table.render({
        elem: '#tableId',
        url: okMock.api.listUser,
        limit: 20,
        page: true,
        toolbar: true,
        toolbar: "#toolbarTpl",
        size: "sm",
        headers: {'Authorization': okUtils.local('M&OAS-token')},
        cols: [[
            {type: "checkbox", fixed: "left"},
            {field: "id", title: "ID", width: 60,},
            {field: "get_full_name", title: "用户名", width: 150},
            {field: "username", title: "账户", width: 150},
            {field: "email", title: "邮箱", width: 200},
            {field: "is_active", title: "状态", width: 80, templet: "#statusTpl"},
            {field: "department", title: "部门", width: 150},
            {field: "date_joined", title: "加入时间", width: 145, templet: "<div>{{ layui.util.toDateString(d.date_joined, \"yyyy-MM-dd HH:mm:ss\") }}</div>"},
            {title: "操作", width: 132, align: "center", fixed: "right", templet: "#operationTpl"}
        ]],
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

    form.on("submit(search)", function (data) {
        userTable.reload({
            where: data.field,
            page: {curr: 1}
        });
        return false;
    });

    table.on("toolbar(tableFilter)", function (obj) {
        switch (obj.event) {
            case "batchEnabled":
                batchEnabled();
                break;
            case "batchDisabled":
                batchDisabled();
                break;
            case "batchDel":
                batchDel();
                break;
            case "add":
                add();
                break;
        }
    });

    table.on("tool(tableFilter)", function (obj) {
        let data = obj.data;
        switch (obj.event) {
            case "edit":
                edit(data);
                break;
            case "del":
                del(data.id);
                break;
        }
    });

    function batchEnabled() {
        okLayer.confirm("确定要批量启用吗？", function (index) {
            layer.close(index);
            let idsStr = okUtils.tableBatchCheck(table);
            okUtils.ajax(okMock.api.batch + '/' + idsStr, "put", {'is_active': true}).done(function () {
                okUtils.tableSuccessMsg('批量启用成功');
            }).fail(function (error) {
                console.log(error)
            });

        });
    }

    function batchDisabled() {
        okLayer.confirm("确定要批量禁用吗？", function (index) {
            layer.close(index);
            let idsStr = okUtils.tableBatchCheck(table);
            okUtils.ajax(okMock.api.batch + '/' + idsStr, "put", {'is_active': false}).done(function () {
                okUtils.tableSuccessMsg('批量禁用成功');
            }).fail(function (error) {
                console.log(error)
            });

        });
    }

    function batchDel() {
        okLayer.confirm("确定要批量删除吗？", function (index) {
            layer.close(index);
            let idsStr = okUtils.tableBatchCheck(table);
            okUtils.ajax(okMock.api.batch + '/' + idsStr, "delete").done(function (response) {
                okUtils.tableSuccessMsg('批量删除成功');
            }).fail(function (error) {
                console.log(error)
            });
        });
    }

    function add() {
        okLayer.open("添加用户", "user-add.html", "90%", "90%", null, function () {
            userTable.reload();
        })
    }

    function edit(data) {
        okLayer.open("更新用户", "user-edit.html", "90%", "90%", function (layero) {
            let iframeWin = window[layero.find("iframe")[0]["name"]];
            iframeWin.initData(data);
        }, function () {
            userTable.reload();
        })
    }

    function del(id) {
        okLayer.confirm("确定要删除吗？", function () {
            okUtils.ajax(okMock.api.listUser + '/' + id, 'delete').done(function () {
                okUtils.tableSuccessMsg('删除成功');
            }).fail(function (error) {
                console.log(error)
            });
        })
    }
})