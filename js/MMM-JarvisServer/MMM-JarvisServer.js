Module.register("MMM-JarvisServer", {
	defaults: {
		text: "Jarvis Server",
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

    getStyles: function () {
        return ["css/jarvisserver.css"];
    },

	getHeader: function () {
		return "Jarvis Server";
	},

	getDom: function () {
		var wrapper = document.createElement("div");
		wrapper.innerHTML = this.config.text;
		return wrapper;
	},
});
