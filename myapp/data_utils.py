# Import necessary libraries
import requests  
import pandas as pd  
import pandas_market_calendars as mcal  
import os  
from dotenv import load_dotenv, find_dotenv 

# Load the .env file containing the API key
dotenv_path = find_dotenv()  

# Check if the .env file is found, otherwise raise an error
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found. Please ensure it's present in the project directory.")

# Retrieve the API key from environment variables
Apikey = os.getenv("APIKEY")

# If the API key is not found, raise an error
if not Apikey:
    raise ValueError("APIKEY Not Found In Environment Variables.")

# Function to fetch stock data for a given ticker and save it as a CSV file
def Get_Stock(ticker):
    global Ticker
    Ticker = ticker  # Store the stock ticker symbol in a global variable.
    global file_name
    # Set the file path for the stock data CSV file.
    file_name = os.path.join(os.getcwd(), f"{ticker}_Stock_data.csv")
    
    # Construct the API URL for fetching stock data from Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Ticker}&outputsize=full&apikey={Apikey}&datatype=csv'

    try:
        # Send the GET request to fetch the stock data as a CSV
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx).

        # Save the fetched content to the specified CSV file
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name  # Return the file name of the saved CSV.

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None  # If an error occurs, return None.

# Function to process the stock data CSV file and filter by user-specified date range and price/volume options
def Get_Stock_CSV(file_name, SDate, EDate, Open_Price, High_Price, Low_Price, Close_Price, Volume):
    df = pd.read_csv(file_name)  # Read the stock data CSV into a DataFrame.
    df.columns = df.columns.str.strip()  # Strip any extra spaces from the column names.
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Convert the timestamp column to datetime.
    df['close'] = pd.to_numeric(df['close'], errors='coerce')  # Ensure 'close' column is numeric.

    # Get the valid trading days for the NYSE between the specified start and end dates
    nyse = mcal.get_calendar('NYSE')
    early = nyse.valid_days(start_date=SDate, end_date=EDate)
    dfe = pd.DataFrame(early)

    # Initialize a dictionary to store the final processed data
    FinalData = {'Open Price': [], 'High Price': [], 'Low Price': [], 'Close Price': [], 'Volume': [], 'Date': []}

    x = 0
    y = len(dfe.index) - 1
    date = ''

    # Iterate through the valid trading days
    while x <= y:
        date = str(dfe[0][x].date())  # Get the current date from the valid trading days DataFrame.
        
        # Check if this date exists in the stock data
        if (df['timestamp'] == date).any():  
            rslt_df = df.loc[df['timestamp'] == pd.to_datetime(date)]  # Extract rows for this date.

            # Retrieve the stock data for the day
            close_price = rslt_df['close'].iloc[0]
            open_price = rslt_df['open'].iloc[0]
            high_price = rslt_df['high'].iloc[0]
            low_price = rslt_df['low'].iloc[0]
            volume = rslt_df['volume'].iloc[0]

            # Append data to FinalData dictionary based on user selections
            FinalData['Date'].append(date)

            if Open_Price:
                FinalData['Open Price'].append(open_price)
            else:
                FinalData['Open Price'].append(None)

            if High_Price:
                FinalData['High Price'].append(high_price)
            else:
                FinalData['High Price'].append(None)

            if Low_Price:
                FinalData['Low Price'].append(low_price)
            else:
                FinalData['Low Price'].append(None)

            if Close_Price:
                FinalData['Close Price'].append(close_price)
            else:
                FinalData['Close Price'].append(None)

            if Volume:
                FinalData['Volume'].append(volume)
            else:
                FinalData['Volume'].append(None)

            x += 1
        else:
            x += 1  # Move to the next day if no data exists for the current day.

    # Convert the processed data to a DataFrame
    dfa = pd.DataFrame(FinalData)
    dfa = dfa.dropna(axis=1, how='all')  # Drop columns that have all null values.

    # Get the directory of the original file
    file_dir = os.path.dirname(file_name)

    # Construct the processed file path in the same directory
    final_file_name = os.path.join(file_dir + '/myapp', f'{os.path.splitext(os.path.basename(file_name))[0]}_Processed.csv')

    # Save the processed data to a new CSV file
    dfa.to_csv(final_file_name, index=False)   
    os.remove(file_name)  # Delete the original CSV file after processing.
    return final_file_name

# Function to verify if the stock ticker is valid
def Verify_Stock(ticker):
    Ticker = ticker.upper()  # Convert the ticker symbol to uppercase.

    # Ensure that the ticker doesn't contain any dots (used for other stock exchanges).
    if Ticker.find(".") != -1:
        return False

    # Construct the API URL to search for the stock symbol in Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={Ticker}&apikey={Apikey}'

    try:
        # Send the GET request to search for the stock symbol
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx).
        data = response.json()  # Parse the JSON response.

        # Check if there are matching results for the ticker
        if "bestMatches" in data and data["bestMatches"]:
            first_result = data["bestMatches"][0]["1. symbol"]
            region = data["bestMatches"][0]["4. region"]

            # Return True if the ticker matches the first result and the ticker region is United States
            if Ticker == str(first_result) and "United States" == str(region):
                return True
            else:
                return False  # Ticker doesn't match the first result.
        else:
            print("No matching results found.")
            return False  # No matches found.

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False  # If an error occurs during the request, return False.
