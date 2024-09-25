const server = require('./server');

const NodeHelper = require("node_helper");
const Log = require("logger");
const ping = require("ping");
const devices = {
    "Desktop": "192.168.1.74",
    "Laptop": "192.168.1.69",
    "Phone": "192.168.1.80"
}

module.exports = NodeHelper.create({

    socketNotificationReceived: function(notification, payload) {
        if (notification === "JARVIS_READY") {
            Log.log(payload.message);
            this.checkServerStatus();
            server.startServer();
            this.pingDevices();
        } else if (notification === "PRINT_MESSAGE") {
            Log.log("[JS] " + payload.message);
        }
    },

    checkServerStatus: function() {
        const status = server.getStatus();
        Log.log(`[JS] Server Status: ${status}`);
        this.sendSocketNotification("SERVER_STATUS", { status: status });
    },

    pingDevices: function() {
        Log.log("[JS] Starting to ping devices...");
    
        let deviceAmount = Object.keys(devices).length;
        
        const pingAllDevices = () => {
            let pingCount = 0;
            let results = {
                "Desktop": false,
                "Laptop": false,
                "Phone": false
            };
    
            for (let device in devices) {
                let ip = devices[device];
                ping.sys.probe(ip, (isAlive) => {
                    results[device] = server.clients[device].connected ? "connected" : isAlive ? "online" : "offline";
                    pingCount++;
                    
                    if (pingCount === deviceAmount) {
                        this.sendSocketNotification("PING_RESULTS", results);
                    }
                });
            }
            Log.log("[JS] Pinging complete. Sending results.");
        };
    
        pingAllDevices();
    
        setInterval(pingAllDevices, 60000 * 30); // Ping every 30 minutes
    }

});
