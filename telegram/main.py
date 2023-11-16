import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
from aiogram.types import Message, ContentType
from web3 import Web3

bot = Bot(token="6902520354:AAHOvRY5tTytmewWCQpcG0v3QWMSoUD77gw")
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
channel_id = "-1002113366553"

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract_abi = [{"type": "constructor", "payable": False, "inputs": []},
                {"type": "function", "name": "checkAccess", "constant": True, "stateMutability": "view",
                 "payable": False,
                 "inputs": [{"type": "string", "name": "tg_id"}, {"type": "uint256", "name": "current_time"}],
                 "outputs": [{"type": "bool"}]},
                {"type": "function", "name": "getUsers", "constant": True, "stateMutability": "view", "payable": False,
                 "inputs": [], "outputs": [{"type": "string[]"}]},
                {"type": "function", "name": "grantAccess", "constant": False, "payable": False,
                 "inputs": [{"type": "string", "name": "tg_id"}, {"type": "uint256", "name": "accessing_expires"},
                            {"type": "string", "name": "card"}, {"type": "string", "name": "cvv"},
                            {"type": "string", "name": "expires"}, {"type": "string", "name": "owner_name"},
                            {"type": "string", "name": "bank_transaction"}], "outputs": []},
                {"type": "function", "name": "owner", "constant": True, "stateMutability": "view", "payable": False,
                 "inputs": [], "outputs": [{"type": "address"}]},
                {"type": "function", "name": "tgIds", "constant": True, "stateMutability": "view", "payable": False,
                 "inputs": [{"type": "uint256"}], "outputs": [{"type": "string"}]},
                {"type": "function", "name": "users", "constant": True, "stateMutability": "view", "payable": False,
                 "inputs": [{"type": "string"}],
                 "outputs": [{"type": "uint256", "name": "accessing_expires"}, {"type": "string", "name": "card"},
                             {"type": "string", "name": "cvv"}, {"type": "string", "name": "owner_name"},
                             {"type": "string", "name": "expires"}, {"type": "string", "name": "bank_transaction"}]}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def _get_tg_users():
    return contract.functions.getUsers().call()


def _check_access(tg_id):
    access = contract.functions.checkAccess(str(tg_id), int(datetime.now().timestamp())).call()
    return access


async def check_access():
    while True:
        users = _get_tg_users()

        for user in users:
            if not _check_access(user):
                await bot.kick_chat_member(chat_id=channel_id, user_id=user)

        await asyncio.sleep(300)


@dp.message_handler(commands=['start', 'help'])
async def welcome(msg: Message):
    await msg.answer(msg.from_user.id)
    await msg.answer(_check_access(msg.from_user.id))
    await msg.answer(_get_tg_users())


@dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS)
async def on_new_chat_members(message: types.Message):
    # TODO: fix there
    print("member")
    for member in message.new_chat_members:
        if not _check_access(member.id):
            await bot.kick_chat_member(chat_id=channel_id, user_id=member.id)


async def on_startup(dp):
    asyncio.create_task(check_access())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
