import {environment} from '../environment/environment';
import * as web3 from 'web3';

export class actionRecognition{
private web3:web3;
	private myContractInstance:any
	constructor(){
		this.web3 = new web3();
		this.web3.setProvider(new web3.providers.HttpProvider(environment.nodeURL));

		if (this.web3.isConnected()) { 
			this.myContractInstance = this.web3.eth.contract(environment.contractABI).at(environment.contractAddress);
	        // console.log(`Server connected to ${environment.nodeURL}`);	
	        // console.log(this.web3.fromWei(this.web3.eth.getBalance("0x0Ec793B3F6ECf6FC2D371F7e2000337A1CB47dA6").toNumber(),"ether"));	
	        // console.log("gasprice",this.web3.fromWei(this.web3.eth.gasPrice.toNumber(),"ether") );	
	        // console.log("block",this.web3.eth.getBlock("latest").gasLimit);
	        // console.log("fee",this.web3.fromWei(this.web3.eth.gasPrice.toNumber(),"ether")*this.web3.eth.getBlock("latest").gasLimit);
		} else {
	        let err = new Error("A web3 valid instance must be provided");
	        err.name = "Web3InstanceError";
	        throw err;
		}		
	}	


	public loadClusters():any{
		try{
			let index = this.myContractInstance.totalClusters();
			let clusters = [];
			let data;
			for(let i=25;i<index;i++){
				data = this.myContractInstance.loadClusters(i).map((x)=>x*Math.pow(10,-10));
				console.log(data);
				clusters.push( data );
			}
			return ({ success:true, data:clusters, error:null });
		}catch(err){
			return ({ success:false, data:null, error:String(err)});
		}		 
	}

	public loadWords():Promise<any>{
			let index = this.myContractInstance.totalWords();
			console.log(index)
			return new Promise((resolve,reject)=>{
				this.forLoop([], 0, index).then((response)=>{
					resolve({ success:true, data:response, error:null });
				}).catch((err)=>{
					reject({ success:false, data:null, error:err});
				});
			});
	}	

	public forLoop(_word,_i,index){
		let i = _i;
		let word = _word;
		return new Promise((resolve,reject)=>{
			if (i<index) { 
				this.myContractInstance.loadWords(i,(error, result)=>{
					if(!error){
						console.log(result);
						let f = {
						name:result[0],
						word:result[1]
						}				
						word.push(f);
						i++;
						setTimeout(()=>{
							resolve(this.forLoop(word,i,index));
						},700);

					}else{
						reject(String(error));
					}
				});
			} else {
				resolve(word);
			}
			
		});
	}

}
