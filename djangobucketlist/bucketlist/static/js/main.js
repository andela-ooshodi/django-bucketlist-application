$(document).ready(function() {
    $('#flash-message').fadeOut(3000);
    // Submit new bucketitem on submit
    $('#bucketitem-form').on('submit', function(event) {
        event.preventDefault();
        var url = $(this).attr("action");
        // doesn't allow for posting empty bucketitem
        var name = $('#id_name').val() ? $('#id_name').val() : undefined;
        create_post(url, name);
    });
    // AJAX for creating bucketitems
    function create_post(url, name) {
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                name: name
            },
            // handle a successful response
            success: function(json) {
                $('#id_name').val('');
                $('#bucketModal').modal('hide');
                $('#item-body').load(document.URL + " #item-body");
            },
        });
    };
    // edit bucketitem
    $('body').on('click','.item-checkbox', function(event) {
        var id_attr = $(this).attr('id').split('-');
        var item_pk = id_attr[1];
        var item_bucket = id_attr[2];
        edit_bucketitem(item_pk, item_bucket);
    });
    // AJAX for editing bucketitem
    function edit_bucketitem(item_pk, item_bucket) {
        $.ajax({
            url: '/bucketlist/' + item_bucket + '/bucketitem',
            type: 'PUT',
            data: {
                itempk: item_pk
            },
            success: function(json) {
                $('#item-body').load(document.URL + " #item-body");
            },
        });
    };
    // delete bucketitem
    $('body').on('click','.delete-item', function() {
        var id_attr = $(this).attr('id').split('-');
        var item_pk = id_attr[1];
        var item_bucket = id_attr[2];
        delete_bucketitem(item_pk, item_bucket);
    });
    // AJAX for deleting bucketitem
    function delete_bucketitem(item_pk, item_bucket) {
        $.ajax({
            url: '/bucketlist/' + item_bucket + '/bucketitem',
            type: 'DELETE',
            data: {
                itempk: item_pk
            },
            success: function(json) {
                $('#item-body').load(document.URL + " #item-body");
            },
        });
    };
    // delete bucketlist
    $('body').on('click', '.delete-list', function() {
        var list_pk = $(this).attr('id').split('-')[1];
        var user = $('#name').text().split(' ')[1];
        delete_bucketlist(list_pk, user);
    });
    // AJAX for deleting bucketlist
    function delete_bucketlist(list_pk, user) {
        $.ajax({
            url: '/bucketlist/' + user,
            type: 'DELETE',
            data: {
                listpk: list_pk
            },
            success: function(json) {
                $('#bucket-body').load(document.URL + " #bucket-body");
            },
        });
    };
});