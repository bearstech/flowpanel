$(function() {

    var connection = new WebSocket('ws://' + document.location.host + '/chaussette');

    // When the connection is open, send some data to the server
    connection.onopen = function () {
        connection.send('Ping'); // Send the message 'Ping' to the server
    };

    // Log errors
    connection.onerror = function (error) {
        console.log('WebSocket Error ' + error);
    };

    // Log messages from the server
    connection.onmessage = function (e) {
        console.log('Server: ' + e.data);
        $('#events').append('<ul>' + e.data);
    };


});
