# Algo Futures Roll Bot

![Language](https://img.shields.io/badge/language-Python_3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Prototype-orange.svg)

## Overview

**Algo Futures Roll Bot** is an asynchronous, event-driven trading engine designed to automate the "rolling" of futures positions (Calendar Spreads). 

In derivatives markets, traders must migrate positions from expiring contracts (Near Month) to the next cycle (Far Month). Executing these legs separately introduces **"Legging Risk"** (price slippage between trades). This bot solves that problem by monitoring the spread differential in real-time and executing atomic roll orders when the market spread deviates from the theoretical Fair Value.

## Key Features

- **Fair Value Modeling:** Calculates the theoretical spread price using the **Cost of Carry** model ($S \cdot e^{(r-q)t}$), accounting for interest rates and time to expiry.
- **Asynchronous Architecture:** Built on Python's `asyncio` for non-blocking, high-frequency data polling.
- **Atomic Execution:** Prioritizes native exchange combo orders (Spread Orders) to eliminate legging risk.
- **Smart Fallback:** automatically degrades to simultaneous market orders if the exchange does not support native spreads.
- **Modular Design:** Decoupled architecture separating Strategy, Broker Connection, and Analytics.

## Mathematical Logic
The bot evaluates the Fair Spread ($F_{spread}$) versus the Market Spread ($M_{spread}$).
$$F_{spread} = Spot \times (e^{(r-q)T_{far}} - e^{(r-q)T_{near}})$$
Where:
* $r$ = Risk-free interest rate
* $q$ = Dividend yield (if applicable)
* $T$ = Time to expiry (in years)

Execution Signal:The bot triggers a roll when:
$$M_{spread} < (F_{spread} - \text{RiskThreshold})$$

## Disclaimer
IMPORTANT: READ BEFORE USE

This software is for educational and research purposes only.

* No Financial Advice: Nothing in this repository constitutes financial advice or a recommendation to buy or sell any financial instrument.

* Risk Warning: Algorithmic trading involves significant risk. Bugs, API failures, or market volatility can result in substantial financial loss.

* Liability: The authors and contributors are not liable for any losses incurred through the use of this software. You use this code entirely at your own risk. Always test thoroughly in a paper-trading environment before deploying real capital.