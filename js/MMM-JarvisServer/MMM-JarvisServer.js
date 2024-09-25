Module.register("MMM-JarvisServer", {
	defaults: {
		text: "Pinging Devices...",
		pingResults: {},
		serverStatus: false
	},

	loaded: function (callback) {
		this.finishLoading();
		Log.log(this.name + ' is loaded!');
		callback();
	},
    
    start: function () {
        this.started = true;
        this.sendSocketNotification("JARVIS_READY", { message: "[JS] Jarvis Server is Ready" });
    },

	socketNotificationReceived: function(notification, payload) {
		if (notification == "PING_RESULTS") {
			this.config.pingResults = payload;
			this.updateDom();
		} else if (notification == "SERVER_STATUS") {
			this.config.serverStatus = payload.status
			this.updateDom();
		}
	},

    getStyles: function () {
        return [this.file("css/jarvisserver.css")];
    },

	getHeader: function () {
		return "J.A.R.V.I.S. Server";
	},

	getDom: function () {
		var wrapper = document.createElement("div");
		wrapper.id = "pingStatus";
	
		let results = this.config.pingResults;
		wrapper.innerHTML = ""; 
	
		let table = document.createElement("table");
	
		const createStatusRow = (device, status) => {
			let row = table.insertRow();
			row.insertCell(0).textContent = device;
	
			let statusCell = row.insertCell(1);
			let statusCircle = document.createElement("span");
			statusCircle.classList.add("statusCircle", status);
			statusCell.appendChild(statusCircle);
	
			row.insertCell(2).textContent = status === "connected" ? "Connected" : status === "online" ? "Online" : "Offline";
		};
	
		createStatusRow("Server", this.config.serverStatus ? "connected" : "offline");
	
		for (let device in results) {
			createStatusRow(device, results[device]);
		}
	
		wrapper.appendChild(table);
		return wrapper;
	}

});
