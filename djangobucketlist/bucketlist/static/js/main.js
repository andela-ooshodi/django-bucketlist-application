function show_registration_form() {
    $(".login-form").hide();
    $(".registration-form").show();
};

function show_login_form() {
    $(".registration-form").hide();
    $(".login-form").show();
};

var eventListeners = {
    init: function() {
        $("#flash-message").fadeOut(3000);

        // Switch to registration form
        $("#registration-link").on("click", function(e) {
            e.preventDefault();
            show_registration_form();
        });
        // Switch to login form
        $("#login-link").on("click", function(e) {
            e.preventDefault();
            show_login_form();
        });
        // Submit checkbox value
        $("body").on("click", "#item-checkbox", function(e) {
            e.preventDefault();
            var url = $(this).attr("href");
            window.location.assign(url);
        });
    }
};

$(document).ready(function() {
    var url = window.location.href;
    $(function() {
        if ( url.indexOf('login') > -1) {
            show_login_form();
        }
    });

    eventListeners.init();
    // $.material.init();
});