
# StockFetch: Webpage for Extracting and Downloading Stock Data

**StockFetch** is a web application that allows users to download specific stock market data, including open price, close price, volume, low price, and high price, in CSV format for a given stock (from either the NYSE or NASDAQ). Users must enter a stock ticker, select a date range, and choose at least one parameter to retrieve the data. The CSV file will then be automatically downloaded to their computer.




![StockFetch](Images/Image%201.png)


## Getting An API Key

- **Sign Up for Alpha Vantage**: Go to [this link](https://www.alphavantage.co/support/#api-key) and sign up.
- **Obtain Your API Key**: After signing up, you'll receive an API key. Copy it to the `.env` file in your project.

## Running The App

1. Clone the `myapp` folder from the repository:
    ```bash
    git clone https://github.com/NicolasGarzon0/StockFetch.git
    ```

2. Navigate into the `myapp` directory:
    ```bash
    cd StockFetch/myapp
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Open the `.env` file in the `myapp` directory and add your API key:
    ```bash
    ALPHA_VANTAGE_API_KEY=your_api_key
    ```

5. Run the application:
    ```bash
    python app.py
    ```

6. Open your browser and go to `http://127.0.0.1:5000/` to use the application.

## Technologies Used

Python (Flask), HTML, CSS, JavaScript, Alpha Vantage API


