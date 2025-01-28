const socket = new WebSocket("ws://127.0.0.1:8080");
socket.onopen = function () {
  console.log("WebSocket connection established.");
};
socket.onmessage = function (event) {
  const message = JSON.parse(event.data);
  console.log("Received WebSocket message:", message);
  if (message.type === "code_sent") {
    alert(`Pairing code sent to: ${message.phone}`);
  } else if (message.type === "connection_update") {
    console.log("Connection update:", message.update);
  } else if (message.type === "new_message") {
    console.log("New message received:", message.messages);
  }
};
socket.onclose = function () {
  console.log("WebSocket connection closed.");
};
socket.onerror = function (error) {
  console.error("WebSocket error:", error);
};
