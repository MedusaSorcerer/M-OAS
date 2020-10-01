let startData;
let startTime;

layui.use(["element", "form", "okLayer", "okUtils", "okMock", "laydate"], function () {
    var form = layui.form;
    var okLayer = layui.okLayer;
    var okUtils = layui.okUtils;
    var okMock = layui.okMock;
    let laydate = layui.laydate;

    function initSelect(elements) {
        for (var i of elements) {
            var element = document.getElementById(i);
            element.value = '';
            element.setAttribute('disabled', '');
        }
        form.render('select');
    }

    laydate.render({
        elem: "#startDate",
        type: "date",
        format: 'yyyy-MM-dd', trigger: 'click',
        done: function (value) {
            initSelect(['startTime', 'endDate', 'endTime']);
            if (value !== '') {
                document.getElementById('startTime').removeAttribute('disabled')
                document.getElementById('endTimeDiv').innerHTML = '' +
                    '<input class="layui-input" placeholder="请选择休假截止日期" autocomplete="off" id="endDate" name="endDate" required lay-verify="required" disabled>';
                laydate.render({
                    elem: "#endDate",
                    type: "date",
                    format: 'yyyy-MM-dd',
                    trigger: 'click',
                    min: value,
                    done: function (value) {
                        initSelect(['endTime']);
                        if (value !== '') {
                            if (startData === value && startTime === '2') {
                                document.getElementById('ett').setAttribute('disabled', '')
                            } else {
                                document.getElementById('ett').removeAttribute('disabled')
                            }
                            document.getElementById('endTime').removeAttribute('disabled');
                            form.render('select');
                        }
                    }
                });
                startData = value;
                form.render('select');
            }
        }
    });

    okUtils.ajax(okMock.api.holidayHandle, "get").done(function (response) {
        for (var val of response.data) {
            document.getElementById('holiday').append(new Option(val.name, val.id));
        }
        form.render('select');
    }).fail(function (error) {
        console.log(error);
    });

    form.on("submit(add)", function (data) {
        let btn = document.getElementById('layui-btn');
        btn.setAttribute('disabled', '');
        okUtils.ajax(okMock.api.holidayHandle, "post", data.field).done(function () {
            okLayer.greenTickMsg("已创建休假申请", function () {
                parent.layer.close(parent.layer.getFrameIndex(window.name));
            });
        }).fail(function (error) {
            console.log(error);
        });
        btn.removeAttribute('disabled');
        return false;
    });

    form.on('select(startTime)', function (data) {
        initSelect(['endDate', 'endTime']);
        if (data.value !== "") {
            document.getElementById('endDate').removeAttribute('disabled');
            form.render('select');
            startTime = data.value;
        }
    })
})