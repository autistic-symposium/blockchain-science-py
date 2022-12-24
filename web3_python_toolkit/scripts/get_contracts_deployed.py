#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: steinkirch

import os
import ethereumetl
import pandas as pd
from utils.os import load_config, create_dir, run_exec
from utils.plots import plot_bar, open_csv, save_csv



def get_data_for_contracts_by_block() -> dict:
    """Prepare a dict of data to extract contracts by block."""
    
    data = {}
    create_dir('data')
    env_keys = ['PROVIDER_URL', 
                'TX_FILE', 
                'START_BLOCK',
                'OUTPUT_FILE']
    env_vars = load_config(env_keys) 

    data['provider_uri'] = env_vars['PROVIDER_URL']
    data['tx_file'] = env_vars['TX_FILE']
    data['start_block'] = env_vars['START_BLOCK']
    data['output_file'] = env_vars['OUTPUT_FILE']

    # adding this manually
    data['last_block_2015'] = 778482
    data['last_block_2016'] = 2912406
    data['last_block_2017'] = 4832685
    data['last_block_2018'] = 6988614
    data['last_block_2019'] = 9193265
    data['last_block_2020'] = 11565018
    data['last_block_2021'] = 13916165
    data['last_block_2022'] = 15978869 
    data['buffer_for_chunk_size'] = 10000

    return data


def export_blocks_and_transactions(end_block, data) -> dict:
    """Run ethereumetl export_blocks_and_transactions."""

    run_exec(['ethereumetl', 'export_blocks_and_transactions', \
                  f'--start-block {data["start_block"]}', \
                  f'--end-block {end_block}', \
                  f'--provider-uri {data["provider_uri"]}', \
                  f'--transactions-output {data["tx_file"]}'])

    txs = open_csv(data['tx_file'])
    contracts = txs[txs['to_address'].isnull()]
    os.remove(data['tx_file'])
    return contracts + txs['from_address'].unique().tolist()


def get_contracts_by_block(data, year) -> dict:
    """Extract unique contracts by block for a given year."""

    contracts = []
    last_block_year = data[f'last_block_{year}']
    start_block = int(data['start_block'])
    end_block = start_block + 9999

    while (end_block <= last_block_year + data['buffer_for_chunk_size']): 
        end_block_used = min(end_block, last_block_year)
        contracts.append(export_blocks_and_transactions(end_block_used, data))
        start_block += data['buffer_for_chunk_size']
        end_block += data['buffer_for_chunk_size']

    return contracts


def get_unique_contracts(contracts, year) -> None:
    """Extract and save a list of unique contracts."""

    unique_contract = [*set(contracts)]
    print(f"✅ Unique contract for {year})): {str(len(unique_contract))}")
    return pd.DataFrame(unique_contract, columns=["contracts"])


if __name__ == "__main__":

    ###########
    # Set up
    ###########
    contracts_by_year = {}
    all_contracts = pd.DataFrame()
    years = list(range(2015, 2022))
    data = get_data_for_contracts_by_block()
    start_block = int(data['start_block'])

    ###########
    # Get data
    ###########
    for year in years:
        contracts = get_contracts_by_block(data, year)
        contracts_by_year[year] = len(contracts)
        all_contracts.append(get_unique_contracts(contracts, year))
        start_block += 1

    all_contracts = all_contracts['contract_deployers'].unique()
    all_contracts_df = pd.DataFrame(all_contracts, columns=['contract'])
    save_csv(all_contracts_df, data['output_file'])
                                                     
    ###########
    # Plot data
    ###########
    y_data = [y for y in contracts_by_year[year] if year == years.revers().pop()]
    plot_bar({'contract deployed': y_data}, years)


