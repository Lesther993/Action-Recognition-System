import express = require("express");
import bodyParser = require('body-parser');
import cors = require('cors');

import {actionRecognitionRoutes} from './routes/actionRecognitionRoutes';


const app = express();

// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


app.use(cors());


let port = process.env.PORT || 4200;



app.get('/', function(req, res) {
    res.send("Welcome :)");
});

app.use('/action-recognition', actionRecognitionRoutes);


// Start up the Node server
app.listen(port, () => {
  console.log(`Node server listening on http://localhost:${port}`);
});