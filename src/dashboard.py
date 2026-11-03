def build_dashboard_metrics(df):
    if df.empty:
        return {"total": 0, "achieved": 0, "target": 0, "average": 0, "top_name": "—", "top_region": "—"}
    top = df.sort_values("Achievement_Percentage", ascending=False).iloc[0]
    return {
        "total": int(len(df)),
        "achieved": round(float(df["Achieved"].sum()), 2),
        "target": round(float(df["Target"].sum()), 2),
        "average": round(float(df["Achievement_Percentage"].mean()), 2),
        "top_name": str(top["Employee_Name"]),
        "top_region": str(top["Region"])
    }
