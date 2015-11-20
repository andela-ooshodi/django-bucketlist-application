$(document).ready(function() {
    $('#flash-message').fadeOut(3000);

    $('body').on('click', '#item-checkbox', function(event) {
        event.preventDefault();
        var url = $(this).attr('href');
        window.location.assign(url);
    });
});