$(document).ready(function () {
    // Authentication -->
    (function () {

        var authentication = {
            init: function () {
                this.handleLogin();
                this.handleSignup();
                this.handlePasswordReset();
            },
            handleLogin: function () {
                this.handleFormRequestServer($("form#authenticationForm"));
            },
            handleLogout: function(){
                // not implemented yet but the logout is working properly
                // this.handleFormRequestServer($("form#signOutForm"));
            },
            handleSignup: function () {
                this.handleFormRequestServer($("form#signupForm"));
            },
            handlePasswordReset: function () {
                this.handleFormRequestServer($("form#passwordReset"));
            },
            handleFormServerResponse: function (fm, data) {
                var { detail, user_id, url, success, redirect } = data;
                var responseDiv = fm.find(".response");
                if (!success || !user_id || !url) {
                    responseDiv.html(detail);
                }
                responseDiv.html(detail);

                if (redirect && url) {
                    setTimeout(function () {
                        window.location.href = url;
                    }, 200);
                }
            },
            handleFormRequestServer: function (fm) {
                var instance = this;
                fm.off("submit").on("submit", function (event) {
                    event.preventDefault();
                    var form = $(this);
                    var fd = new FormData(this);
                    var btn = form.find("button[type=submit]");
                    var btnText = btn.text();
                    btn.prop("disabled", true);
                    btn.text("Loading...");
                    $.ajax({
                        url: form.attr("action"),
                        type: form.attr("method"),
                        data: fd,
                        contentType: false,
                        processData: false,
                        success: function (response, textStatus, jqXHR) {
                            console.log(response);
                            instance.handleFormServerResponse(fm, response);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            var data = jqXHR.responseJSON || {
                                detail: "An Error occurred while processing your request",
                            };
                            console.error(textStatus, errorThrown);
                            instance.handleFormServerResponse(fm, data);
                        },
                        complete: function (jqXHR, textStatus) {
                            btn.text(btnText);
                            btn.prop("disabled", false);
                        },
                    });
                });
            },
        };
        authentication.init();
    })();
});
