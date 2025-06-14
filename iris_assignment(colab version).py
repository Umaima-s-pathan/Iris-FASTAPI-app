# -*- coding: utf-8 -*-
"""iris assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iAyos1l80t0pJIHHqbmFZLAoQ2BFi59U

# FastAPI Excel Processor
"""

!pip install fastapi uvicorn pandas openpyxl nest-asyncio pyngrok

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import pandas as pd
from google.colab import files
import nest_asyncio
from pyngrok import ngrok, conf
import uvicorn
import re
import asyncio
from getpass import getpass

# ===== Async Environment =====
nest_asyncio.apply()

# ===== Initialize =====
app = FastAPI()
EXCEL_FILE_PATH = None
public_url = None

# ===== Excel Structure Configuration =====
TABLE_SECTIONS = {
    "Initial Investment": {
        "rows": (3, 9),
        "label_col": 0 # to set the start point for row sum
    },
    "Revenue Projections": {
        "rows": (3, 6),
        "columns": (4, 8),
        "label_col": 4  # to set the start point for row sum
    },
    "Operating Expenses": {
        "rows": (38, 48),
        "columns": (1, 9),
        "label_col": 0   # to set the start point for row sum
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
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="CapBudgWS", header=None)
    table_data = get_table_data(df, table_name)

    if table_data is None:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

    # Use label_col from config or default to 0
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
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="CapBudgWS", header=None)
    table_data = get_table_data(df, table_name)

    if table_data is None:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

    # Get the label column (where row names are stored)
    label_col = TABLE_SECTIONS[table_name].get("label_col", 0)

    # Normalize the row name and match it in the configured label_col
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

    # Sum numeric values in the defined column range
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

# ===== Startup =====
@app.on_event("startup")
async def startup_event():
    global EXCEL_FILE_PATH, public_url

    # Upload file
    uploaded = files.upload()
    EXCEL_FILE_PATH = next(iter(uploaded.keys()))

    # Start ngrok
    try:
        ngrok_auth = getpass("Enter ngrok authtoken (skip if in Colab secrets): ")
        if ngrok_auth.strip():
            conf.get_default().auth_token = ngrok_auth.strip()

        ngrok_tunnel = ngrok.connect(9090)
        public_url = ngrok_tunnel.public_url
        print(f"\nAPI Ready at: {public_url}")
        print("Test endpoints:")
        print(f"  {public_url}/list_tables")
    except Exception as e:
        print(f"Ngrok error: {e}\nContinuing without public URL")

# ===== Server Startup =====
def run_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=9090)
    server = uvicorn.Server(config)
    asyncio.run(server.serve())

# Start ngrok tunnel and server
if __name__ == "__main__":
    run_server()





df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="CapBudgWS", header=None)
row = df.iloc[38, 1:9]  # Revenues row, cols B to I
print(row.tolist())

revenues_row = df.iloc[37, 2:10]
print("Revenues:", revenues_row.tolist())
print("Sum:", revenues_row.sum())

row_38 = df.iloc[38, 0:15]  # Columns A to O
print("Row 38 Full:", row_38.tolist())
print("Len:", len(row_38.dropna()))

revenues_row = df.iloc[38, 2:10]
print("Revenues:", revenues_row.tolist())
print("Sum:", revenues_row.sum())

revenues_row = df.iloc[38, 2:10]
for i, value in enumerate(revenues_row):
    print(f"Year {i+1}: {value} ({type(value)})")

revenues_row = df.iloc[38, 2:10]
print("Values:", revenues_row.tolist())
print("Sum (Python):", sum(revenues_row))  # native Python sum
print("Sum (Pandas):", revenues_row.sum())  # pandas sum

values = [40000, 44000, 48400, 53240, 58564, 58564, 58564, 58564]
print("Expected sum:", sum(values))  # Should be 449960

# Your actual values
raw = df.iloc[38, 2:10].tolist()
print("Raw Values:", raw)
print("Rounded:", [round(x) for x in raw])
print("Rounded Sum:", sum([round(x) for x in raw]))

df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="CapBudgWS", header=None)

# Print full "Operating Expenses" row (Revenues)
row_index = 38  # likely where Revenues is
row = df.iloc[row_index, :15]  # Print more columns
print("Row 38 (first 15 columns):", row.tolist())

print("Index map test:", [(i, row[i]) for i in range(len(row))])

revenues_row = df.iloc[38, 2:10]
print("Values:", revenues_row.tolist())
print("Sum:", sum(revenues_row))

revenues_row = df.iloc[38, 2:10]
numeric_values = pd.to_numeric(revenues_row, errors='coerce')
print("Raw values:", revenues_row.tolist())
print("After numeric cleaning:", numeric_values.tolist())
print("Length after cleaning:", len(numeric_values.dropna()))
print("Sum after cleaning:", numeric_values.sum())

values = [40000.0, 44000.0, 48400.0, 53240.0, 58564.0, 58564.0, 58564.0, 58564.0]
print("Manual sum:", sum(values))

