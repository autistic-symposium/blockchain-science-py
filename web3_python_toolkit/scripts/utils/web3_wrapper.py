# -*- encoding: utf-8 -*-
# This class implements an (ongoing) wrapper for web3 libs.
# author: steinkirch

from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware


class Web3Wrapper():

    def __init__(self, mode, network):
        self.w3 = None
        self.pair_contract = None
        self.mode = mode
        self.network = network
        self._setup()
    
    def _setup(self) -> None:
        self._get_web3_object()
        
    def _get_web3_object(self) -> None:
        if self.mode == 'http':
            self.w3 = Web3(HTTPProvider(self.network))
    
    def get_pair_contract(self, address, abi) -> str:
        self.pair_contract = self.w3.eth.contract(address=address, abi=abi)

    def inject_middleware(self, layer=0) -> None:
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=layer)
    
    def get_reserves(self, block) -> list:
        reserve1, reserve2 = self.pair_contract.functions.getReserves().call({}, block)[:2]
        