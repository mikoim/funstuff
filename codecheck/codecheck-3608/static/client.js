'use strict';

function getServerAddress() {
    var protocol = location.protocol == 'https:' ? 'wss://' : 'ws://';
    return protocol + location.hostname + '/chat';
}

var ws = new WebSocket(getServerAddress());

document.querySelector('form').addEventListener('submit', function (evt) {
    evt.preventDefault();

    if (ws.readyState == 1) {
        var m = document.querySelector('#m');
        ws.send(JSON.stringify({text: m.value}));
        m.value = '';
    } else {
        appendMessage('info', '>>> disconnected from server');
    }
});

ws.onmessage = function (msg) {
    var returnObject = JSON.parse(msg.data);
    appendMessage(returnObject.type, returnObject.text)
};

ws.onerror = function (event) {
    appendMessage('info', '>>> error: something went wrong');
};

ws.onopen = function () {
    appendMessage('info', '>>> connected to server');
};

ws.onclose = function close() {
    appendMessage('info', '>>> disconnected from server');
};

function appendMessage(type, msg) {
    var messages = document.querySelector('#messages');

    var message = document.createElement('div');
    message.className = 'message';

    var status = document.createElement('p');
    status.className = 'status';
    status.textContent = new Date().toISOString() + ' / ' + type;
    message.appendChild(status);

    var text = document.createElement('pre');
    text.className = 'text';
    text.textContent = msg;
    message.appendChild(text);

    messages.insertBefore(message, messages.firstChild);
}
