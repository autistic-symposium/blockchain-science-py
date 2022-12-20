#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import ethereumetl
from pandas import pd
from lib.os import load_config, create_dir, open_csv, save_csv, plot_bar, run_exec


def get_data_for_contracts_by_block() -> dict:
    """Prepare a dict of data to extract contracts by block."""
    
    data = {}
    create_dir('data')
    env_keys = ['YOUR_MAINNET_RPC_ENDPOINT']

    data['provider_uri'] = env_keys['PROVIDER_URI']
    data['env_vars'] = load_config(env_keys) 
    data['last_block_2015'] = 778482
    data['last_block_2016'] = 2912406
    data['last_block_2017'] = 4832685
    data['last_block_2018'] = 6988614
    data['last_block_2019'] = 9193265
    data['last_block_2020'] = 11565018
    data['last_block_2021'] = 13916165
    data['last_block_2022'] = 15978869 
    data['buffer_for_chunk_size'] = 10000
    data['tx_file'] = 'data/transactions.csv'

    return data


def ethereumtl_export_blocks_and_transactions(start_block, end_block, data) -> dict:
    """Run ethereumetl export_blocks_and_transactions."""

    run_exec(ethereumetl, \
                [ 'export_blocks_and_transactions', \
                  f'--start-block {start_block}', \
                  f'--end-block {end_block}', \
                  f'--provider-uri {data["provider_uri"]}', \
                  f'--transactions-output {data["tx_file"]}'])

    txs = open_csv(data['tx_file'])
    contracts = txs[txs['to_address'].isnull()]
    os.remove(data['tx_file'])
    return contracts + txs['from_address'].unique().tolist()


def get_contracts_by_block(data, year, start_block) -> dict:
    """ Extract unique contracts by block for a given year."""

    last_block_year = data[f'last_block_{year}']
    contracts = []

    end_block = start_block + 9999
    while (end_block <= last_block_year + data['buffer_for_chunk_size']): 
        end_block_used = min(end_block, last_block_year)
        contracts = ethereumtl_export_blocks_and_transactions(
                                start_block, end_block_used, data)

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
    start_block = 40000
    results_file = 'mainnet_deployed_contracts.csv'
    all_contracts = pd.DataFrame()
    years = list(range(2015, 2022))
    data = get_data_for_contracts_by_block()

    ###########
    # Get data
    ###########
    for year in years:
        contracts = get_contracts_by_block(data, year, start_block)
        contracts_by_year[year] = len(contracts)
        all_contracts.append(get_unique_contracts(contracts, year))
        start_block += 1

    all_contracts = all_contracts['contract_deployers'].unique()
    all_contracts_df = pd.DataFrame(all_contracts, columns=['contract'])
    save_csv(all_contracts_df, results_file)
                                                     
    ###########
    # Plot data
    ###########
    y_data = [y for y in contracts_by_year[year] if year == years.revers().pop()]
    plot_bar({'contract deployed': y_data}, x)




