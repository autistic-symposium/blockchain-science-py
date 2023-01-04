# -*- encoding: utf-8 -*-
# src/bots/bot1.py
# author: steinkirch
# Deploy trading bot1.

import asyncio
import src.utils.os as utils
from src.markets.bybit import BybitCex

class BbBotOne:
    """Deploy trading bot one."""

    def __init__(self, env_vars):

        self._env_vars = env_vars
        self._market = env_vars["BOT_MARKET"].upper()

        try:
            self._coin1 = env_vars["BOT_COINS"].split(',')[0].strip()
            self._coin2 = env_vars["BOT_COINS"].split(',')[1].strip()
        except IndexError:
            utils.exit_with_error(f'Define two coins string for bot1.')
    
        self._session = None
        self._setup()

    #########################
    #   private methods     #
    #########################

    def _setup(self):
        """Setup the bot."""

        self._session = BybitCex(self._env_vars, ws=True, market=self._market)
        self._session.set_leverage(self._coin1, is_isolated=True, 
                                            buy_leverage=1, sell_leverage=1)
        self._session.set_leverage(self._coin2, is_isolated=True, 
                                            buy_leverage=1, sell_leverage=1)


    #########################
    #   public methods      #
    #########################
    
    def run(self):

        try:
            asyncio.get_event_loop().run_until_complete(
                self._session.orderbook_ws(self._coin1, self._coin2))
            
            return True

        except KeyboardInterrupt as e:
            utils.log_error(f"Bot 1 is stopped: {e}")
            return False

