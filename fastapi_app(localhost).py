
# FastAPI Excel Processor
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
import uvicorn
import re
from pathlib import Path

# ===== Initialize =====
app = FastAPI()
EXCEL_FILE_PATH = "Data/capbudg.xls"
# ===== Excel Structure Configuration =====
TABLE_SECTIONS = {
    "Initial Investment": {
        "rows": (3, 9),
        "columns": (1, 3),
        "label_col": 0 # to set the start point for row sum
    },
    "Revenue Projections": {
        "rows": (3, 6),
        "label_col": 4 # to set the start point for row sum
    },
    "Operating Expenses": {
        "rows": (38, 48),
        "columns": (1, 9),
        "label_col": 0  # to set the start point for row sum
    }
}

# ===== Helper Functions =====
def normalize_name(name: str) -> str:
    """Convert to single spaces and lowercase for reliable matching"""
    return re.sub(r'\s+', ' ', name.strip().lower())

def get_table_data(df, table_name: str):
    """Extract rows for a specific table"""
    if table_name not in TABLE_SECTIONS:
        return None
    start, end = TABLE_SECTIONS[table_name]["rows"]
    return df.iloc[start:end+1]

# ===== API Endpoints =====
@app.get("/list_tables")
async def list_tables():
    return {"tables": list(TABLE_SECTIONS.keys())}

@app.get("/get_table_details")
async def get_table_details(table_name: str = Query(...)):
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="CapBudgWS", header=None)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Excel file not found")

    table_data = get_table_data(df, table_name)
    if table_data is None:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

    label_col = TABLE_SECTIONS[table_name].get("label_col", 0)
    row_names = (
        table_data.iloc[:, label_col]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    return {
        "table_name": table_name,
        "row_names": row_names
    }

@app.get("/row_sum")
async def calculate_row_sum(
    table_name: str = Query(...),
    row_name: str = Query(...)
):
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="CapBudgWS", header=None)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Excel file not found")

    table_data = get_table_data(df, table_name)
    if table_data is None:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

    label_col = TABLE_SECTIONS[table_name].get("label_col", 0)
    normalized_target = normalize_name(row_name)

    matching_rows = [
        i for i, x in enumerate(table_data.iloc[:, label_col].astype(str))
        if normalize_name(x) == normalized_target
    ]

    if not matching_rows:
        raise HTTPException(
            status_code=404,
            detail=f"Row '{row_name}' not found in table '{table_name}'"
        )

    row_idx = matching_rows[0]
    start_col, end_col = TABLE_SECTIONS[table_name]["columns"]
    numeric_values = pd.to_numeric(
        table_data.iloc[row_idx, start_col:end_col + 1],
        errors='coerce'
    ).dropna()

    return {
        "table_name": table_name,
        "row_name": table_data.iloc[row_idx, label_col],
        "sum": float(numeric_values.sum()) if not numeric_values.empty else 0.0
    }

# ===== Main Execution =====
if __name__ == "__main__":
    # Verify file exists
    if not Path(EXCEL_FILE_PATH).exists():
        raise FileNotFoundError(f"Excel file not found at {EXCEL_FILE_PATH}")

    # Start server
    print(f"Starting server at http://localhost:9090")
    uvicorn.run(app, host="0.0.0.0", port=9090, log_level="debug")