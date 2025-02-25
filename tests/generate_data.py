import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define stock codes and sector mappings
stocks = [
    {"code": "ADH", "sector": "Consumer Discretionary"},
    {"code": "BHP", "sector": "Materials"},
    {"code": "CBA", "sector": "Financials"},
    {"code": "TLS", "sector": "Communication Services"},
    {"code": "WES", "sector": "Consumer Staples"}
]

# Generate 10 weekdays excluding weekends
start_date = datetime(2024, 5, 1)
dates = []
while len(dates) < 10:
    if start_date.weekday() < 5:  # Weekday check (0=Monday, 4=Friday)
        dates.append(start_date)
    start_date += timedelta(days=1)

# Introduce a missing day (removing the 5th day for testing)
missing_day = dates[4]
dates.remove(missing_day)

# Generate sample data
data = []
np.random.seed(42)  # For reproducibility

for date in dates:
    for stock in stocks:
        num_snapshots = np.random.choice([2, 3, 4])  # Random snapshots per day
        last_price = round(np.random.uniform(2, 100), 2)  # Starting price

        for _ in range(num_snapshots):
            change = round(np.random.uniform(-1, 1), 2)
            last_price = max(1.0, round(last_price + change, 2))  # Ensure price doesn't go negative
            open_price = round(last_price + np.random.uniform(-0.5, 0.5), 2)
            high = max(open_price, last_price + np.random.uniform(0, 0.5))
            low = min(open_price, last_price - np.random.uniform(0, 0.5))
            prev_close = round(last_price - change, 2)

            data.append([
                #date.strftime("%d/%m/%Y"),  # aest_day
                stock["code"],  # code
                np.random.randint(500, 600),  # index (random id)
                np.random.randint(2000, 3000),  # id
                np.random.randint(10, 20),  # sector_id
                f"{stock['code']} Ltd",  # title
                stock["code"],  # path
                False,  # is_asr
                last_price,  # last price
                change,  # change
                round((change / prev_close) * 100, 2),  # change_percent
                open_price,  # open
                high,  # high
                low,  # low
                prev_close,  # previous_close
                round(last_price * 0.8, 2),  # 52w_low (approx 80% of last)
                round(last_price * 1.2, 2),  # 52w_high (approx 120% of last)
                round(np.random.uniform(1000, 5000), 1),  # turnover
                round(np.random.uniform(-10, 20), 2),  # ytd_percent_change
                round(np.random.uniform(-15, 15), 2),  # 1yr_percent_change
                False,  # star_stock
                np.random.randint(100000000, 1000000000),  # market_cap
                np.random.randint(500, 5000),  # volume
                datetime.utcnow().isoformat()+'Z',  # last_traded
                "OPEN",  # status
                None,  # deleted_at
                datetime(2024, 9, 29, 7, 45, 55).isoformat()+'Z',  # created_at
                date.isoformat()+'Z',  # updated_at
                np.random.randint(300000, 400000),  # month_volume
                round(np.random.uniform(-5, 5), 3),  # week_percent_change
                round(np.random.uniform(-10, 10), 3),  # month_percent_change
                1,  # type
                {"id": np.random.randint(100, 200), "gics_sector": stock["sector"]},  # company_sector
                stock["sector"],  # sector
                #(date + timedelta(hours=10)).isoformat(),  # aest_time
                #date.strftime("%d/%m/%Y")  # aest_day_datetime
            ])

# Convert to DataFrame
df_test = pd.DataFrame(data, columns=[
    "code", "index", "id", "sector_id", "title", "path", "is_asr",
    "last", "change", "change_percent", "open", "high", "low", "previous_close",
    "52w_low", "52w_high", "turnover", "ytd_percent_change", "1yr_percent_change",
    "star_stock", "market_cap", "volume", "last_traded", "status", "deleted_at",
    "created_at", "updated_at", "month_volume", "week_percent_change", "month_percent_change",
    "type", "company_sector", "sector"
])

# Display sample rows
df_test.head(10)

df_test.to_csv("test_data_raw_data.csv", index = False)
