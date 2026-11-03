
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="DIT Sales Report Automation",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DIT Sales Report Automation")
st.write("Upload your sales Excel or CSV file to generate a sales performance report.")

uploaded_file = st.file_uploader(
    "Upload Sales Data",
    type=["xlsx", "csv"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Uploaded Sales Data")
        st.dataframe(df, use_container_width=True)

        df.columns = df.columns.str.strip()

        st.subheader("Data Validation")

        required_columns = [
            "Employee Name",
            "Sales Target",
            "Sales Achieved"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            st.error("Missing columns: " + ", ".join(missing))
            st.info(
                "Your file must contain Employee Name, "
                "Sales Target and Sales Achieved columns."
            )
        else:
            df["Sales Target"] = pd.to_numeric(
                df["Sales Target"], errors="coerce"
            )
            df["Sales Achieved"] = pd.to_numeric(
                df["Sales Achieved"], errors="coerce"
            )

            df = df.dropna(
                subset=["Employee Name", "Sales Target", "Sales Achieved"]
            )

            df["Achievement %"] = (
                df["Sales Achieved"] /
                df["Sales Target"].replace(0, pd.NA)
            ) * 100

            df["Achievement %"] = df["Achievement %"].fillna(0)

            total_target = df["Sales Target"].sum()
            total_sales = df["Sales Achieved"].sum()

            overall = (
                total_sales / total_target * 100
                if total_target else 0
            )

            st.subheader("Sales Performance Dashboard")

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Sales Target", f"{total_target:,.2f}")
            c2.metric("Total Sales Achieved", f"{total_sales:,.2f}")
            c3.metric("Overall Achievement", f"{overall:.2f}%")

            st.subheader("Employee Performance")
            st.dataframe(
                df.sort_values(
                    "Sales Achieved", ascending=False
                ),
                use_container_width=True
            )

            if not df.empty:
                top_employee = df.loc[
                    df["Sales Achieved"].idxmax(),
                    "Employee Name"
                ]
                st.success(f"Top Sales Performer: {top_employee}")

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Sales Report"
                )

            st.download_button(
                "📥 Download Sales Report",
                data=output.getvalue(),
                file_name="DIT_Sales_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload an Excel or CSV sales dataset to begin.")
