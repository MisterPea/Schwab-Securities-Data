from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, List


@dataclass
class OptionExpirationType:
    expirationDate: str  # Example: "2026-12-18", represents the expiration date of the option.
    daysToExpiration: int  # Number of days remaining until expiration.
    expirationType: Literal["S", "W", "Q"]  # 'S' for Standard, 'W' for Weekly, 'Q' for Quarterly.
    settlementType: Literal["P", "C"]  # 'P' for Physical, 'C' for Cash Settlement.
    optionRoots: str  # Root symbol for the option, e.g., "AAPL".
    standard: bool  # True if it's a standardized option, false otherwise.

@dataclass
class OptionChainRequest:
    symbol: str  # The symbol for the underlying asset, e.g., "AAPL"
    contractType: Literal["CALL", "PUT", "ALL"]  # The type of option contract: CALL, PUT, or ALL
    strikeCount: Optional[int] = None  # Number of strikes above/below ATM price to return
    includeUnderlyingQuote: Optional[bool] = False  # Whether to include the underlying asset's quote
    strategy: Literal["SINGLE", "ANALYTICAL", "COVERED", "VERTICAL", "CALENDAR", "STRANGLE", "STRADDLE",
    "BUTTERFLY", "CONDOR", "DIAGONAL", "COLLAR", "ROLL"] = "SINGLE"  # The strategy to use
    interval: Optional[float] = None  # Strike interval for spread strategy chains
    strike: Optional[float] = None  # Specific strike price
    range: Optional[str] = None  # Range (e.g., ITM, NTM, OTM)
    fromDate: Optional[str] = None  # From date (format: yyyy-MM-dd)
    toDate: Optional[str] = None  # To date (format: yyyy-MM-dd)
    volatility: Optional[float] = None  # Volatility for ANALYTICAL strategy calculations
    underlyingPrice: Optional[float] = None  # Underlying price for ANALYTICAL strategy calculations
    interestRate: Optional[float] = None  # Interest rate for ANALYTICAL strategy calculations
    daysToExpiration: Optional[int] = None  # Days to expiration for ANALYTICAL strategy calculations
    expMonth: Literal[
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "ALL"] = "ALL" # Expiration month
    optionType: Optional[str] = None  # Option type
    entitlement: Optional[Literal["PN", "NP", "PP"]] = None  # Entitlement (retail token): PP, NP, PN

@dataclass
class OptionDeliverable:
    symbol: str
    assetType: str
    deliverableUnits: int


@dataclass
class OptionData:
    putCall: str
    symbol: str
    description: str
    exchangeName: str
    bid: float
    ask: float
    last: float
    mark: float
    bidSize: int
    askSize: int
    bidAskSize: str
    lastSize: int
    highPrice: float
    lowPrice: float
    openPrice: float
    closePrice: float
    totalVolume: int
    tradeTimeInLong: int
    quoteTimeInLong: int
    netChange: float
    volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    openInterest: int
    timeValue: float
    theoreticalOptionValue: float
    theoreticalVolatility: float
    optionDeliverablesList: List[OptionDeliverable]
    strikePrice: float
    expirationDate: str
    daysToExpiration: int
    expirationType: str
    lastTradingDay: int
    multiplier: int
    settlementType: str
    deliverableNote: str
    percentChange: float
    markChange: float
    markPercentChange: float
    intrinsicValue: float
    extrinsicValue: float
    optionRoot: str
    exerciseType: str
    high52Week: float
    low52Week: float
    nonStandard: bool
    pennyPilot: bool
    inTheMoney: bool
    mini: bool


@dataclass
class Underlying:
    symbol: str
    description: str
    change: float
    percentChange: float
    close: float
    quoteTime: int
    tradeTime: int
    bid: float
    ask: float
    last: float
    mark: float
    markChange: float
    markPercentChange: float
    bidSize: int
    askSize: int
    highPrice: float
    lowPrice: float
    openPrice: float
    totalVolume: int
    exchangeName: str
    fiftyTwoWeekHigh: float
    fiftyTwoWeekLow: float
    delayed: bool


@dataclass
class OptionReturnType:
    symbol: str
    status: str
    underlying: Underlying
    strategy: str
    interval: int
    isDelayed: bool
    isIndex: bool
    interestRate: float
    underlyingPrice: float
    volatility: float
    daysToExpiration: int
    numberOfContracts: int
    assetMainType: str
    assetSubType: str
    isChainTruncated: bool
    callExpDateMap: Dict[str, Dict[float, List[OptionData]]]
