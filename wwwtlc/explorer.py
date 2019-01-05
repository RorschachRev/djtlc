import requests
from hexbytes import HexBytes
import json
import time
import web3
# from web3 import Web3, HTTPProvider
from ethjsonrpc import EthJsonRpc
from wwwtlc.tx_hashes import rop_tx

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
            self.contract_address="0xb638530d07088A424c8A1821Ff8E3c9a57CB434e"	#ETH Main	
            #~ self.contract_address="0x8BC87Ae6F6b7946B5ab84e0AC47cb2F76EC4193F"	#ETH Main	
            #~ self.blockchainURL="http://66.232.80.162:48545"      #ETH
            self.blockchainURL="https://mainnet.infura.io/metamask"      #ETH
            self.w3 = web3.Web3(web3.Web3.WebsocketProvider("wss://mainnet.infura.io/_ws")) # Websocket connection (?)
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
    tx = web3.eth.Eth(w3)
    for x in rop_tx:
        receipt = tx.getTransactionReceipt(x)
        tx_data = tx.getTransaction(x)
        try:
            data = receipt.logs[0]['data']
            print('\nTransaction:     %s' % (x))
            print('From:            %s' % (receipt['from'][:22]))
            if contract_address.lower() == receipt['to']:
                print('To:              %s (Contract)' % (receipt['to'][:22]))
            else:
                print('To:              %s' % (receipt['to'][:22]))
            print('Data:            %s \
                 \n    (%s)' % (int(data[2:], 16), data))
            print('Tx Input Data: \
                 \n    (%s)' % tx_data.input)
        except:
            print('\nTransaction:     %s' % (x))
            print('From:            %s' % (receipt['from'][:22]))
            if contract_address.lower() == receipt['to']:
                print('To:              %s (Contract)' % (receipt['to'][:22]))
            else:
                print('To:              %s' % (receipt['to'][:22]))
            print('Data:            %s' % (receipt.logs))
            print('Tx Input Data: \
                 \n    (%s)' % tx_data.input)

if __name__ == '__main__':
    main()
