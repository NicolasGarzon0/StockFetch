function sendData() {
    // Get the value of the stock ticker input
    const ticker = document.getElementById('stockTicker').value;

    // Get the value of the start date and end date to search for
    let startdate = document.getElementById('startDate').value;
    let enddate = document.getElementById('endDate').value;

    // Check if the dates are empty and set to "empty"
    if (startdate === "") {
        startdate = "empty"; // If start date is not provided, set it as "empty"
    }
    if (enddate === "") {
        enddate = "empty"; // If end date is not provided, set it as "empty"
    }

    // Get checkbox values as booleans (whether they are checked or not)
    const openPrice = document.getElementById('openPrice').checked;
    const highPrice = document.getElementById('highPrice').checked;
    const lowPrice = document.getElementById('lowPrice').checked;
    const closePrice = document.getElementById('closePrice').checked;
    const volume = document.getElementById('volume').checked;

    // Validate if at least one checkbox is selected
    if (!openPrice && !highPrice && !lowPrice && !closePrice && !volume) {
        alert("Please select at least one type of data to retrieve.");
        return; // Stop execution if no checkboxes are selected
    }
    
    // Validate if all required fields are filled (ticker, start date, and end date)
    if (!ticker || startdate === "empty" || enddate === "empty") {
        alert("Please provide a stock ticker and both start and end dates.");
        return; // Stop execution if validation fails
    }

    // Construct the data object with all form inputs
    const data = {
        Ticker: ticker.toUpperCase(), // Convert ticker to uppercase for consistency
        Start_Date: startdate,
        End_Date: enddate,
        Open_Price: openPrice.toString().charAt(0).toUpperCase() + openPrice.toString().slice(1).toLowerCase(), // Capitalize first letter
        High_Price: highPrice.toString().charAt(0).toUpperCase() + highPrice.toString().slice(1).toLowerCase(),
        Low_Price: lowPrice.toString().charAt(0).toUpperCase() + lowPrice.toString().slice(1).toLowerCase(),
        Close_Price: closePrice.toString().charAt(0).toUpperCase() + closePrice.toString().slice(1).toLowerCase(),
        Volume: volume.toString().charAt(0).toUpperCase() + volume.toString().slice(1).toLowerCase() 
    };

    // Send data using fetch API (POST request)
    fetch('/submit', {
        method: 'POST', // Define the request method
        headers: {
            'Content-Type': 'application/json' // Set the content type to JSON
        },
        body: JSON.stringify(data) // Convert the data object to a JSON string
    })
    .then(response => {
        // Check if the response is a file (successfully fetched data)
        if (response.ok) {
            // Convert the response to a Blob (binary data) for file download
            return response.blob();
        }
        throw new Error("Error fetching data"); // Throw an error if the response is not OK
    })
    .then(blob => {
        // Create a link element to simulate file download
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob); // Create an object URL for the blob data
        link.download = data.Ticker + '_Data.csv'; // Set the download file name based on ticker
        link.click(); // Simulate a click to trigger the download
        document.getElementById('stockForm').reset(); // Reset the form after download
    })
    .catch((error) => {
        // Catch any errors during the fetch request
        console.error('Error:', error); // Log the error to the console
        alert('Error: ' + error.message); // Show an alert with the error message
        document.getElementById('stockForm').reset(); // Reset the form if there was an error
    });
}

// Event listener to enable/disable the button based on form input
document.getElementById('stockForm').addEventListener('input', function() {
    // Get the value of the ticker, start date, and end date input fields
    const ticker = document.getElementById('stockTicker').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const submitBtn = document.getElementById('submitBtn'); // Get the submit button

    // Get checkbox values as booleans inside the event listener
    const openPrice = document.getElementById('openPrice').checked;
    const highPrice = document.getElementById('highPrice').checked;
    const lowPrice = document.getElementById('lowPrice').checked;
    const closePrice = document.getElementById('closePrice').checked;
    const volume = document.getElementById('volume').checked;

    // Check if at least one checkbox is selected
    const checkboxes = openPrice || highPrice || lowPrice || closePrice || volume;
    
    // Enable the submit button only if all required fields are filled
    if (ticker && startDate && endDate && checkboxes) {
        submitBtn.disabled = false; // Enable the button if all fields are filled
    } else {
        submitBtn.disabled = true; // Disable the button if any required field is missing
    }
});



