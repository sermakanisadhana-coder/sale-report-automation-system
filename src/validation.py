import pandas as pd

REQUIRED_COLUMNS = ["Employee_ID", "Employee_Name", "Target", "Achieved", "Region"]

def validate_sales_data(df):
    """Return (valid_rows, rejected_rows). Keeps the first occurrence of each Employee_ID."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))

    valid, errors, seen = [], [], set()
    for row_number, row in df.iterrows():
        excel_row = row_number + 2
        employee_id = str(row.get("Employee_ID", "")).strip()
        name = str(row.get("Employee_Name", "")).strip()
        region = str(row.get("Region", "")).strip()
        reason = None

        if not employee_id or employee_id.lower() == "nan":
            reason = "Employee_ID is required"
        elif employee_id in seen:
            reason = "Duplicate Employee_ID"
        elif not name or name.lower() == "nan":
            reason = "Employee_Name is required"
        elif not region or region.lower() == "nan":
            reason = "Region is required"
        else:
            try:
                target = float(row["Target"])
                achieved = float(row["Achieved"])
                if target <= 0:
                    reason = "Target must be greater than zero"
                elif achieved < 0:
                    reason = "Achieved sales cannot be negative"
            except (TypeError, ValueError):
                reason = "Target and Achieved must be numeric"

        if reason:
            errors.append({"Excel_Row": excel_row, "Employee_ID": employee_id, "Reason": reason})
            continue

        seen.add(employee_id)
        valid.append({
            "Employee_ID": employee_id,
            "Employee_Name": name,
            "Target": target,
            "Achieved": achieved,
            "Region": region
        })
    return pd.DataFrame(valid, columns=REQUIRED_COLUMNS), pd.DataFrame(errors, columns=["Excel_Row", "Employee_ID", "Reason"])
