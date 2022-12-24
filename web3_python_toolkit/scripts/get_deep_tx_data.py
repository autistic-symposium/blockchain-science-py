#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: steinkirch

from utils.strings import pprint
from utils.os import load_config
from utils.web3_wrapper import Web3Wrapper


def get_data_for_connection() -> dict:
    """Prepare a dict of data for connection."""

    data = {}
    env_keys = ['PROVIDER_TYPE', 
                'PROVIDER_URL',
                'TRANSACTION']
    env_vars = load_config(env_keys) 

    data['network'] = env_vars['PROVIDER_URL']
    data['provider_type'] = env_vars['PROVIDER_TYPE'] 
    data['tx'] = env_vars['TRANSACTION']
    return data


def get_deep_tx_data(data) -> dict:
    
    w3 = Web3Wrapper(mode=data['provider_type'],
                     network=data['network'])  
    tx_data = w3.get_tx(data['tx'])
    tx_data.update(w3.get_tx_receipt(data['tx']))

    return tx_data


if __name__ == "__main__":

    data = get_data_for_connection()
    tx_data = get_deep_tx_data(data)
    pprint(tx_data)
    
