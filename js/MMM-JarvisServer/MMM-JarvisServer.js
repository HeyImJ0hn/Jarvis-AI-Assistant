Module.register("MMM-JarvisServer", {
	defaults: {
		text: "Pinging Devices...",
		pingResults: {}
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
		
		if (Object.keys(results).length === 0) {
			let noDataRow = table.insertRow();
			let cell = noDataRow.insertCell(0);
			cell.colSpan = 3;
			cell.textContent = this.config.text;
		} else {
			for (let device in results) {
				let row = table.insertRow();
				
				let deviceCell = row.insertCell(0);
				deviceCell.textContent = device;
	
				let statusCell = row.insertCell(1);
				let statusCircle = document.createElement("span");
				statusCircle.classList.add("statusCircle");
				statusCircle.classList.add(results[device] ? "online" : "offline");
				statusCell.appendChild(statusCircle);
	
				let statusTextCell = row.insertCell(2);
				statusTextCell.textContent = results[device] ? "Online" : "Offline";
			}
		}
	
		wrapper.appendChild(table);
		return wrapper;
	}

});
