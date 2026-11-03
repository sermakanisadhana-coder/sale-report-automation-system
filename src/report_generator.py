from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path

def style_sheet(ws):
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="193B63")
        cell.alignment = Alignment(horizontal="center")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for column in ws.columns:
        max_len = max(len(str(c.value or "")) for c in column)
        ws.column_dimensions[get_column_letter(column[0].column)].width = min(max(max_len + 3, 12), 32)

def create_excel_report(processed, errors, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with __import__("pandas").ExcelWriter(output_path, engine="openpyxl") as writer:
        processed.to_excel(writer, sheet_name="Sales Report", index=False)
        errors.to_excel(writer, sheet_name="Rejected Rows", index=False)
        summary = __import__("pandas").DataFrame([
            ["Total Valid Employees", len(processed)],
            ["Total Target", processed["Target"].sum() if not processed.empty else 0],
            ["Total Achieved", processed["Achieved"].sum() if not processed.empty else 0],
            ["Average Achievement %", processed["Achievement_Percentage"].mean() if not processed.empty else 0],
            ["High Performers", int((processed["Performance_Status"] == "High Performer").sum()) if not processed.empty else 0],
            ["Below Target", int((processed["Performance_Status"] == "Below Target").sum()) if not processed.empty else 0],
        ], columns=["Metric", "Value"])
        summary.to_excel(writer, sheet_name="Summary", index=False)
        for ws in writer.book.worksheets:
            style_sheet(ws)
    error_path = output_path.parent / "Error_Report.xlsx"
    with __import__("pandas").ExcelWriter(error_path, engine="openpyxl") as writer:
        errors.to_excel(writer, sheet_name="Errors", index=False)
        style_sheet(writer.book.active)
