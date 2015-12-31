var eventListeners = {
    init: function() {
        $("#flash-message").fadeOut(3000);
        // Switch to registration form
        $("#registration-link").on("click", function(e) {
            e.preventDefault();
            $(".login-form").hide();
            $(".registration-form").show();
        });
        // Switch to login form
        $("#login-link").on("click", function(e) {
            e.preventDefault();
            $(".registration-form").hide();
            $(".login-form").show();
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
    eventListeners.init();
    // $.material.init();
});