const express = require('express');
const https = require('https');
const fs = require('fs');

const PORT = 8082;
const IP = '192.168.1.88';

const app = express();

const sslOptions = {
    key: fs.readFileSync(process.cwd() + '/modules/MMM-JarvisServer/server.key'),
    cert: fs.readFileSync(process.cwd() + '/modules/MMM-JarvisServer/server.cert')
};

app.use(express.json());

app.post('/req', (req, res) => {
    console.log('Received request:', req.body);
    res.json({ message: 'Request received!', data: req.body });
});

app.get('/status', (req, res) => {
    res.json({ status: serverStatus });
});

const server = https.createServer(sslOptions, app);
server.listen(PORT, IP, () => {
    console.log(`Server running on https://${IP}:${PORT}`);
    serverStatus = true;
}).on('error', (err) => {
    console.error(err);
});

module.exports = {
    server,
    getStatus: () => serverStatus
}