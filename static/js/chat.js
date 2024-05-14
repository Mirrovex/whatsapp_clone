const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + id + "/"
);

socket.onopen = function(event) {
    console.log("CONNECTION ESTABILISHED");
}

socket.onclose = function(event) {
    console.log("CONNECTION LOST");
}

socket.onerror = function(event) {
    console.log(event);
}

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.username == message_username) {
        document.querySelector("#chat-body").innerHTML += `
        <tr>
            <td>
                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                    ${data.message}
                </p>
            </td>
        </tr>`
    } else {
        document.querySelector("#chat-body").innerHTML += `
        <tr>
            <td>
                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-LEFT rounded">
                    ${data.message}
                </p>
            </td>
        </tr>`
    }
}


document.querySelector("#chat-message-submit").onclick = function(event) {
    const message_input = document.querySelector("#message_input");
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message': message,
        'username': message_username
    }));
    message_input.value = '';
}