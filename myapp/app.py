# Import necessary libraries and modules
from flask import Flask, request, jsonify, render_template, send_file
from data_utils import Get_Stock, Get_Stock_CSV, Verify_Stock
import os

# Initialize the Flask web application
app = Flask(__name__)

# Route for the home page (index.html) to render the initial interface
@app.route('/')
def index():
    return render_template('index.html')  # Render the 'index.html' template when the root URL is accessed.

# Route for handling the POST request when stock data is requested
@app.route('/submit', methods=['POST'])
def handle_post():
    # Extract JSON data from the request body
    data = request.get_json()

    # If no data is provided, return an error response
    if not data:
        return jsonify({"error": "No Data Provided"}), 400  # 400: Bad request error.

    # Verify if the stock ticker is valid
    if not Verify_Stock(data["Ticker"]):
        return jsonify({"error": "Invalid or Unsupported Stock Ticker"}), 400

    # Fetch the stock data using Get_Stock
    file_name = Get_Stock(data["Ticker"])
    if not file_name:
        return jsonify({"error": "Failed to Fetch Stock Data"}), 503  # Service Unavailable

    # Generate the CSV file with selected data
    try:
        Get_Stock_CSV(
            file_name=file_name,
            SDate=data["Start_Date"],
            EDate=data["End_Date"],
            Open_Price=data["Open_Price"] == "True",
            High_Price=data["High_Price"] == "True",
            Low_Price=data["Low_Price"] == "True",
            Close_Price=data["Close_Price"] == "True",
            Volume=data["Volume"] == "True",
        )

        # Path to the processed CSV file
        file_path = os.path.join(app.root_path, f'{data["Ticker"]}_Stock_data_Processed.csv')

        # Check if the file was created successfully
        if not os.path.exists(file_path):
            return jsonify({"error": "Failed to Generate CSV File"}), 500  # Internal Server Error

        # Send the file as a download response
        return send_file(file_path, as_attachment=True, download_name=f"{data['Ticker']}_Data.csv")

    finally:
        # Clean up: Delete the file after sending it
        if os.path.exists(file_path):
            os.remove(file_path)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
