import pandas as pd

def process_sales(df):
    """Apply the T3 brief's achievement and incentive-rate thresholds."""
    result = df.copy()
    result["Achievement_Percentage"] = (result["Achieved"] / result["Target"] * 100).round(2)
    result["Incentive_Rate"] = result["Achievement_Percentage"].apply(
        lambda value: 0.15 if value >= 120 else (0.10 if value >= 100 else 0.0)
    )
    result["Performance_Status"] = result["Achievement_Percentage"].apply(
        lambda value: "High Performer" if value >= 120 else ("Target Achieved" if value >= 100 else "Below Target")
    )
    # The assessment's input schema does not include Salary, although its example
    # calculates incentive amount using salary. Therefore this app reports the
    # applicable incentive rate and does not invent an incentive amount.
    return result
