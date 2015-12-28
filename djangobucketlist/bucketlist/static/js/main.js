$(document).ready(function() {
    $('#flash-message').fadeOut(3000);
    // $.material.init();

    // Switch to registration form
    $('#registration-link').on('click', function (event) {
        event.preventDefault();
        $('.login-form').hide();
        $('.registration-form').show();
    });
    // Switch to login form
    $('#login-link').on('click', function (event) {
        event.preventDefault();
        $('.registration-form').hide();
        $('.login-form').show();
    });
    // Submit checkbox
    $('body').on('click', '#item-checkbox', function (event) {
        event.preventDefault();
        var url = $(this).attr('href');
        window.location.assign(url);
    });
});