import os
import time
import logging
from typing import Dict, Any, Generator
import MetaTrader5 as mt5

# Setup logging for Random's framework
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (Forex-Ingest) %(message)s")
logger = logging.getLogger(__name__)

class MT5DataIngestor:
    def __init__(self, symbol: str, path: str = None, login: int = None, password: str = None, server: str = None):
        self.symbol = symbol.upper()
        self.path = path
        self.login = login
        self.password = password
        self.server = server
        self.initialized = False

    def connect(self) -> bool:
        """Initializes the connection to the MT5 terminal client."""
        logger.info("Attempting to initialize connection to MT5...")
        
        # Build initialization args based on user configuration
        init_args = {}
        if self.path: init_args['path'] = self.path
        if self.login: init_args['login'] = self.login
        if self.password: init_args['password'] = self.password
        if self.server: init_args['server'] = self.server

        if not mt5.initialize(**init_args):
            logger.error(f"MT5 Initialization failed. Error code: {mt5.last_error()}")
            return False

        # Ensure the targeted Forex pair is visible in Market Watch
        if not mt5.symbol_select(self.symbol, True):
            logger.error(f"Failed to select symbol {self.symbol}. Ensure it exists in your broker asset list.")
            mt5.shutdown()
            return False

        self.initialized = True
        logger.info(f"Successfully hooked Random to MT5 terminal. Monitoring asset: {self.symbol}")
        return True

    def stream_live_ticks(self, poll_interval: float = 0.1) -> Generator[Dict[str, Any], None, None]:
        """
        Polls MT5 for the latest symbol tick data.
        Yields structured updates only when a change in timestamp occurs.
        """
        if not self.initialized and not self.connect():
            raise ConnectionError("Cannot stream data without an active MT5 terminal connection.")

        last_tick_time = 0

        try:
            while True:
                tick = mt5.symbol_info_tick(self.symbol)
                if tick is not None:
                    # MT5 tick time is provided in epoch seconds
                    if tick.time_msc > last_tick_time:
                        last_tick_time = tick.time_msc
                        
                        # Normalize data structure to insulate Random from platform changes
                        tick_data = {
                            "timestamp": tick.time,
                            "timestamp_msc": tick.time_msc,
                            "bid": tick.bid,
                            "ask": tick.ask,
                            "spread": round(tick.ask - tick.bid, 5),
                            "volume": tick.volume
                        }
                        yield tick_data
                else:
                    logger.warning(f"Could not retrieve tick data for {self.symbol}. Terminal might be lagging.")

                # High-frequency sleep to prevent burning CPU cycles
                time.sleep(poll_interval)

        except KeyboardInterrupt:
            logger.info("Live data streaming interrupted by user command.")
        finally:
            self.disconnect()

    def disconnect(self):
        """Clean resource breakdown."""
        if self.initialized:
            mt5.shutdown()
            self.initialized = False
            logger.info("Disconnected from MetaTrader 5 interface safely.")

if __name__ == "__main__":
    # Local environment validation block
    # NOTE: Keep credentials in environment variables or configuration files!
    SYMBOL_TO_TRACK = "EURUSD"
    
    ingestor = MT5DataIngestor(symbol=SYMBOL_TO_TRACK)
    
    print(f"--- Starting Live Stream Feed for Random on {SYMBOL_TO_TRACK} ---")
    for live_tick in ingestor.stream_live_ticks(poll_interval=0.05):
        print(f"Tick Stream -> Time: {live_tick['timestamp_msc']} | Bid: {live_tick['bid']} | Ask: {live_tick['ask']} | Spread: {live_tick['spread']:.5f}")
