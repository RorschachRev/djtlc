import requests
import decimal as D
import codecs

ETH_MAIN= False
ROPSTEN_TEST= True

func_get_loan_bal="0x9ead1b00" # web3.sha3("loanBalanceOf(address)").substring(0,8) - truncated, needed another byte
func_loan_pay_TLC="0xf3cc89a1"	#web3.sha3("loanPayTLC(address,uint256)").substring(0,8)    #actually sends loan payments
func_deed_loan="0x59a7fc3b"     #returns string in hex, convert to str, attach URL front: https://cloudflare-ipfs.com/ipfs/ + string returned from func_deed_loan
func_paid_fee="0x6fc26c6c"
func_paid_interest="0xefbe3e58"
func_paid_principal="0x5d79ba08"
func_tlc_to_usd="0x08aaf9bd"        #global conversion rate, how much is each TLC worth? 
func_get_allow_loan="0x4ebc792f"    #returns bool, if allowed to make loan payments from wallet selected
func_bal_of="0x70a08231"    #returns TLC Tokens


all_func='''
59a7fc3b: getDeedForLoan(address)	done
6fc26c6c: getLoanPaidFees(address)		done
efbe3e58: getLoanPaidInterestl(address)	done
5d79ba08: getLoanPaidPrincipal(address)	done
9ead1b00: loanBalanceOf(address)		done
08aaf9bd: TLCtoUSDc()				done
4ebc792f: getAllowLoan(address)
70a08231: balanceOf(address)'''

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
			self.contract_address="0xc4aD60059A548b460920ee3ce5534794f44a8729"	#Ropsten
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
		return false '''
	
	#Begin Gio's Function
	def get_deed_loan(self, addr):
		func_data="0x59a7fc3b"
		params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		r=self.rpc_eth_read(self.blockchainURL, params)
		if (r.__contains__("result")):
			bal=r['result']
			return (bal[130:222])
		else:
			return (False)

	def get_paid_fee(self, addr):
		func_data="0x6fc26c6c"
		params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		r=self.rpc_eth_read(self.blockchainURL, params)
		if (r.__contains__("result")):
			bal=r['result']
			return (bal[130:222])
		else:
			return (False)
	
	#def get_paid_fee(self, addr):
		#func_data="0x6fc26c6c"
		#params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		#r=self.rpc_eth_read(self.blockchainURL, params)
		#if (r.__contains__("result")):
			#bal=int(r['result'], 0)
			#return (bal)
		#else:
			#return (False)
	
	def get_paid_interest(self, addr):
		func_data="0xefbe3e58"
		params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		r=self.rpc_eth_read(self.blockchainURL, params)
		if (r.__contains__("result")):
			bal=r['result']
			return (bal[130:222])
		else:
			return (False)

	#def get_paid_interest(self, addr):
		#func_data="0xefbe3e58"
		#params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		#r=self.rpc_eth_read(self.blockchainURL, params)
		#if (r.__contains__("result")):
			#bal=int(r['result'], 0)
			#return (bal)
		#else:
			#return (False)
	
	def get_paid_principal(self, addr):
		func_data="0x5d79ba08"
		params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		r=self.rpc_eth_read(self.blockchainURL, params)
		if (r.__contains__("result")):
			bal=r['result']
			return (bal[130:222])
		else:
			return (False)

	#def get_paid_principal(self, addr):
		#func_data="0x5d79ba08"
		#params= {"to": self.contract_address, "data": func_data+'0'*24+addr }
		#r=self.rpc_eth_read(self.blockchainURL, params)
		#if (r.__contains__("result")):
			#bal=int(r['result'], 0)
			#return (bal)
		#else:
			#return (False)

	#End Gio's Function
		

if __name__ == '__main__':
	resp= BC()
	addresses=[
	"D45617882dec19F713832DA44B0BdFD6d320d103",
	#"303f9e7D8588EC4B1464252902d9e2a96575168A",
	#"aB8dB075fbf9adcE5D906b1c1680fDE70fc347Ff", 
	#"d520f58d25f7259c9a03e4d861a593d7cdfe92df"
	]
	for addr in addresses:
		answer = D.Decimal(resp.get_loan_bal(addr)/100)
		print(("Loan balance of %s is: $%s") % (addr, answer ) )
		answer =  D.Decimal(resp.get_TLC_USDc())/100000000 
		print("Current TLC to USDc is: ${:0.2f} per TLC".format(answer) ) 
		
		answer = resp.get_deed_loan(addr)	# https://stackoverflow.com/questions/9641440/convert-from-ascii-string-encoded-in-hex-to-plain-ascii
		strurl=answer
		print(("Deed loans of %s is: %s") % (addr, strurl) )
		
		answer = resp.get_paid_fee(addr)
		print(("Paid loan fees of %s is: %s") % (addr, strurl) )
		#answer =  D.Decimal(resp.get_paid_fee(addr))/100000000 
		#print("Paid loan fees of %s is: ${:0.2f} ".format(answer) % (addr) )
		
		answer = resp.get_paid_interest(addr)
		print(("Paid loan interest of %s is: %s") % (addr, strurl) )		
		#answer =  D.Decimal(resp.get_paid_interest(addr))/100000000 
		#print("Paid loan interest of %s is: ${:0.2f} ".format(answer) % (addr) )

		answer = resp.get_paid_principal(addr)
		print(("Paid loan principal of %s is: %s") % (addr, strurl) )		
		#answer =  D.Decimal(resp.get_paid_principal(addr))/100000000 
		#print("Paid loan principal of %s is: ${:0.2f} ".format(answer) % (addr) )
		
		
		
