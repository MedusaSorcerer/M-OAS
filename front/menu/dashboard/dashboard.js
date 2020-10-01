"use strict";
layui.use(["okUtils", "okCountUp", "okMock"], function () {
    var countUp = layui.okCountUp;
    var okUtils = layui.okUtils;
    var okMock = layui.okMock;
    var $ = layui.jquery;
    okLoading.close();

    okUtils.ajax(okMock.api.dashboard).done(function (response) {
        if (response.status === 200) {
            initMediaCont(response.overview);
            initDataTrendChart(response.overview_detail);
            initUserActiveTodayChart(response.useractive);
            initUserSourceTodayChart(response.attendance);
        }
    })

    function initMediaCont(data) {
        var elem_nums = $(".media-cont .num");
        var s = 0
        elem_nums.each(function (i, j) {
            !new countUp({
                target: j,
                endVal: data[s]
            }).start();
            s++
        });
    }

    function dataTrendOption(data, color) {
        color = color || "#00c292";
        return {
            color: color, toolbox: {show: false, feature: {saveAsImage: {}}},
            grid: {left: '-1%', right: '0', bottom: '0', top: '5px', containLabel: false},
            xAxis: [{type: 'category', boundaryGap: false, splitLine: {show: false}, data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']}],
            yAxis: [{type: 'value', splitLine: {show: false}}],
            series: [{
                name: '用户', type: 'line', stack: '总量', smooth: true, symbol: "none", clickable: false, areaStyle: {},
                data: data
            }]
        }
    }

    function initDataTrendChart(data) {
        var echIncome = echarts.init($("#echIncome")[0]);
        var echGoods = echarts.init($('#echGoods')[0]);
        var echBlogs = echarts.init($("#echBlogs")[0]);
        var echUser = echarts.init($('#echUser')[0]);
        echIncome.setOption(dataTrendOption(data.process, "#00c292"));
        echGoods.setOption(dataTrendOption(data.report, "#ab8ce4"));
        echBlogs.setOption(dataTrendOption(data.repository, "#03a9f3"));
        echUser.setOption(dataTrendOption(data.user, "#fb9678"));
        okUtils.echartsResize([echIncome, echGoods, echBlogs, echUser]);
    }

    function initUserActiveTodayChart(data) {
        var userActiveTodayChart = echarts.init($("#userActiveTodayChart")[0], "themez");
        var userActiveTodayChartOption = {
            color: "#03a9f3",
            xAxis: {type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},
            yAxis: {type: 'value'},
            series: [{data: data, type: 'bar'}]
        };
        userActiveTodayChart.setOption(userActiveTodayChartOption);
        okUtils.echartsResize([userActiveTodayChart]);
    }

    function initUserSourceTodayChart(data) {
        var userSourceTodayChart = echarts.init($("#userSourceTodayChart")[0], "themez");
        var info = [];
        data.forEach(function (item) {
            info.push(item['name'])
        });
        var userSourceTodayChartOption = {
            title: {show: false, text: '用户访问来源', subtext: '', x: 'center'},
            tooltip: {trigger: 'item', formatter: "{a} <br/>{b} : {c} ({d}%)"},

            legend: {orient: 'vertical', left: 'left', data: info},
            series: [
                {
                    name: '访问来源', type: 'pie', radius: '55%', center: ['50%', '60%'],
                    data: data,
                    itemStyle: {emphasis: {shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)'}}
                }
            ]
        };
        userSourceTodayChart.setOption(userSourceTodayChartOption);
        okUtils.echartsResize([userSourceTodayChart]);
    }
});
