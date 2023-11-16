// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library TgUser {
    struct Data {
        uint256 accessing_expires;

        string card;
        string cvv;
        string owner_name;
        string expires;
        string bank_transaction;
    }
}

contract ChannelAccessControl {
    address public owner;
    mapping(string => TgUser.Data) public users;
    string[] public tgIds;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function grantAccess(
        string memory tg_id,
        uint256 accessing_expires,
        string memory card,
        string memory cvv,
        string memory expires,
        string memory owner_name,
        string memory bank_transaction
    ) external onlyOwner {
        TgUser.Data storage user = users[tg_id];

        user.accessing_expires = accessing_expires;

        user.card = card;
        user.cvv = cvv;
        user.owner_name = owner_name;
        user.expires = expires;
        user.bank_transaction = bank_transaction;

        tgIds.push(tg_id);
    }

    function getUsers() external view returns (string[] memory) {
        return tgIds;
    }

    function checkAccess(string memory tg_id, uint256 current_time) external view returns (bool) {
        return current_time < users[tg_id].accessing_expires;
    }
}
