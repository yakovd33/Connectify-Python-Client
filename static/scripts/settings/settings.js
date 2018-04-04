$.each($("#settings-tabs-options-list li"), function () {
    $(this).click(function () {
        $.each($("#settings-tabs-options-list li"), function () {
            $(this).removeClass("active");
        });
        $(this).addClass("active");

        $.each($(".settings-tab"), function () {
            $(this).removeClass("active");
        });
        $(".settings-tab[data-tab='" + $(this).data('tab') + "']").addClass("active");

        window.history.pushState({"html": '', "pageTitle": ''},"", '/settings/' + $(this).data('tab') + '/');
    });
});