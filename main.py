from tradingview_ta import TA_Handler
import json


class Interval:
    INTERVAL_1_MINUTE: str = "1m"
    INTERVAL_5_MINUTES: str = "5m"
    INTERVAL_15_MINUTES: str = "15m"
    INTERVAL_30_MINUTES: str = "30m"
    INTERVAL_1_HOUR: str = "1h"
    INTERVAL_2_HOURS: str = "2h"
    INTERVAL_4_HOURS: str = "4h"
    INTERVAL_1_DAY: str = "1d"
    INTERVAL_1_WEEK: str = "1W"
    INTERVAL_1_MONTH: str = "1M"


class GetAnalysis:
    def __init__(
            self,
            screener: str="crypto",
            exchange: str="BINANCE",
            symbol: str="BTCUSD",
            timestap: str=Interval.INTERVAL_5_MINUTES
        ) -> None:
        self.screener = screener
        self.exchange = exchange
        self.symbol = symbol
        self.timestap = timestap


    def analysis(self) -> dict:
        company = TA_Handler(
            symbol=self.symbol,
            screener=self.screener,
            exchange=self.exchange,
            interval=self.timestap
        )
        return company.get_analysis()


    def get_start_point(self) -> int:
        return self.analysis().indicators["close"]


if __name__ == "__main__":
    # Ваши данные
    ETHUSD = GetAnalysis(
        exchange="BITSTAMP",
        screener="crypto",
        symbol="ETHUSD",
        timestap=Interval.INTERVAL_15_MINUTES
    )
    price = ETHUSD.get_start_point()
    analysis = ETHUSD.analysis().summary

    element = str(analysis['RECOMMENDATION'])
    if element.upper() in ["BUY", "STRONG_BUY"]:
        element = "BUY"
    if element.upper() in ["SELL", "STRONG_SELL"]:
        element = "SELL"

    procent = round(analysis[element] * 100 / sum([analysis['BUY'], analysis['SELL'], analysis['NEUTRAL']]))
    with open("data.json", "w+") as f:
        f.write(json.dumps({
            "procent": f"{procent}%",
            "recommendation": " ".join(analysis['RECOMMENDATION'].split("_")).lower(),
            "price": price,
            "analysis_info": {
                "symbol": ETHUSD.symbol,
                "screener": ETHUSD.screener,
                "exchange": ETHUSD.exchange,
                "timestap": ETHUSD.timestap
            }
        }, indent=4))