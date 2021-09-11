import json
import time
from web3 import Web3

contract_address = '0xBa94dc518F64911F2352c07e1f448417426e89BE'

abi2 = json.loads(
    '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"_tokenId","type":"uint256"},{"indexed":false,"internalType":"enum Battle.MonsterLevel","name":"monster","type":"uint8"},{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"enum Battle.BattleResult","name":"result","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"BattleEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"currentReward","type":"uint256"}],"name":"ClaimEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"BATTLE_ADMIN","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_winRateMonster1","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_winRateMonster2","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_winRateMonster3","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_winRateMonster4","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_xExp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"enum Battle.MonsterLevel","name":"_monster","type":"uint8"}],"name":"battle","outputs":[{"internalType":"enum Battle.BattleResult","name":"result","type":"uint8"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"battleSessions","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"uint256","name":"times","type":"uint256"}],"name":"battleSessionsTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"battleTimes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"currentTotalReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getCurrentRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getLastTimeClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_manager","type":"address"},{"internalType":"address","name":"_monerToken","type":"address"},{"internalType":"address","name":"_monerNFT","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"manager","outputs":[{"internalType":"contract IManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"monerNFT","outputs":[{"internalType":"contract IPolkaMonsterNFT","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"monerToken","outputs":[{"internalType":"contract IMonster","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_monerERC20","type":"address"}],"name":"setERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_config","type":"address"}],"name":"setManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_monerNFT","type":"address"}],"name":"setNFT","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setWinRateMonster1","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setWinRateMonster2","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setWinRateMonster3","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setWinRateMonster4","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setXExp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')


def connectBscNetwork():
    my_provider = Web3.HTTPProvider('https://bsc-dataseed.binance.org/')
    web3 = Web3(my_provider)
    return web3


def get_abi():
    return abi2


def load_contract(w3):
    return w3.eth.contract(address=contract_address, abi=abi2)


def get_total_battle_times(monster_id, contract):
    return contract.functions.battleTimes(monster_id).call()


def get_last_battle_time(monster_id, last_fight, contract):
    return contract.functions.battleSessionsTime(monster_id, last_fight - 1).call()


def get_next_battle_time(hour):
    """ 3 hours should be config """

    return hour * 60 * 60


def get_current_time():
    return int(time.time())


def is_ready_to_battle(monster_id, contract, round_monster):
    is_ready = False

    total_battle = get_total_battle_times(monster_id, contract)

    if total_battle == 0:
        """ monster from egg """
        is_ready = True
        return is_ready

    if round_monster == 2 or round_monster == 3:
        is_ready = True
        return is_ready

    last_battle_time = get_last_battle_time(monster_id, total_battle, contract)

    if get_current_time() > last_battle_time + get_next_battle_time(3) + 30:
        is_ready = True

    return is_ready


def monster_battle(monster_id, w3, my_address, my_private_key):
    data0 = '0x88f56f0900000000000000000000000000000000000000000000000000000000000'
    data1 = format(int(monster_id), '05x')
    data2 = '0000000000000000000000000000000000000000000000000000000000000000'

    data = data0 + data1 + data2

    try:
        nonce = w3.eth.get_transaction_count(my_address, 'pending')
        transaction = w3.eth.account.signTransaction(dict(
            gas=300000,
            gasPrice=w3.eth.gasPrice,
            to=contract_address,
            nonce=nonce,
            data=data
        ), my_private_key)

        result = Web3.toHex(w3.eth.sendRawTransaction(transaction.rawTransaction))
        tx = str(result)

    except:
        tx = "Tx error"
        pass

    return tx
