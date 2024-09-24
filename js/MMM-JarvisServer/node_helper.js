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
            this.pingDevices();
        } else if (notification === "PRINT_MESSAGE") {
            Log.log("[JS] " + payload.message);
        }
    },

    pingDevices: function() {
        Log.log("[JS] Starting to ping devices...");
        setInterval(() => {
            let results = {
                "Desktop": false,
                "Laptop": false,
                "Phone": false
            };

            for (let device in devices) {
                let ip = devices[device];
                ping.sys.probe(ip, (isAlive) => {
                    results[device] = isAlive;

                    this.sendSocketNotification("PING_RESULTS", results);
                });
            }
            Log.log("[JS] Pinging complete. Sending results.");
        }, 100000);
    },

});
