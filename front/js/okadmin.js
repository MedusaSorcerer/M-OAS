/^http(s*):\/\//.test(location.href) || alert('请先部署到 localhost 下再访问');

var objOkTab = "";
layui.use(["element", "form", "layer", "okUtils", "okTab", "okLayer", "okContextMenu", "okHoliday", "laydate", "okMock"], function () {
    var okUtils = layui.okUtils;
    var $ = layui.jquery;
    var form = layui.form;
    var laydate = layui.laydate;
    var layer = layui.layer;
    var okLayer = layui.okLayer;
    var okHoliday = layui.okHoliday;
    var okMock = layui.okMock;
    var okTab = layui.okTab({
        url: okMock.api.navs,
        openTabNum: 30,
        parseData: function (data) {
            var _data = [];
            for (var i of data.data) {
                if (i['display'] === true) {
                    if (i['children']) {
                        var __data = []
                        for (var i2 of i['children']) {
                            if (i2['display']) {
                                __data.push(i2)
                            }
                        }
                        i['children'] = __data
                    }
                    _data.push(i)
                }
            }
            return _data
        }
    });
    var config = okUtils.local("okConfig") || okConfig || {};
    objOkTab = okTab;
    okLoading && okLoading.close();
    /**关闭加载动画*/

    $(".layui-layout-admin").removeClass("orange_theme blue_theme");
    $(".layui-layout-admin").addClass(config.theme);

    if (config.menuArrow) { //tab箭头样式
        $("#navBar").addClass(config.menuArrow);
    }

    /**
     * 左侧导航渲染完成之后的操作
     */
    okTab.render(function () {
        /**tab栏的鼠标右键事件**/
        $("body .ok-tab").okContextMenu({
            width: 'auto',
            itemHeight: 30,
            menu: [
                {
                    text: "定位所在页",
                    icon: "ok-icon ok-icon-location",
                    callback: function () {
                        okTab.positionTab();
                    }
                },
                {
                    text: "关闭当前页",
                    icon: "ok-icon ok-icon-roundclose",
                    callback: function () {
                        okTab.tabClose(1);
                    }
                },
                {
                    text: "关闭其他页",
                    icon: "ok-icon ok-icon-roundclose",
                    callback: function () {
                        okTab.tabClose(2);
                    }
                },
                {
                    text: "关闭所有页",
                    icon: "ok-icon ok-icon-roundclose",
                    callback: function () {

                        okTab.tabClose(3);
                    }
                }
            ]
        });
    });

    /**系统设置*/
    $("body").on("click", "#okSetting", function () {
        layer.open({
            type: 2,
            title: "系统设置",
            shadeClose: true,
            closeBtn: 0, //不显示关闭按钮
            skin: "slideInRight ok-setting",
            area: ['340px', '100%'],
            offset: 'r', //右边
            time: 200000, //2秒后自动关闭
            anim: -1,
            content: "./pages/system/setting.html"
        });
    });

    /**
     * 添加新窗口
     */
    $("body").on("click", "#navBar .layui-nav-item a, #userInfo a", function () {
        // 如果不存在子级
        if ($(this).siblings().length == 0) {
            okTab.tabAdd($(this));
        }
        // 关闭其他展开的二级标签
        $(this).parent("li").siblings().removeClass("layui-nav-itemed");
        if (!$(this).attr("lay-id")) {
            var topLevelEle = $(this).parents("li.layui-nav-item");
            var childs = $("#navBar > li > dl.layui-nav-child").not(topLevelEle.children("dl.layui-nav-child"));
            childs.removeAttr("style");
        }
    });

    /**
     * 左侧菜单展开动画
     */
    $("#navBar").on("click", ".layui-nav-item a", function () {
        if (!$(this).attr("lay-id")) {
            var superEle = $(this).parent();
            var ele = $(this).next('.layui-nav-child');
            var height = ele.height();
            ele.css({"display": "block"});
            // 是否是展开状态
            if (superEle.is(".layui-nav-itemed")) {
                ele.height(0);
                ele.animate({height: height + "px"}, function () {
                    ele.css({height: "auto"});
                });
            } else {
                ele.animate({height: 0}, function () {
                    ele.removeAttr("style");
                });
            }
        }
    });

    /**
     * 左边菜单显隐功能
     */
    $(".ok-menu").click(function () {
        $(".layui-layout-admin").toggleClass("ok-left-hide");
        $(this).find("i").toggleClass("ok-menu-hide");
        localStorage.setItem("isResize", false);
        setTimeout(function () {
            localStorage.setItem("isResize", true);
        }, 1200);
    });

    /**
     * 移动端的处理事件
     */
    $("body").on("click", ".layui-layout-admin .ok-left a[data-url], .ok-make", function () {
        if ($(".layui-layout-admin").hasClass("ok-left-hide")) {
            $(".layui-layout-admin").removeClass("ok-left-hide");
            $(".ok-menu").find('i').removeClass("ok-menu-hide");
        }
    });

    /**
     * tab左右移动
     */
    $("body").on("click", ".okNavMove", function () {
        var moveId = $(this).attr("data-id");
        var that = this;
        okTab.navMove(moveId, that);
    });

    /**
     * 刷新当前tab页
     */
    $("body").on("click", ".ok-refresh", function () {
        okTab.refresh(this, function (okTab) {
            //刷新之后所处理的事件
        });
    });

    /**
     * 关闭tab页
     */
    $("body").on("click", "#tabAction a", function () {
        var num = $(this).attr("data-num");
        okTab.tabClose(num);
    });

    /**
     * 键盘的事件监听
     */
    $("body").on("keydown", function (event) {
        event = event || window.event || arguments.callee.caller.arguments[0];

        // 按 Esc
        if (event && event.keyCode === 27) {
            console.log("Esc");
            $("#fullScreen").children("i").eq(0).removeClass("layui-icon-screen-restore");
        }
        // 按 F11
        if (event && event.keyCode == 122) {
            console.log("F11");
            $("#fullScreen").children("i").eq(0).addClass("layui-icon-screen-restore");
        }
    });

    /**
     * 全屏/退出全屏
     */
    $("body").on("click", "#fullScreen", function () {
        if ($(this).children("i").hasClass("layui-icon-screen-restore")) {
            screenFun(2).then(function () {
                $("#fullScreen").children("i").eq(0).removeClass("layui-icon-screen-restore");
            });
        } else {
            screenFun(1).then(function () {
                $("#fullScreen").children("i").eq(0).addClass("layui-icon-screen-restore");
            });
        }
    });

    /**
     * 全屏和退出全屏的方法
     * @param num 1代表全屏 2代表退出全屏
     * @returns {Promise}
     */
    function screenFun(num) {
        num = num || 1;
        num = num * 1;
        var docElm = document.documentElement;

        switch (num) {
            case 1:
                if (docElm.requestFullscreen) {
                    docElm.requestFullscreen();
                } else if (docElm.mozRequestFullScreen) {
                    docElm.mozRequestFullScreen();
                } else if (docElm.webkitRequestFullScreen) {
                    docElm.webkitRequestFullScreen();
                } else if (docElm.msRequestFullscreen) {
                    docElm.msRequestFullscreen();
                }
                break;
            case 2:
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.webkitCancelFullScreen) {
                    document.webkitCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                break;
        }

        return new Promise(function (res, rej) {
            res("返回值");
        });
    }

    $("#logout").click(function () {
        okLayer.confirm("确定要退出登录吗？", function () {
            okTab.removeTabStorage(function () {
                okUtils.ajax(okMock.api.logout, "get",)
                okTab.removeTabStorage();
                window.location = "menu/login.html";
            });
        });
    });

    console.log("ooo        ooooo   .oo.       .oooooo.         .o.        .oooooo..o \n" +
        "`88.       .888' .88' `8.    d8P'  `Y8b       .888.      d8P'    `Y8 \n" +
        " 888b     d'888  88.  .8'   888      888     .8\"888.     Y88bo.      \n" +
        " 8 Y88. .P  888  `88.8P     888      888    .8' `888.     `\"Y8888o.  \n" +
        " 8  `888'   888   d888[.8'  888      888   .88ooo8888.        `\"Y88b \n" +
        " 8    Y     888  88' `88.   `88b    d88'  .8'     `888.  oo     .d8P \n" +
        "o8o        o888o `bodP'`88.  `Y8bood8P'  o88o     o8888o 8\"\"88888P'  \n" +
        "                                                                                v 1.0.0 \n" +
        "\n" +
        "To the world you may be one person\n" +
        "But to one person you may be the world\n" +
        "Github: https://www.github.com/MedusaSorcerer"
    );
});
