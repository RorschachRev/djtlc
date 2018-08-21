import requests
import decimal as D

ETH_MAIN=True
ROPSTEN_TEST= False

func_get_loan_bal="0x9ead1b00" # web3.sha3("loanBalanceOf(address)").substring(0,8) - truncated, needed another byte
func_loan_pay_TLC="0xf3cc89a1"	#web3.sha3("loanPayTLC(address,uint256)").substring(0,8)


class BC():
	"""
	Stub for blockchain state. Will include config data later.
	"""
	def __init__(self):
		if ETH_MAIN:
			self.contract_address="0xb638530d07088A424c8A1821Ff8E3c9a57CB434e"	#ETH Main	
			#~ self.contract_address="0x8BC87Ae6F6b7946B5ab84e0AC47cb2F76EC4193F"	#ETH Main	
			#~ self.blockchainURL="http://66.232.80.162:48545"      #ETH
			self.blockchainURL="https://mainnet.infura.io/metamask"      #ETH
			self.network_id=1
		if ROPSTEN_TEST:
			self.contract_address="0x89699241f04e489e5583f57f71cf2e48e9c526ca"	#Ropsten
			self.blockchainURL="https://ropsten.infura.io/metamask"      #ETH
			self.network_id=3
	def get_loan_bal(self, addr):
		func_data="0x9ead1b00"
		params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		#	params= {"to": contract_address, "data": "0x9ead1b00000000000000000000000000303f9e7d8588ec4b1464252902d9e2a96575168a" }
		#	params= {"to": contract_address, "data": "0x9ead1b00000000000000000000000000303f9e7D8588EC4B1464252902d9e2a96575168A" }
		#params= {"to": contract_address, "data": "0x771282f6" }	
		r=self.rpc_eth_read(self.blockchainURL, params)
		if (r.__contains__("result")):
			bal=int(r['result'],0)
			return (bal)
		else:
			return (False)

	def get_TLC_USDc(self):
	    func_data="0x08aaf9bd"
	    params= {"to": self.contract_address, "data": func_data }
	    r=self.rpc_eth_read(self.blockchainURL, params)
	    if (r.__contains__("result")):
	            TLCtoUSDc=int(r['result'],0)
	            return(TLCtoUSDc)
	    else:
	            return (False)

	def rpc_eth_read(self, url, params={}):
		jsondata={"jsonrpc":"2.0","method":"eth_call","params":[params , "latest"],"id":self.network_id}	
		r = requests.post( url, json=jsondata )
		return r.json()
		
	# Alex
	'''def check_deed(time.sleep=30):
		return false'''

if __name__ == '__main__':
	resp= BC()
	addr="303f9e7D8588EC4B1464252902d9e2a96575168A"
	answer = D.Decimal(resp.get_loan_bal(addr)/100)
	print(("Loan balance of %s is: $%s") % ( addr, answer ) )
	answer =  D.Decimal(resp.get_TLC_USDc())/100000000 
	print("Current TLC to USDc is: ${:0.2f} per TLC".format(answer) ) 
