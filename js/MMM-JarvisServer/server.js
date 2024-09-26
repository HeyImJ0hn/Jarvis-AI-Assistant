const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const ping = require("ping");

const PORT = 8082;
const IP = '192.168.1.88';
let readFile = false;
const dataPath = path.resolve(__dirname, 'data/devices.json');
const clients = {};
const pingResults = {};

let updatePingResults = false;

let devices = {};
try {
    devices = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
    readFile = true;
} catch (error) {
    console.error(error);
}

if (readFile) {
    for (const device in devices) {
        clients[device] = {
            connected: false,
            ws: null
        };
    }

    for (let device in devices)
        pingResults[device] = "offline";
}

const wss = new WebSocket.Server({ port: PORT, host: IP });

wss.on('connection', async (ws, req) => {
    let ip = req.socket.remoteAddress;
    const device = Object.entries(devices).find(([device, value]) => value === ip)?.[0];
    
    ws.on('message', (message) => {
        console.log(`Received message: ${message}`);

        try {
            const data = JSON.parse(message);
            const targetDevice = data.target;
            const msgToSend = data.message;

            let targetClient = clients[targetDevice];
            if (!targetClient.connected) {
                ws.send(`Target device ${targetDevice} is not connected`);
            } else {
                console.log(`Sending message to ${targetDevice}: ${msgToSend}`);
                targetClient.ws.send(JSON.stringify({ from: device, message: msgToSend }), (error) => {
                    if (error) {
                        console.error(error);
                    } else {
                        ws.send(`Message sent to ${targetDevice}`);
                    }
                });
            }
        } catch (error) {
            console.error(error);
        }
    });

    ws.on('close', () => {
        console.log(`Client disconnected: ${device} (${ip})`);
        clients[device].connected = false;
        clients[device].ws = null;

        pingDevices();
    });

    clients[device].connected = true;
    clients[device].ws = ws;

    console.log(`Client connected: ${device} (${ip})`);
    
    await pingDevices();
});

const sendMessageToClient = (targetDevice, message) => {
    let targetClient = clients[targetDevice];
    if (!targetClient || !targetClient.connected) {
        console.error(`Cannot send message. Target device ${targetDevice} is not connected.`);
        return false;
    }

    targetClient.ws.send(JSON.stringify({ from: "Server", message: message }), (error) => {
        if (error) {
            console.error(`Error sending message to ${targetDevice}:`, error);
            return false;
        }
    });
    
    console.log(`Message sent to ${targetDevice}: ${message}`);
    return true;
};

function pingDevices() {
    console.log("[JS] Starting to ping devices...");

    let deviceAmount = Object.keys(devices).length;
    allDevicesPinged = false;
    
   return new Promise((resolve) => {
        let pingCount = 0;

        for (let device in devices) {
            let ip = devices[device];
            ping.sys.probe(ip, (isAlive) => {
                pingResults[device] = clients[device].connected ? "connected" : isAlive ? "online" : "offline";
                pingCount++;
                
                if (pingCount === deviceAmount) {
                    updatePingResults = true;
                    for (let device in devices)
                        if (clients[device].connected)
                            clients[device].ws.send(JSON.stringify({ type: "status", status: pingResults }));
                    resolve();
                }
            });
        }
    });
}

module.exports = {
    startServer: () => {
        console.log(`WebSocket server is running on ws://${IP}:${PORT}`);
    },
    getStatus: () => {
        return true;
    },
    pingDevices,
    pingResults,
    updatedPingResults: () => { 
        let temp = updatePingResults;
        updatePingResults = false;
        return temp; 
    },
    sendMessageToClient
};