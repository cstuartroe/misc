const express = require("express");
const path = require('path');
const http = require('http');
const request = require('request');

const app = express();

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'build/index.html'));
})

app.use(express.static(path.join(__dirname, 'build')));

app.use('assets', express.static(path.join(__dirname, 'public')));

const port = process.env.PORT || '3000';
app.set('port', port);

const server = http.createServer(app);

server.listen(port, () => console.log(`temp-map running on localhost:${port}`));
