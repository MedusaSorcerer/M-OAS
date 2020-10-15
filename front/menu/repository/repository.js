layui.use(["element", "table", "form", "laydate", "okLayer", "okUtils", "okMock"], function () {
    var util = layui.util;
    var form = layui.form;
    var okLayer = layui.okLayer;
    var okUtils = layui.okUtils;
    var okMock = layui.okMock;
    var converter = new showdown.Converter();
    var dataids = [];
    var ajax_sign = true;
    var page = 1;
    var request_sign = true;
    var scrollHeight_sign = 0;

    function inner(response) {
        var element = '';
        for (var val of response.data) {
            if (dataids.includes(val.id) === false) {
                dataids.push(val.id);
                if (val.content.length >= 300) {
                    element += ('' +
                        '<li>' +
                        '<h2 class="title">' + val.title + '</h2>' +
                        '<p class="update_author">' + val.author_name + ' / ' + layui.util.toDateString(val.update, "yyyy-MM-dd HH:mm:ss") + '</p>' +
                        '<input type="checkbox" id="contTab_' + val.id + '" checked="checked" class="tabbed">' +
                        '<div class="content">' + converter.makeHtml(val.content) + '</div>' +
                        '<div class="content-more"><div class="gradient"></div> <label for="contTab_' + val.id + '" class="readmore">点 击 查 阅 全 文</label></div>' +
                        '</li>');
                } else {
                    element += ('' +
                        '<li>' +
                        '<h2 class="title">' + val.title + '</h2>' +
                        '<p class="update_author">' + val.author_name + ' / ' + layui.util.toDateString(val.update, "yyyy-MM-dd HH:mm:ss") + '</p>' +
                        '<div class="content">' + converter.makeHtml(val.content) + '</div>' +
                        '</li>'
                    )
                }
            }
        }
        document.getElementById('content-ul').innerHTML += element;
        return ''
    }

    function clear() {
        document.getElementById('repository').innerHTML = '<div class="layui-none">无数据</div><ul id="content-ul"></ul>';
        dataids = [];
        page = 1;
    }

    function ajax(params) {
        okUtils.ajax(okMock.api.repository, 'get', params).done(function (response) {
            if (response.next === null || response.next === '') {
                ajax_sign = false;
            }
            if (response.data.length === 0) {
                document.getElementsByClassName('layui-none')[0].setAttribute('style', 'display: block;');
                return;
            } else {
                document.getElementsByClassName('layui-none')[0].removeAttribute('style');
            }
            inner(response);
        }).fail(function (error) {
            console.log(error);
            ajax_sign = false;
        });
    }

    ajax();

    form.on("submit(search)", function (data) {
        clear();
        ajax(data.field);
        return false;
    });

    util.event('lay-active', {
        add: function () {
            okLayer.open("发表文章", "repository-add.html", "90%", "90%", null, function () {
                window.location.reload();
            })
        },
        detail: function (data) {
            console.log(data)
        }
    });

    document.onscroll = function () {
        if (request_sign === true && ajax_sign === true) {
            request_sign = false;
            var scrollTop = document.documentElement.scrollTop || document.body.scrollTop,
                clientHeight = document.documentElement.clientHeight || document.body.clientHeight,
                scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight

            if (scrollHeight - scrollTop - clientHeight <= 500 && scrollHeight_sign !== scrollHeight) {
                page += 1;
                scrollHeight_sign = scrollHeight;
                ajax({'page': page, 'search': document.getElementById('search').value});
                setTimeout(function () {
                    request_sign = true;
                }, 2000);
            } else {
                request_sign = true;
            }
        }
    }

    okLoading.close();
})