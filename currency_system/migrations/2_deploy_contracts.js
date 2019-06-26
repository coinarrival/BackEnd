const SafeMath = artifacts.require("SafeMath");
const CoinArrivalCoin = artifacts.require("CoinArrivalCoin");

module.exports = function(deployer) {
  deployer.deploy(SafeMath);
  deployer.link(SafeMath, CoinArrivalCoin);
  deployer.deploy(CoinArrivalCoin);
};