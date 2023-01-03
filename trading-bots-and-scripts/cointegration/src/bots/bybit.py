# -*- encoding: utf-8 -*-
# src/utils/bot.py
# author: steinkirch
# Deploy a trading bot.

import datetime
import websockets
from pybit import HTTP

'''
from src.markets import get_start_time
from src.utils import load_config
from src.stategies import extract_close_prices, calculate_cointegration


def get_ws_subscriptions(token1, token2) -> object:
    """Get public websocket subscriptions."""

    return [
        f"orderBookL2_25.{token1}",
        f"orderBookL2_25.{token2}"
    ]


def get_ws_connection(ws_url, token1, token2) -> object:
    """Get public websocket connections."""

    return websockets.connect(
        ws_url,
        subscriptions=get_ws_subscriptions(token1, token2) 
    )


def set_leverage(token, session) -> None:
    """Set leverage for safety, using private session."""

    try:
        session.cross_isolated_margin_switch(
            symbol=token,
            is_isolated=True,
            buy_leverage=1,
            sell_leverage=1
        )
    except Exception as e:
        print(f'Could not set leverage: {e}')


def push_order_execution(token, direction, capital, ws, env_vars) -> str:
    """Start order execution for a given token in the public ws."""

    limit_order_basis = env_vars['LIMIT_ORDER_BASIS']
    orderbook = ws.fetch(f"orderBookL2_25.{token}")
    mid_price, stop_loss, quantity = get_trade_details(orderbook, direction, capital, env_vars)
    order = place_order(token, mid_price, quantity, direction, limit_order_basis, stop_loss)

    if 'result' in order.keys():
        if 'order_id' in order['result']:
            return order['result']['order_id']


def get_trade_details(orderbook, direction, capital, env_vars) -> tuple:
    """Get trade details and latest price."""

    rouding_token1 = env_vars['ROUDING_TOKEN1']
    rouding_token2 = env_vars['ROUNDING_TOKEN2']
    qty_token1 = env_vars['QTY_TOKEN1']
    qty_token2 = env_vars['QTY_TOKEN2']
    stop_loss_fail_safe = env_vars['STOP_LOSS_FAIL_SAFE']
    price_rounding = 20
    quantity_rounding = 20
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_items_list = []
    ask_items_list = []

    if orderbook:
        price_rounding = rouding_token1 if orderbook[0]['symbol'] == token1 else rouding_token2
        quantity_rounding = qty_token1 if orderbook[0]["symbol"] == token1 else qty_token2
        for level in orderbook:
            if level['side'] == 'Buy':
                bid_items_list.append(float(level['price']))
            else:
                ask_items_list.append(float(level['price']))

    if len(ask_items_list) > 0 and len(ask_items_list) > 0:

        ask_items_list.sort()
        bid_items_list.sort()
        bid_items_list.reverse()

        nearest_ask = ask_items_list[0]
        nearest_bid = bid_items_list[0]

        if direction == 'Long':
            mid_price = nearest_bid
            stop_loss = round(mid_price * (1 - stop_loss_fail_safe), price_rounding)
        else:
            mid_price = nearest_ask
            stop_loss = round(mid_price * (1 + stop_loss_fail_safe), price_rounding)

        quantity = round(capital / mid_price, quantity_rounding)

    return mid_price, stop_loss, quantity


def place_order(session, token, price, quantity, direction, stop_loss, limit_order_basis, trade_type=None) -> dict:
    """Place a limit order to long/short or close long/short."""

    trade_type = trade_type or 'Open'
    reduce_only = False
    side = 'Buy'

    if trade_type == 'Open':
        stop_loss = round(stop_loss, 3)
        if direction !='"Long':
            side = 'Sell'
    elif trade_type == 'Close':
        stop_loss = False
        reduce_only = True
        if direction == 'Long':
            side = 'Sell'

    if limit_order_basis:
        return session.place_active_order(
            symbol=token,
            side=side,
            order_type='Limit',
            qty=quantity,
            price=price,
            time_in_force='PostOnly',
            reduce_only=reduce_only,
            close_on_trigger=False,
            stop_loss=stop_loss
        )
    else:
        return session.place_active_order(
            symbol=token,
            side=side,
            order_type='Market',
            qty=quantity,
            time_in_force='GoodTillCancel',
            reduce_only=reduce_only,
            close_on_trigger=False,
            stop_loss=stop_loss
        )


def get_price_klines(token, session, timeframe, kline_limit) -> str:
    """Get price klines from public session."""

    time_start_seconds = get_start_time()
    prices = session.query_mark_price_kline(
        symbol = token,
        interval = timeframe,
        limit = kline_limit,
        from_time = time_start_seconds
    )

    if len(prices['result']) == kline_limit:
        return prices['result']


def get_latest_klines(token1, token2, session, timeframe, kline_limit) -> tuple:
    """Get last klines from public session."""

    series1, series2 = [], []
    prices1 = get_price_klines(token1, session, timeframe, kline_limit)
    prices2 = get_price_klines(token2, session, timeframe, kline_limit)

    if len(prices1) > 0:
        series1 = extract_close_prices(prices1)

    if len(prices2) > 0:
        series2 = extract_close_prices(prices2)

    return series1, series2


def get_latest_z_score(ws, session, token1, token2, timeframe, kline_limit) -> tuple:
    """Get latest asset orderbook prices and add dummy price."""

    ws_subs = get_ws_subscriptions
    orderbook1 = ws.fetch(ws_subs[0])
    orderbook2 = ws.fetch(ws_subs[1])
    midprice1, _, _ = get_trade_details(orderbook1)
    midprice2, _, _ = get_trade_details(orderbook2)

    series1, series2 = get_latest_klines(token1, token2, session, timeframe, kline_limit)

    if len(series1) > 0 and len(series2) > 0:
        series_1 = series1[:-1]
        series_2 = series2[:-1]
        series_1.append(midprice1)
        series_2.append(midprice2)

        data = calculate_cointegration(series1, series2)
        zscore = data['zscore'].to_list.tolist()[-1]
        signal_sign_positive = True if zscore > 0 else False

        return zscore, signal_sign_positive


def get_closed_pnl_info(token, session) -> str:
    """Get P&L info using private session."""

    pnl = session.closed_profit_and_loss(symbol=token)
    closed_pnl = 0

    if 'ret_msg' in pnl.keys():
        if pnl['ret_msg'] == 'OK':
            for item in pnl['result']['data']:
                closed_pnl += item['closed_pnl']

    return closed_pnl


def get_position_info(token, session) -> tuple:
    """Get position info from private position."""

    position = session.my_poition(symbol=token)
    side, size, pnl_un, pos_value = 0, "", 0, 0

    if 'ret_msg' in position.keys():
        if position['ret_msg'] == 'OK':
            if len(position['result']) == 2:
                if position['result'][0]['size'] > 0:
                    size = position['result'][0]['size']
                    side = "Buy"
                    pnl_un = position['result'][0]['unrealised_pnl']
                    pos_value = position['result'][0]['position_value']
                else:
                    size = position['result'][1]['size']
                    side = "Sell"
                    pnl_un = position['result'][1]['unrealised_pnl']
                    pos_value = position['result'][1]['position_value']

    return side, size, pnl_un, pos_value


def place_market_close_order(session, token, side, size) -> None:
    """Place market order to close position."""

    session.place_active_order(
        symbol=token,
        side=side,
        order_type='Market',
        qty=size,
        time_in_force='GoodTillCancel',
        reduce_only=True,
        close_on_trigger=False
    )


def initialise_order_execution(ws, token, direction, capital) -> str:
    """Initialize order on the public ws."""

    orderbook = ws.fetch(f'orderBookL2_25.{token}')

    if orderbook:
        mid_price, stop_loss, quantity = get_trade_details(orderbook, direction, capital)
        if quantity > 0:
            order = place_order(token, mid_price, quantity, direction, stop_loss)
            if "result" in order.keys():
                if 'order_id' in order['result']:
                    return order["result"]["order_id"]
    

def run_bot() -> None:
    """Entry point for this bot."""

    ########################
    #  Load env variables  #
    ########################

    env_vars = load_config()
    ws_public_url = env_vars['WS_PUBLIC_URL']
    token1 = env_vars['TOKEN1']
    token2 = env_vars['TOKEN2']
    api_url = env_vars['API_URL']
    api_key = env_vars['API_KEY']
    api_secret = env_vars['API_SECRET']
    signal_positive = env_vars['SIGNAL_POSTIVE']
    signal_negative = env_vars['SIGNAL_NEGATIVE']
    mass_loss_usdt = env_vars['MASS_LOSS_USDT']
    tradeable_capital = env_vars['TRADEABLE_CAPITAL']
    max_trades_per_signal = env_vars['MAX_TRADES_PER_SIGNAL']
    signal_trigger_thresh = env_vars['SIGNAL_TRIGGER_THRESH']
    timeframe = env_vars['TIMEFRAME']
    kline_limit = int(env_vars['KLINE_LIMIT'])


    #############################
    #  Start ws and sesssions   #
    #############################

    session_public = HTTP(api_url)
    ws_public = get_ws_connection(ws_public_url, token1, token2) 
    session_private = HTTP(api_url, api_key=api_key, api_secret=api_secret)
    

    #############################
    #       Order execution     #
    #############################
    
    set_leverage(signal_positive, session_public)
    set_leverage(signal_negative, session_public)

    zscore, signal_sign_positive = get_latest_z_score(ws_public, session_public, token1, token2, timeframe, kline_limit)
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    print(f"Timestamp: {current_time},", f"Z-score: {round(zscore,2)}")

    closed_pnl1 = get_closed_pnl_info(signal_positive, session_private)
    closed_pnl2 = get_closed_pnl_info(signal_negative, session_private)

    side1, size1, pnl_un1, pos_value1 = get_position_info(signal_positive, session_private)
    side2, size2, pnl_un2, pos_value2 = get_position_info(signal_negative, session_private)

    close_check2 = False
    close_check1 = (closed_pnl1 + closed_pnl2 + pnl_un1 + pnl_un2) <= mass_loss_usdt
    hot = True if abs(zscore) > signal_trigger_thresh else False
    if not hot:
        if size1 > 0 or size2 > 0:
            close_check2 = True

    if close_check1 or close_check2:

        print(f'Closing trades: {zscore}')
        halt_trading = True

        session_private.cancel_all_active_orders(symbol=signal_positive)
        session_private.cancel_all_active_orders(symbol=signal_negative)

        if size1 > 0:
            place_market_close_order(session_private, signal_positive, side2, size1) 

        if size2 > 0:
            place_market_close_order(session_private, signal_negative, side1, size2) 

    position_capital_allowance_total = tradeable_capital / 2
    trade_check1 = pos_value1 < position_capital_allowance_total and pos_value2 < position_capital_allowance_total
    trade_check2 = hot

    if trade_check1 and trade_check2:

        print(f'Placing trades: {zscore}')
        if signal_sign_positive:
            long_ticker = signal_positive
            short_ticker = signal_negative
        else:
            long_ticker = signal_negative
            short_ticker = signal_positive

        # Place market orders
        initialise_order_execution(ws_public, long_ticker, "Long", position_capital_allowance_total / max_trades_per_signal)
        initialise_order_execution(ws_public, short_ticker, "Short", position_capital_allowance_total / max_trades_per_signal)

'''

def run_bot():
    """
    Run bot
    """
    print('aaa')



if __name__ == "__main__":
    run_bot() 