test_config = [
    {"type": "moving_average",
        'day_small': 9,
         'day_long': 21,# Difference % between high and low
         "difference_threshold_max": 10,  # Difference % between high and low
        "difference_threshold_min": 0,
        "buy_status": True,  
        "min_streak": 2,  
        "max_streak": 10  
    },
    {"type":"gradient_average",
     'column':'last',
        "num_days": [9, 20, 3, 4, 5, 6],  
        "greater_than": 0,  
        "less_than": 4.0  
    },
    {"type": "RSI",
     "min_periods": 13,
     "window":14,
    'rsi_max': 45}
]