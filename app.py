
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd

from src.validation import validate_sales_data
from src.business_rules import process_sales
from src.report_generator import create_excel_report
from src.dashboard import build_dashboard_metrics
from src.logger import log_error


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = Flask(__name__)
app.secret_key = "dit-sales-report-automation-key"

ROOT = Path(__file__).resolve().parent

UPLOAD_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"xlsx", "csv"}


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    report_path = OUTPUT_DIR / "Final_Sales_Report.xlsx"

    if not report_path.exists():
        return render_template(
            "dashboard.html",
            metrics=None,
            records=[]
        )

    try:
        df = pd.read_excel(report_path)

        # Check whether the DataFrame contains records
        if df.empty:
            return render_template(
                "dashboard.html",
                metrics=None,
                records=[]
            )

        metrics = build_dashboard_metrics(df)

        records = (
            df.head(100)
            .fillna("")
            .to_dict(orient="records")
        )

        return render_template(
            "dashboard.html",
            metrics=metrics,
            records=records
        )

    except Exception as exc:

        log_error(f"Dashboard loading failed: {exc}")

        flash(
            "Could not load dashboard. Please process the input file again.",
            "error"
        )

        return render_template(
            "dashboard.html",
            metrics=None,
            records=[]
        )


# --------------------------------------------------
# FILE UPLOAD AND PROCESSING
# --------------------------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    uploaded = request.files.get("sales_file")

    # Check file selection
    if uploaded is None or uploaded.filename == "":
        flash("Please select an Excel or CSV file.", "error")
        return redirect(url_for("home"))

    filename = secure_filename(uploaded.filename)

    # Validate extension
    if (
        "." not in filename
        or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS
    ):
        flash("Only Excel (.xlsx) and CSV files are supported.", "error")
        return redirect(url_for("home"))

    saved = UPLOAD_DIR / filename

    try:

        # Save uploaded file
        uploaded.save(saved)

        # Read Excel or CSV
        if saved.suffix.lower() == ".xlsx":
            raw = pd.read_excel(saved)
        else:
            raw = pd.read_csv(saved)

        # Check empty input
        if raw.empty:
            flash("The uploaded file contains no records.", "error")
            return redirect(url_for("home"))

        # Validate input data
        valid_df, errors = validate_sales_data(raw)

        # Process valid records
        processed = process_sales(valid_df)

        # Generate Excel report
        report_file = OUTPUT_DIR / "Final_Sales_Report.xlsx"

        create_excel_report(
            processed,
            errors,
            report_file
        )

        # Check rejected records safely
        if len(errors) > 0:

            flash(
                f"Report created successfully. "
                f"{len(errors)} row(s) were rejected. "
                f"Please check the Error Report.",
                "warning"
            )

        else:

            flash(
                "Sales report generated successfully!",
                "success"
            )

        return redirect(url_for("dashboard"))

    except Exception as exc:

        log_error(
            f"File processing failed for {filename}: {exc}"
        )

        flash(
            f"Processing failed: {exc}",
            "error"
        )

        return redirect(url_for("home"))


# --------------------------------------------------
# DOWNLOAD REPORTS
# --------------------------------------------------

@app.route("/download/<kind>")
def download(kind):

    names = {
        "sales": "Final_Sales_Report.xlsx",
        "errors": "Error_Report.xlsx"
    }

    filename = names.get(kind)

    if filename is None:
        flash("Unknown report type.", "error")
        return redirect(url_for("dashboard"))

    path = OUTPUT_DIR / filename

    if not path.exists():
        flash("The requested report is not available yet.", "error")
        return redirect(url_for("dashboard"))

    return send_file(
        path,
        as_attachment=True
    )


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

@app.route("/about")
def about():
    return render_template("about.html")


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
