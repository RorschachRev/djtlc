import requests
import json
import time
#from web3.provider.rpc import HTTPProvider
from web3 import Web3, HTTPProvider
from ethjsonrpc import EthJsonRpc

ETH_MAIN=False
ROPSTEN_TEST=True

#c = EthJsonRpc('127.0.0.1', 8545)
c = EthJsonRpc('66.232.80.162', 48545)

class BC():
	"""
	Stub for blockchain state. Will include config data later.
	"""
	def __init__(self):
		if ETH_MAIN:
			#self.contract_address="0xb638530d07088A424c8A1821Ff8E3c9a57CB434e"	#ETH Main	
			#~ self.contract_address="0x8BC87Ae6F6b7946B5ab84e0AC47cb2F76EC4193F"	#ETH Main	
			self.contract_address="0x97fa8C5349c5Edf44FfE861297c602D13c662C00"
			#~ self.blockchainURL="http://66.232.80.162:48545"      #ETH
			self.blockchainURL="https://mainnet.infura.io/metamask"      #ETH
			self.w3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws")) # Websocket connection (?)
			self.network_id=1
		if ROPSTEN_TEST:
#			self.contract_address="0x89699241f04e489e5583f57f71cf2e48e9c526ca"	#Ropsten
			self.contract_address="0xFF1cef38Ce6a7DE2f8df6dfE5Ad922B81A952822"
			self.blockchainURL="https://ropsten.infura.io/metamask"      #ETH
			self.w3 = Web3(Web3.WebsocketProvider("wss://ropsten.infura.io/ws")) # Websocket connection (?)
			self.network_id=3

def main():
	resp= BC()
	w3 = resp.w3
	#w3 = Web3(HTTPProvider(resp.blockchainURL)) # infura doens't allow filters over http
	#Contract.events.<event name>.createFilter(fromBlock=block, toBlock=block, argument_filters={"arg1": "value"}, topics=[])
	#https://web3py.readthedocs.io/en/stable/contracts.html
	# Start of my code
	contract_address=Web3.toChecksumAddress(resp.contract_address)
	with open('abi.json', 'r', encoding='utf-8') as abi_file:
		contract_abi = json.loads(abi_file.read())
	my_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#	approval_filter = my_contract.events.Approval.createFilter(fromBlock=3258319, toBlock=3258320)
	approval_filter = my_contract.events.Approval.createFilter(fromBlock=0)
	print('Approval \n')	
	print(approval_filter.get_all_entries())
	print('\n')
	print('Buy\n')	
	buy_filter = my_contract.events.Buy.createFilter(fromBlock=0)
	print(buy_filter.get_all_entries())
	print('\n')
	print('Loan Payment\n')	
	loan_payment_filter = my_contract.events.LoanPayment.createFilter(fromBlock=0)
	print(loan_payment_filter.get_all_entries())
	print('\n')
	print('Ownership\n')	
	ownership_filter = my_contract.events.OwnershipTransferred.createFilter(fromBlock=0)
	print(str(dir(ownership_filter)))
	#print(ownership_filter.get_all_entries())
	print('\n')
	print('Transfer\n')	
	transfer_filter = my_contract.events.Transfer.createFilter(fromBlock=0)
	print(transfer_filter.get_all_entries())
	print('\n')
	

if __name__ == '__main__':
	main()
