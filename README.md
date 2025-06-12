# FastAPI Excel Processor - Assignment Submission

📚 Overview

This FastAPI application is designed to read and process an Excel file (capbudg.xls) and expose a RESTful API to interact with its data. The application supports listing table sections, retrieving row names, and summing values for specified rows.

The assignment demonstrates skills in:

FastAPI development

Excel file handling using pandas

REST API design and testing

Clean and maintainable Python coding practices

🔠 API Endpoints

Base URL: http://localhost:9090

1. GET /list_tables

Returns all available table names in the Excel file.

Response Example:
