setInterval(function () {
    $.ajax({
        url: '/get_user_num_copies/',
        processData: false,
        contentType: false,
        success: function (response) {
        $('#total-copies-counter').html(response);
        }
    });
}, 10000);