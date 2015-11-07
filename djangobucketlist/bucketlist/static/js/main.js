$(document).ready(function() {
    $('#flash-message').fadeOut(3000);
    // Submit post on submit
    $('#bucketitem-form').on('submit', function(event) {
        event.preventDefault();
        var url = $(this).attr("action");
        var data = {
            'name': $('#id_name').val()
        }
        create_post(url, data);
    });
    // AJAX for posting
    function create_post(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                the_post: $('#id_name').val()
            },
            // handle a successful response
            success: function(json) {
                $('#id_name').val('');
                $('#bucketModal').modal('hide');
                $('body').load(document.URL);
            },
        });
    };
});