const server = require('./server');

const NodeHelper = require("node_helper");
const Log = require("logger");

module.exports = NodeHelper.create({

    socketNotificationReceived: function(notification, payload) {
        if (notification === "JARVIS_READY") {
            Log.log(payload.message);
            this.checkServerStatus();
            server.startServer();
            devices = server.devices;
            this.pingDevices();
            this.updatePingResults();
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
        const ping = async () => { 
            await server.pingDevices();
            this.sendSocketNotification("PING_RESULTS", server.pingResults);
        };

        ping();
    
        setInterval(ping, 60000 * 30); // Ping every 30 minutes
    },

    updatePingResults: function() {
        const getResults = () => {
            if (server.updatedPingResults)
                this.sendSocketNotification("PING_RESULTS", server.pingResults);
        };

        setInterval(getResults, 1000);
    }

});
