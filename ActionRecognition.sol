pragma solidity ^0.4.23;

/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

contract owned { //Contract used to only allow the owner to call some functions
  address public owner;

  function owned() public {
    owner = msg.sender;
  }

  modifier onlyOwner {
    require(msg.sender == owner);
    _;
  }

  function transferOwnership(address newOwner) onlyOwner public {
    owner = newOwner;
  }
}


contract ActionRecognition is owned {
  using SafeMath for uint256;

  uint256 public precision = 10 ** 10;

  int[20][] public clusters;

  string[] public activities;

  struct activityInfo{
    string word;
    string name;
  }

  activityInfo[] public wordInfo;

  event ClustersAdded(uint256 n_clusters);

  event ActivityWordAdded(uint256 n_words, string activity); 

  event ActivityAdded(string activity);



  function saveClusters(int[20] cluster1,int[20] cluster2,int[20] cluster3,int[20] cluster4,int[20] cluster5) onlyOwner public returns(bool){
    clusters.push(cluster1);
    clusters.push(cluster2);
    clusters.push(cluster3);
    clusters.push(cluster4);
    clusters.push(cluster5);
    emit ClustersAdded(5);
    return true;
  }

  function save1Word(string activity,string wordForActivity) onlyOwner public returns(bool){
    wordInfo.push(activityInfo({ word:wordForActivity, name:activity }));
    emit ActivityWordAdded(1, activity);
    return true;
  }

  function save4Words(string activity,string wordForActivity1,string wordForActivity2,string wordForActivity3,string wordForActivity4) onlyOwner public returns(bool){
    wordInfo.push(activityInfo({ word:wordForActivity1, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity2, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity3, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity4, name:activity }));
    emit ActivityWordAdded(4, activity);
    return true;
  }

  function save5Words(string activity,string wordForActivity1,string wordForActivity2,string wordForActivity3,string wordForActivity4,string wordForActivity5) onlyOwner public returns(bool){
    wordInfo.push(activityInfo({ word:wordForActivity1, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity2, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity3, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity4, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity5, name:activity }));
    emit ActivityWordAdded(5, activity);
    return true;
  } 

  function save6Words(string activity,string wordForActivity1,string wordForActivity2,string wordForActivity3,string wordForActivity4,string wordForActivity5,string wordForActivity6) onlyOwner public returns(bool){
    wordInfo.push(activityInfo({ word:wordForActivity1, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity2, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity3, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity4, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity5, name:activity }));
    wordInfo.push(activityInfo({ word:wordForActivity6, name:activity }));
    emit ActivityWordAdded(6, activity);
    return true;
  }    


  function saveActivity(string activity) onlyOwner public returns(bool){
    activities.push(activity);
    emit ActivityAdded(activity);
    return true;
  }

  function loadClusters(uint256 index) public view returns(int[20]){
    return clusters[index];
  }

  function loadWords(uint256 index) public view returns(string, string){
    return(wordInfo[index].name, wordInfo[index].word);
  }

  function totalClusters() public view returns(uint256){
    return clusters.length;
  }

  function totalWords() public view returns(uint256){
    return wordInfo.length;
  }

  function totalActivities() public view returns(uint256){
    return activities.length;
  }

}