'use strict';

var ws = new WebSocket('wss://' + location.hostname + '/chat');

$(function () {
    $('form').submit(function () {
        if (ws.readyState == 1) {
            var $m = $('#m');
            ws.send($m.val());
            $m.val('');
        } else {
            appendMessage('>>> disconnected from server');
        }

        return false;
    });
    ws.onmessage = function (msg) {
        var returnObject = JSON.parse(msg.data);
        appendMessage(returnObject.data)
    };
    ws.onerror = function (err) {
        appendMessage('>>> error: ' + err);
    };
    ws.onclose = function close() {
        appendMessage('>>> disconnected from server');
    };

    function appendMessage(msg) {
        $('#messages').append($('<li>')).append($('<pre id="clientMessage">').text(msg));
    }
});
