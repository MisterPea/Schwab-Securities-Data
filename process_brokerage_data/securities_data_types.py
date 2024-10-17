from typing import Literal, TypedDict

# Price History Types
PeriodType = Literal['day', 'month', 'year', 'ytd']
FrequencyType = Literal['minute', 'daily', 'weekly', 'monthly']

DayPeriod = Literal[1, 2, 3, 4, 5, 10]
MonthPeriod = Literal[1, 2, 3, 6]
YearPeriod = Literal[1, 2, 3, 5, 10, 15, 20]
YtdPeriod = Literal[1]
Period = DayPeriod | MonthPeriod | YearPeriod | YtdPeriod

MinuteFrequency = Literal[1, 5, 10, 15, 30]
OtherFrequency = Literal[1]

Frequency = MinuteFrequency | OtherFrequency


class PriceHistoryOptions(TypedDict):
    period_type: PeriodType
    period: Period
    frequency_type: FrequencyType
    frequency: Frequency
    extended_hours: bool
    need_previous_close: bool
    start_date: str
    end_date: str


# Movers Types
IndexSymbolType = Literal[
    "EQUITY_ALL",
    "INDEX_ALL",
    "OPTION_ALL",
    "OPTION_PUT",
    "OPTION_CALL",
    "$DJI",
    "$COMPX",
    "$SPX",
    "NYSE",
    "NASDAQ",
    "OTCBB"
]

MoverSortType = Literal[
    "VOLUME",
    "TRADES",
    "PERCENT_CHANGE_UP",
    "PERCENT_CHANGE_DOWN"
]

MoversFreqType = Literal[0, 1, 5, 10, 30, 60]

# Market Hours Types
MarketTimeType = Literal["equity", "option", "bond", "future", "forex"]
