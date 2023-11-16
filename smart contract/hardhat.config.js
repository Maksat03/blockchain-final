require("@nomiclabs/hardhat-waffle");

module.exports = {
  solidity: "0.8.19",
  networks: {
    dev: {
      url: "http://localhost:8545",
    },
  },
};