$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    // 加载右侧区域的内容
    function load_content_page(url) {
        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
            }
        });
    }

    // Bind a callback that executes when document.location.hash changes.
    $(window).bind('hashchange', function () {
        // Some browers return the hash symbol, and some don't.
        var hash = window.location.hash.replace('#', '');
        var url = null;
        if (hash === 'group') {
            url = group_page_url;
        } else {
            url = home_page_url;
        }

        load_content_page(url);
    });

    if (window.location.hash === '') {
        window.location.hash = '#home'; // home page, show the default view
    } else {
        $(window).trigger('hashchange'); // user refreshed the browser, fire the appropriate function
    }

    // 创建分组
    function create_group() {
        var name = $("#i_createGroupInput").val();
        $.ajax({
            type: 'POST',
            url: create_group_url,
            data: JSON.stringify({'name': name}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                alert(data["message"]);
                $(window).trigger('hashchange');
            }
        });
    }

    // 移除分组
    function remove_group() {
        var group_id = $("#i_removeGroupInfo").attr("data-group");
        $.ajax({
            type: 'DELETE',
            url: remove_group_url,
            data: JSON.stringify({'group_id': group_id}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                alert(data["message"]);
                // $(window).trigger('hashchange');
            }
        });
    }

    $(document).on('click', '#i_createGroupButton', create_group);
    $(document).on('click', '#i_removeGroupButton', remove_group);

    $(document).on('click', '.to-group-btn', function(){
        var url = $(this).attr("data-href");
        load_content_page(url);
    });

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
                load_content_page(cur_group_detail_url);
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
                load_content_page(cur_group_detail_url);
            }
        });
    }

    $(document).on('click', '#i_addGroupStockButton', add_group_stock);
    $(document).on('click', '#i_rmGroupStockButton', rm_group_stock);
});
