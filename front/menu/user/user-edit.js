let ID;

function initData(data) {
    let jsonString = JSON.stringify(data);
    ID = JSON.parse(jsonString).id;
}

layui.use(["element", "form", "laydate", "okUtils", "okMock", "util", 'okLayer'], function () {
    let form = layui.form;
    let okUtils = layui.okUtils;
    let okMock = layui.okMock;
    let util = layui.util;
    let okLayer = layui.okLayer;

    function ajax() {
        okUtils.ajax(okMock.api.listUser + '/' + ID, "get").done(function (response) {
            var data = response.data;
            data.date_joined = util.toDateString(data.date_joined, "yyyy-MM-dd HH:mm:ss");
            data['is_admin'] = data['is_admin'] === true ? '1' : '0';
            for (var val of response.department) {
                if (val.value !== data.department) {
                    document.getElementById('department').append(new Option(val.name, val.value));
                } else {
                    document.getElementById('department').append(new Option(val.name, val.value, true));
                }
            }
            for (var swc of ['is_active', 'head_of_department', 'work_management']) {
                if (data[swc] === true) {
                    document.getElementById(swc).setAttribute('checked', '');
                }
            }
            form.val("filter", data);
            form.render('select');
        }).fail(function (error) {
            console.log(error);
        });
    }

    form.on("submit(commit)", function (data) {
        var params = data.field;
        params['is_active'] = params['is_active'] === 'yes';
        params['head_of_department'] = params['head_of_department'] === 'yes';
        params['work_management'] = params['work_management'] === 'yes';
        params['is_admin'] = params['is_admin'] === '1';
        okUtils.ajax(okMock.api.listUser + '/' + ID, "put", params).done(function () {
            okLayer.greenTickMsg("修改成功", function () {
                parent.layer.close(parent.layer.getFrameIndex(window.name));
            });
        }).fail(function (error) {
            console.log(error);
        });
        return false;
    });

    form.on("submit(cancel)", function () {
        ajax();
        for (var val1 of ['get_full_name', 'phone', 'email', 'department', 'title', 'is_admin', 'is_active', 'head_of_department', 'work_management']) {
            document.getElementById(val1).setAttribute('disabled', '');
        }
        for (var val2 of ['cancel', 'commit']) {
            document.getElementById(val2).setAttribute('style', 'display: none');
        }
        document.getElementById('edit').removeAttribute('style');
        form.render('select')
        return false;
    });

    form.on("submit(edit)", function () {
        for (var val1 of ['get_full_name', 'phone', 'email', 'department', 'title', 'is_admin', 'is_active', 'head_of_department', 'work_management']) {
            document.getElementById(val1).removeAttribute('disabled');
            if (['is_active', 'head_of_department', 'work_management'].includes(val1)) {
                document.getElementById(val1).nextElementSibling.classList.remove('layui-disabled');
            }
        }
        for (var val2 of ['cancel', 'commit']) {
            document.getElementById(val2).removeAttribute('style');
        }
        document.getElementById('edit').setAttribute('style', 'display: none');
        form.render()
        return false;
    });

    setTimeout(function () {
        ajax()
    }, 500);
    okLoading.close();
})