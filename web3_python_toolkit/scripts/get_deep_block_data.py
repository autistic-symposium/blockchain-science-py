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
                'BLOCK_NUMBER']
    env_vars = load_config(env_keys) 

    data['network'] = env_vars['PROVIDER_URL']
    data['block'] = env_vars['BLOCK_NUMBER']
    data['provider_type'] = env_vars['PROVIDER_TYPE']  
    return data


def get_deep_block_data(data) -> dict:
    
    w3 = Web3Wrapper(mode=data['provider_type'],
                     network=data['network'])  
    return w3.get_block()


if __name__ == "__main__":

    data = get_data_for_connection()
    results = get_deep_block_data(data)
    pprint(results)
    
