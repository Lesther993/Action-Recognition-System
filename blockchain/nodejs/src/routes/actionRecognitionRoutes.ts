import express = require("express");

import {actionRecognition} from "../services/actionRecognition";


const actionRecognitionRoutes = express.Router();
const ActionRecognition = new actionRecognition();

actionRecognitionRoutes.route('/loadClusters').post((req,res)=>{

	res.send({success:true,data:ActionRecognition.loadClusters(),error:null});

});

actionRecognitionRoutes.route('/loadWords').post((req,res)=>{

	ActionRecognition.loadWords().then((response)=>{
		res.send(response);
	}).catch((err)=>{
		res.send(err);
	})
	// res.send({success:true,data:ActionRecognition.loadWords(),error:null});
	
});


export { actionRecognitionRoutes }