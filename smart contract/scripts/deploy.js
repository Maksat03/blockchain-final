const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    const ChannelAccessControl = await ethers.getContractFactory("ChannelAccessControl");
    const channelAccessControl = await ChannelAccessControl.deploy();

    console.log("ChannelAccessControl deployed to:", channelAccessControl.address);
    const abi = channelAccessControl.interface.format("json");
    console.log(abi);
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });
