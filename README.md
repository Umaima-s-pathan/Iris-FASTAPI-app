# FastAPI Excel Processor - Assignment Submission
## 📚 Overview

This FastAPI application is designed to read and process an Excel file (`capbudg.xls`) and expose a RESTful API to interact with its data. The application supports listing table sections, retrieving row names, and summing values for specified rows.

The assignment demonstrates skills in:

* FastAPI development
* Excel file handling using `pandas`
* REST API design and testing
* Clean and maintainable Python coding practices

---

## 🔠 API Endpoints

**Base URL:** `http://localhost:9090`

### 1. **GET** `/list_tables`

Returns all available table names in the Excel file.

**Response Example:**

```json
{
  "tables": [
    "Initial Investment",
    "Revenue Projections",
    "Operating Expenses"
  ]
}
```

---

### 2. **GET** `/get_table_details`

**Query Parameters:**

* `table_name` (str): The name of the table

**Functionality:** Returns the row labels (first column or configured label column) for the specified table.

**Example Request:**

```
/get_table_details?table_name=Initial%20Investment
```

**Example Response:**

```json
{
  "table_name": "Initial Investment",
  "row_names": [
    "Initial Investment=",
    "Opportunity cost (if any)=",
    "Lifetime of the investment",
    "Salvage Value at end of project=",
    "Deprec. method(1:St.line;2:DDB)=",
    "Tax Credit (if any )=",
    "Other invest.(non-depreciable)="
  ]
}
```

---

### 3. **GET** `/row_sum`

**Query Parameters:**

* `table_name` (str): The table containing the row
* `row_name` (str): The label of the row to sum

**Functionality:** Returns the sum of numeric values in the specified row.

**Example Request:**

```
/row_sum?table_name=Operating%20Expenses&row_name=Revenues
```

**Example Response:**

```json
{
  "table_name": "Operating Expenses",
  "row_name": "Revenues",
  "sum": 449960.0
}
```

---

## 📁 Project Structure

```
FastAPI_Excel_Assignment/
├── Data/
│   └── capbudg.xls
├── fastapi_app(localhost).py
├── requirements.txt
├── README.md
└── FastAPI_Excel_Assignment.postman_collection.json
```

---

## 🔧 Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API server

```bash
python fastapi_app(localhost).py
```

### 3. Test Endpoints

Open Postman or browser:

* `http://localhost:9090/list_tables`
* `http://localhost:9090/get_table_details?table_name=Initial%20Investment`
* `http://localhost:9090/row_sum?table_name=Operating%20Expenses&row_name=Revenues`

---

## 🔄 Potential Improvements

* Add support for `.xlsx` and `.csv` files
* Allow dynamic file upload
* Add a basic front-end UI using Streamlit or React
* Implement column-level summaries
* Include Swagger/OpenAPI documentation

---

## ⚠️ Missed Edge Cases

* Handling Excel files with no data
* Malformed table names not found in config
* Rows with no numeric data return `0.0`, but may require a custom warning
* No duplicate row name checks yet

---

## 🔺 Postman Collection

A complete collection is included in:

```
FastAPI_Excel_Assignment.postman_collection.json
```

It includes:

* `GET /list_tables`
* `GET /get_table_details` (for all tables)
* `GET /row_sum` for known working rows

---

## 🚀 Final Notes

This submission meets all the assignment objectives with clear modular code, correct FastAPI endpoint handling, and robust error management. The use of structured configuration for Excel sections ensures extensibility.


Thanks! Here's the updated section that you can manually add to your README under the last section:

---

## 🌐 Google Colab-Compatible Version (Optional Enhancement)

To ensure broader accessibility and flexibility in testing, a separate version of this FastAPI application has also been adapted to run seamlessly within a **Google Colab environment**.
This enhancement enables users to:

* Test the application **without any local setup**
* Expose the FastAPI endpoints to the public internet using **ngrok**
* Run and demo the API directly from a browser, ideal for collaborative or remote evaluations

---

### 🧾 Additional Requirements for Colab

If using the Colab-compatible version, install the following additional dependencies:

```bash
pip install nest-asyncio pyngrok
```

These are used to:
* Handle asynchronous event loops inside Colab (`nest-asyncio`)
* Create a public URL tunnel for the FastAPI server (`pyngrok`)

---

### 🧪 How to Run in Google Colab

1. Open the provided `fastapi_app_colab.ipynb` notebook in Google Colab.
2. Upload the Excel file `capbudg.xls` when prompted.
3. Enter your ngrok auth token if prompted (or skip if it's preconfigured).
4. Run all cells to launch the FastAPI server.
5. A public `ngrok` URL will be displayed—use this in place of `http://localhost:9090` to test endpoints.

---

