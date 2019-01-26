import requests
from hexbytes import HexBytes
import json
import time
import web3
# from web3 import Web3, HTTPProvider
from ethjsonrpc import EthJsonRpc
from tx_hashes import rop_tx, main_tx

ETH_MAIN=True
ROPSTEN_TEST=False

#c = EthJsonRpc('127.0.0.1', 8545)
c = EthJsonRpc('66.232.80.162', 48545)

class BC():
	"""
	Stub for blockchain state. Will include config data later.
	"""
	def __init__(self):
		if ETH_MAIN:
			#self.contract_address="0xb638530d07088A424c8A1821Ff8E3c9a57CB434e"	#ETH		
			#~ self.contract_address="0x8BC87Ae6F6b7946B5ab84e0AC47cb2F76EC4193F"	#ETH Mai
			self.contract_address="0x97fa8C5349c5Edf44FfE861297c602D13c662C00"
			#~ self.blockchainURL="http://66.232.80.162:48545"      #E
			self.blockchainURL="https://mainnet.infura.io/metamask"      #E
			self.w3 = web3.Web3(web3.Web3.WebsocketProvider("wss://mainnet.infura.io/_ws")) # Websocket connection (
			self.network_id=1
		if ROPSTEN_TEST:
			#self.contract_address="0x89699241f04e489e5583f57f71cf2e48e9c526ca"	#Ropsten
			self.contract_address="0xFF1cef38Ce6a7DE2f8df6dfE5Ad922B81A952822"
			self.blockchainURL="https://ropsten.infura.io/metamask"      #ETH
			self.w3 = web3.Web3(web3.Web3.WebsocketProvider("wss://ropsten.infura.io/_ws")) # Websocket connection (?)
			self.network_id=3

def main():
	resp= BC()
	w3 = resp.w3
	contract_address=web3.Web3.toChecksumAddress(resp.contract_address)
	with open('abi.json', 'r', encoding='utf-8') as abi_file:
		contract_abi = json.loads(abi_file.read())
	my_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#	print(dir(my_contract))
#	print('Transfer\n')
	transfer_filter = my_contract.events.Transfer.createFilter(fromBlock=4340299, toBlock=4615429)
#	print(transfer_filter.get_all_entries())
#	print('\n')
	tx = web3.eth.Eth(w3)
	addresses = ['0x0000000000000000000000000000000000000000']
	tracked_balance = 0
	zero_bal = 0
	zero_addresses = []
#	print(dir(my_contract.functions.currentSupply().call()))
#	print('Current supply of %s is: %s\n' % (my_contract.functions.name().call(), my_contract.functions.currentSupply().call()))
#	print('Total supply of %s is: %s\n' % (my_contract.functions.name(), my_contract.functions.totalSupply()))

	for transfer in transfer_filter.get_all_entries():
		if transfer['args']['from'].lower() not in addresses:
			addresses.append(transfer['args']['from'].lower())
		if transfer['args']['to'].lower() not in addresses:
			addresses.append(transfer['args']['to'].lower())

#	print(addresses)
#	print(len(addresses))

	for x in main_tx:
		receipt = tx.getTransactionReceipt(x)
		try:
			if receipt['from'].lower() not in addresses:
				addresses.append(receipt['from'].lower())
			if receipt['to'].lower() not in addresses:
				addresses.append(receipt['to'].lower())
		except:
#			print('%s or %s Failed' % (receipt['from'], receipt['to']))
			pass
#	for addr in main_tx:
#		if addr not in addresses:
#			addresses.append(addr.lower())

#	print(addresses)
#	print(len(addresses))

	for addr in addresses:
		try:
			addr = web3.Web3.toChecksumAddress(addr)
			token_balance = my_contract.call().balanceOf(addr)
			if not token_balance == 0:
#				print('\nAddress: %s\nHas a balance of: %s\n' % (addr,token_balance))
				print('%s, %s' % (addr, token_balance))
				tracked_balance += token_balance
			else:
				zero_bal += 1
				zero_addresses.append(addr)
		except:
			print('%s address failed' % (addr))
			pass

#	print(zero_addresses)
#	print('
#	print('Addresses with zero balance: %s' % (zero_bal))
#	print('Tracked Balance: %s' % (tracked_balance))
#	print('Current supply of %s is: %s\n' % (my_contract.functions.name(), my_contract.functions.currentSupply()))
#	print('Total supply of %s is: %s\n' % (my_contract.functions.name(), my_contract.functions.totalSupply()))
#	print('Tracked Balance: %s' % (tracked_balance))

if __name__ == '__main__':
    main()
