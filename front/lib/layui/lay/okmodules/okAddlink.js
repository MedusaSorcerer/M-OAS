layui.define(['form', 'jquery'], function (exports) {
    var $ = layui.jquery;
    var form = layui.form;
    var $form = $('form');//当前表单元素

    /**
     * 传入需要联动的三个下拉选择元素（顺序：省、市、区）
     * {
        province:'select[name=province]',
        city:'select[name=city]',
        area:'select[name=area]',
     }
     */
    var config = {
        defElm: {
            province: 'select[name=province]',
            city: 'select[name=city]',
            area: 'select[name=area]',
        }
    };
    var addlink = {
        elms: '',
        init: function (elms = "", data, ab) {
            elms = elms || config.defElm;
            this.elms = elms;
            this.queryset = data;
            this.ab = ab;
            return this;
        },
        render: function () {
            this.elms = this.elms || config.defElm;
            slect_init(this.elms, this.queryset, this.ab);
        }
    };

    function slect_init(elms, data, ab) {
        var workplace = $(elms.workplace);
        var jobnumber = $(elms.jobnumber);
        loadProvince(data, ab);

        function loadProvince(areaData, ab) {
            var proHtml = '';
            for (var i = 0; i < areaData.length; i++) {
                if (ab[0] === areaData[i].code) {
                    proHtml += '<option value="' + areaData[i].code + '" selected>' + areaData[i].name + '</option>';
                    loadArea(areaData[i].children, ab[1]);
                } else {
                    proHtml += '<option value="' + areaData[i].code + '">' + areaData[i].name + '</option>';
                }
            }
            $form.find(workplace).append(proHtml);
            form.render();
            var _filter = workplace.attr("lay-filter");
            form.on('select(' + _filter + ')', function (data) {
                $form.find(jobnumber).html('<option value="">请选择工位</option>');
                var value = data.value;
                if (value === "" || value === null) {
                    $form.find(jobnumber).attr("disabled", "disabled");
                    var areaHtml = '<option value="">请选择工位</option>';
                    $form.find(jobnumber).html(areaHtml);
                    form.render();
                } else {
                    loadArea(areaData[value]['children'], ab[1]);
                }
            });
        }

        function loadArea(areas, b) {
            var areaHtml = '<option value="">请选择工位</option>';
            for (var i = 0; i < areas.length; i++) {
                if (b === areas[i].code) {
                    areaHtml += '<option value="' + areas[i].code + '" selected>' + areas[i].name + '</option>';
                } else {
                    areaHtml += '<option value="' + areas[i].code + '">' + areas[i].name + '</option>';
                }
            }
            $form.find(jobnumber).html(areaHtml).removeAttr("disabled");
            form.render();
            var _filter = jobnumber.attr("lay-filter");
            form.on('select(' + _filter + ')', function (data) {
            });
        }
    };

    exports('okAddlink', addlink);
});
