pragma solidity >=0.4.21 <0.6.0;

import "./SafeMath.sol";

/**
 * Standard ERC20 token
 */
contract StandardToken {
   
    string public name;
    string public symbol;
    uint8 public  decimals;
	uint256 public totalSupply;
   
    function transfer(address to, uint256 value) public returns (bool success);
    
    function transferFrom(address from, address to, uint256 value) public returns (bool success);
    
    function approve(address spender, uint256 value) public returns (bool success);
    
    function allowance(address _owner, address spender) public view returns (uint256 remaining);
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    event Approval(address indexed _owner, address indexed spender, uint256 value);
}

contract CoinArrivalCoin is StandardToken {
 
	mapping (address => uint256) public balanceOf;

	mapping (address => mapping (address => uint256)) internal allowed;
	
	constructor() public {
        totalSupply = 1000000000;
        name = "CoinArrivalCoin";
        symbol = "CAC";
        decimals = 0;
        balanceOf[msg.sender] = totalSupply;
    }
 
    function transfer(address to, uint256 value) public returns (bool success) {
		require(to != address(0));
		require(value <= balanceOf[msg.sender]);
 
        balanceOf[msg.sender] = SafeMath.sub(balanceOf[msg.sender], value);
        balanceOf[to] = SafeMath.add(balanceOf[to], value);
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) public returns (bool success) {
        require(spender != address(0));

        allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
 
    function transferFrom(address from, address to, uint256 value) public returns (bool success) {
		require(to != address(0));
        require(value <= balanceOf[from]);
        require(value <= allowed[from][msg.sender]);
 
        balanceOf[from] = SafeMath.sub(balanceOf[from], value);
        balanceOf[to] = SafeMath.add(balanceOf[to], value);
        allowed[from][msg.sender] = SafeMath.sub(allowed[from][msg.sender], value);

        emit Transfer(from, to, value);

        return true;
    }
 
    function allowance(address _owner, address spender) public view returns (uint256 remaining) {
      return allowed[_owner][spender];
    }
 
}