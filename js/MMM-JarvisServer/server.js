const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const PORT = 8082;
const IP = '192.168.1.88';
let readFile = false;
const dataPath = path.resolve(__dirname, 'data/devices.json');
const clients = {};
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
}


const wss = new WebSocket.Server({ port: PORT, host: IP });

wss.on('connection', (ws, req) => {
    ws.send('Connected to J.A.R.V.I.S. Server');

    let ip = req.socket.remoteAddress;
    const device = Object.entries(devices).find(([device, value]) => value === ip)?.[0];

    clients[device].connected = true;
    clients[device].ws = ws;

    console.log(`Client connected: ${device} (${ip})`);

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
    });
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


module.exports = {
    startServer: () => {
        console.log(`WebSocket server is running on ws://${IP}:${PORT}`);
    },
    getStatus: () => {
        return true;
    },
    devices,
    clients,
    sendMessageToClient
};