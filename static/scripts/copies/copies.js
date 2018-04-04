function delete_copy (id) {
    $.ajax({
        url: '/copy/' + id + '/delete',
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response);
        }
    });
}