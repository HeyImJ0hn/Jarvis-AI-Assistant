const NodeHelper = require("node_helper");
const Log = require("logger");
module.exports = NodeHelper.create({

    socketNotificationReceived: function(notification, payload) {
        if (notification === "JARVIS_READY") {
            Log.log(payload.message);
        }
    }

});
