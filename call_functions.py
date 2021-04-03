import os
import json
from web3 import Web3, HTTPProvider
import sys

# contract path
contract_path = './build/contracts/test.json'

try:
    f=open('./data/address.dat', 'r')
    contractAddress = Web3.toChecksumAddress(f.read())
    f.close()
    print("Contract Address:", contractAddress)
except:
    sys.exit("Error: The smart contract needs to be deployed.")

# open compiled file and get abi
truffleFile = json.load(open(contract_path))
abi = truffleFile['abi']

# setup web3 instance using testnet
f=open('./data/endpoint.dat', 'r')
testnet_endpoint = f.read()
f.close()
w3 = Web3(HTTPProvider(testnet_endpoint))
if w3.isConnected():
    print("Web3 Connected")
else:
    sys.exit("Error: Couldn't connect to the blockchain via web3")

# contract interface
contract = w3.eth.contract(address=contractAddress, abi=abi)

# get private key
f=open('./data/key.dat', 'r')
key = f.read()
f.close()
# get address
addr = w3.eth.account.privateKeyToAccount(key).address

# get the current value of the number
num = contract.functions.num().call()

print("The number is:", num)

# save block number of the block we want to start listening for events from
start = w3.eth.blockNumber-100

# get published changes
changes = contract.events.change.getLogs(fromBlock=start)
for change in changes:
    num = change['args']['number']
    print("Number was changed to:", num)

num = int(sys.argv[1])
# build transaction
build_tx = contract.functions.set(num).buildTransaction({
    'from': addr,
    'nonce': w3.eth.getTransactionCount(addr),
    'gas': 6721975, # from truffle docs
    'gasPrice': 100000000000 # from truffle docs
})
# sign transaction
sign_tx = w3.eth.account.signTransaction(build_tx, key)
# send the transaction
tx_hash = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
# wait for transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=300)

print("I changed the number to:", num)
