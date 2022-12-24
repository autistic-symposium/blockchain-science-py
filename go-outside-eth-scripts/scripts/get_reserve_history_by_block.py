#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: steinkirch

from utils.os import load_config, open_json, log_info
from utils.web3_wrapper import Web3_Wrapper


def get_data_for_connection() -> dict:
    """Prepare a dict of data for connection."""

    data = {}
    env_keys = ['PAIR_ADDRESSES', 
                'NETWORK_RPC_ENDPOINT',
                'BLOCK_NUMBER',
                'ABI_JSON_PATH']
    env_vars = load_config(env_keys) 

    data['addresses'] = env_vars['PAIR_ADDRESSES']
    data['network'] = env_vars['NETWORK_RPC_ENDPOINT']
    data['block'] = env_vars['BLOCK_NUMBER']
    data['abi'] = env_vars['ABI_JSON_PATH']
    return data


def get_reserve_by_block(data) -> None:
    """Establish connection to retrieve reserve history."""

    w3 = Web3_Wrapper(mode='http', network=data['network'])
    w3.inject_middleware()    
    w3.get_pair_contract(data['addresses'], open_json(data['abi']))
    reserve1, reserve2 = w3.get_reserves(data['block'])
    log_info(f'reserves: {reserve1}, {reserve2}')


if __name__ == "__main__":
    
    ###########
    # Set up
    ###########
    data = get_data_for_connection()

    ###########
    # Get data
    ###########
    get_reserve_by_block(data)

    