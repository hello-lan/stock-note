
$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    // 加载内容到右侧区域
    $(document).on('click', '.load-content-btn', function(){
        var url = $(this).attr("data-href");
        loadContent(url);
    });

    // 查询个股
    function searchStock(e) {
        var $input = $("#i_stockInput");
        var value = $input.val().trim()
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');

        var url = stock_page_url + "?code=" + value;
        loadContent(url);
    }

    $(document).on('keyup', '#i_stockInput', searchStock.bind(this));

    // 创建分组
    function create_group() {
        var group_index_url = $("#i_groupIndexPage").attr("data-href");
        var name = $("#i_createGroupInput").val();
        $.ajax({
            type: 'POST',
            url: create_group_url,
            data: JSON.stringify({'name': name}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                alert(data["message"]);
                loadContent(group_index_url);    // 重新加载该页面
            }
        });
    }

    // 移除分组
    function remove_group() {
        var group_index_url = $("#i_groupIndexPage").attr("data-href");
        var group_id = $("#i_removeGroupInfo").attr("data-group");
        $.ajax({
            type: 'DELETE',
            url: remove_group_url,
            data: JSON.stringify({'group_id': group_id}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                alert(data["message"]);
                loadContent(group_index_url);    // 重新加载该页面
            }
        });
    }

    $(document).on('click', '#i_createGroupButton', create_group);
    $(document).on('click', '#i_removeGroupButton', remove_group);

    // 往某分组里添加股票
    function add_group_stock() {
        var $input = $("#i_addGroupStockInput");
        var code = $input.val();
        var add_url = $input.attr("data-href");
        var cur_group_detail_url = $("#i_groupDetailUrl").attr("data-href");
                
        $.ajax({
            type: 'POST',
            url: add_url,
            data: JSON.stringify({'code': code}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                alert(data["message"]);
                loadContent(cur_group_detail_url);
            }
        });
    }

    // 往某分组里移除股票
    function rm_group_stock() {
        var $input = $("#i_rmGroupStockInfo")
        var code = $input.attr("data-code");
        var rm_url = $input.attr("data-href");
        var cur_group_detail_url = $("#i_groupDetailUrl").attr("data-href");
        
        $.ajax({
            type: 'DELETE',
            url: rm_url,
            data: JSON.stringify({'code': code}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                alert(data["message"]);
                loadContent(cur_group_detail_url);
            }
        });
    }

    $(document).on('click', '#i_addGroupStockButton', add_group_stock);
    $(document).on('click', '#i_rmGroupStockButton', rm_group_stock);

    // 检查校正input输入框中的数值类型
    function check_number() {
        this.value = this.value.replace(/\D/g,'');
    }

    function check_float() {
        this.value = this.value.replace(/[^\d\.\-]/g,'');
    }

    function check_float_series() {
        this.value = this.value.replace(/[^\d\.,]/g,'');
    }

    $(document).on('keyup', '.number-checker', check_number);
    $(document).on('keyup', '.float-checker', check_float);
    $(document).on('keyup', '.float-series-checker', check_float_series);

    // DCF 模型估值
    function dcf_valuate() {
        var params = Object();
        
        params["initialCashFlow"] = $("#inputInitialFreeCashFlow").val().trim();
        params["cashFlowGrowths"] = $("#inputFreeCashFlowGrowth").val().trim();
        params["discountRate"] = $("#inputDiscountRate").val();
        params["g"] = $("#inputPerpetuityValueGrowth").val();
        params["totalEquity"] = $("#inputTotalEquity").val();
        params["mos"] = $("#inputMOS").val();

        var a = validate_required(params["initialCashFlow"], "初始现金流不能为空");
        var b = validate_required(params["cashFlowGrowths"], "现金流增长率不能为空");
        if (!(a & b)) { return }

        loadContent(dcf_report_url, "J_report", params)
    }

    // DCF+PE 模型估值
    function dcf_pe_valuate() {
        var params = Object();
        params["r"] = $("#discountRateInput").val();
        params["equity"] = $("#equityInput").val();
        params["profit"] = $("#profitInput").val();
        params["dr0"] = $("#dividendRatio-0-Input").val();
        params["dr1"] = $("#dividendRatio-1-Input").val();
        params["dr2"] = $("#dividendRatio-2-Input").val();
        params["dr3"] = $("#dividendRatio-3-Input").val();
        params["g1"] = $("#growthRate-1-Input").val();
        params["g2"] = $("#growthRate-2-Input").val();
        params["g3"] = $("#growthRate-3-Input").val();
        params["pe"] = $("#PEInput").val();
        loadContent(dcf_pe_report_url, "J_report", params);
    }

    $(document).on('click', '#i_dcfReportButton', dcf_valuate);
    $(document).on('click', '#i_dcfPeValuateButton', dcf_pe_valuate);
});