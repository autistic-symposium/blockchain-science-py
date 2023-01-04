# -*- encoding: utf-8 -*-
# src/bots/bot1.py
# author: steinkirch
# Deploy trading bot1.


class BbBotOne:
    """Deploy trading bot one."""

    def __init__(self, env_vars):
        """Initialize the class."""
        self.env_vars = env_vars

    def run(self):
        import asyncio
        from src.markets.bybit import BybitCex
        
        coins = self.env_vars["BOT_COINS"].split(',')
        market = self.env_vars["BOT_MARKET"].upper()

        b = BybitCex(self.env_vars, ws=True, market=market)
        asyncio.get_event_loop().run_until_complete(b.orderbook_ws(coins[0], coins[1]))


        return f"Bot 1 is succesful running"
