# DIT-P05 Sales Report Automation

A Flask website that accepts Excel/CSV sales data, validates records, calculates achievement percentage and incentive rates, and generates Excel reports.

## Required input columns
- Employee_ID
- Employee_Name
- Target
- Achieved
- Region

## Business rules
- Achievement % = (Achieved / Target) * 100
- Achievement >= 120%: incentive rate 15%
- Achievement >= 100%: incentive rate 10%
- Below 100%: incentive rate 0%

**Assessment clarification:** the brief's input columns do not include Salary, but its sample incentive calculation uses Salary as the incentive base. This implementation reports the incentive rate only and does not invent an incentive amount. Confirm the base with the project mentor.

## Setup (Windows)
1. Install Python 3.10 or later.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Create and activate a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

5. Install packages:

```powershell
pip install -r requirements.txt
```

6. Start the website:

```powershell
python app.py
```

7. Open the local address printed in the terminal (usually http://127.0.0.1:5000).

## Test data
Use `input/Sample_Sales_Data.xlsx`. Upload it through the website.

## Generated files
- `output/Final_Sales_Report.xlsx` (Sales Report, Rejected Rows, Summary sheets)
- `output/Error_Report.xlsx`
- `logs/error_log.txt`

## Notes
- Keep confidential real company data out of public repositories.
- This is a local student project starter, not a production-ready authenticated system.
- Change `app.secret_key` and disable debug mode before any deployment.
