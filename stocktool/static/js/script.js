$(document).ready(function () {
    var ENTER_KEY = 13;
    var ESC_KEY = 27;

    // Bind a callback that executes when document.location.hash changes.
    $(window).bind('hashchange', function () {
        // Some browers return the hash symbol, and some don't.
        var hash = window.location.hash;
        var sel = "a[href='" + hash + "']";
        var url = $(sel).attr("data-href");

        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
            }
        });
    });

    if (window.location.hash === '') {
        window.location.hash = '#home'; // home page, show the default view
    } else {
        $(window).trigger('hashchange'); // user refreshed the browser, fire the appropriate function
    }

    function quitModal() {
        $('body').removeClass("modal-open");
        $("div.modal-backdrop").remove();

    }

    // 往某分组里添加股票
    function add_group_stock() {
        var $input = $("#i_add-group-stock-input");
        var code = $input.val();
        var url = $input.attr("data-href");
        
        quitModal();
        
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify({'code': code}),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
            }
        });
    }

    $(document).on('click', '#i_add-group-stock-btn', add_group_stock);
});