
                $(tItem).on("submit", function (event) {
                  event.preventDefault(); // Prevent form submission
                  const phone = $("#phoneNumber").val();
                  const data = {
                    user_id: "kwasa",
                    phone: phone
                  };
                  handleConnection(data);
                });

                function handleConnection(requestData) {

                  $.ajax({
                    type: "POST",
                    url: "http://127.0.0.1:3000/api/connect",
                    contentType: "application/json",
                    data: JSON.stringify(requestData),
                    success: function (response) {
                      $(tItem).html(JSON.stringify(response));
                      console.log("Connection started successfully!", response);
                    },
                    error: function (xhr, status, error) {
                      console.error("Error:", error);
                      $(tItem).html(JSON.stringify(error));
                    },
                    complete: function () {
                      console.log("Request completed!");
                      console.log('Ajax request completed!');
                    }
                  });
                }
               