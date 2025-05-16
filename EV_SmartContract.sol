pragma solidity >= 0.8.11 <= 0.8.11;

contract EV_SmartContract{

struct EVdata {
        uint timestamp;
        string edata;
    }

  struct register {
        uint timestamp;
        string data;
    }


 

 EVdata[] public evdata;
register[] public rdata;


  //call this function to EV data to Blockchain
    function setEVData(string memory r) public {
       bytes memory filebytes = bytes(r);

       EVdata memory newContent = EVdata({
        edata:r,
        timestamp: block.timestamp
       });

    evdata.push(newContent);
    }
   //get request details
    function getEVData() public view returns (EVdata[] memory) {
        return evdata;
    }



  //call this function to register user request data to Blockchain
    function setUser(string memory r) public {
       bytes memory filebytes = bytes(r);

       register memory newContent = register({
        data:r,
        timestamp: block.timestamp
       });

    rdata.push(newContent);
    }
   //get request details
    function getUser() public view returns (register[] memory) {
        return rdata;
    }

}
