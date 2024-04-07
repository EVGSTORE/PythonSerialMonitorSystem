// THIS SCRIPT DOES NOT NEED TO BE LINKED TO THE HTML, IT IS WRITTEN WITHIN IT. THIS IS JUST FOR VIEWING

var defaultCOMPort = 'COM4'; //SET FOR AUTO LOAD COM PORT
	
function refreshPorts() {
    const select = document.getElementById('com-ports');

    fetch('/list_ports')
        .then(response => response.json())
        .then(data => {
            select.innerHTML = '';
            data.forEach(port => {
                const option = document.createElement('option');
                option.value = port;
                option.text = port;
                select.appendChild(option);

                // Set the default selected port
                if (port === defaultCOMPort) {
                    option.selected = true;
                }
            });
        });
}
		

        function sendCommand() {
    const command = document.getElementById('command-input').value;
    fetch('/send_command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `command=${encodeURIComponent(command)}`
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
        if (data.status === 'success') {
            console.log('Command sent:', data.command);
        } else {
            console.error('Error sending command:', data.message);
        }
    })
    .catch(error => {
        console.error('Network or server error:', error);
    });
}


        function getLatestCommand() {
    fetch('/get_latest_command')
        .then(response => response.json())
        .then(data => {
            document.getElementById('latest-command').value = data.command || '';
        });
}

        setInterval(getLatestCommand, 250);
        setInterval(refreshPorts, 5000);

        // Initial load
        refreshPorts();
		
		function startMonitoring() {
    const port = document.getElementById('com-ports').value;
    document.getElementById('latest-command').textContent = ''; 
    fetch('/start_monitoring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `port=${encodeURIComponent(port)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log(data.message);
        } else {
            console.error('Error starting monitoring:', data.message);
        }
    });
}


	function updateSelectedPort() {
    fetch('/get_monitored_port')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('com-ports');
            select.value = data.port;
        });
}

// Periodically update the selected port
setInterval(updateSelectedPort, 1000);

window.addEventListener('load', function() {
    function updateOnlineStatus(event) {
        var condition = navigator.onLine ? "online" : "offline";
        if(condition === "offline"){
            document.getElementById("offlineMessage").style.display = "block";
        } else {
            document.getElementById("offlineMessage").style.display = "none";
        }
    }

    window.addEventListener('online',  updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
});
