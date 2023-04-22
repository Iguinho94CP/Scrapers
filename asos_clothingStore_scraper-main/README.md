# API Scraper
This API scraper is a Python script that extracts data from an API provided by the fashion retailer ASOS. The script uses the Requests library to make HTTP requests to the API and retrieves the response in JSON format. The data is then processed and organized into a Pandas dataframe for further analysis.

The script extracts information about products listed on the ASOS website, including their name, brand, current price, previous price, product URL, and product image. It makes use of pagination to iterate through multiple pages of product listings and collects data from each page until all pages have been processed.

The extracted data can be used for various purposes, such as price tracking, product analysis, and data visualization. The data can also be exported to various formats, such as CSV or Excel, for further use.

## Dependencies
The following libraries are required to run this script:

- Requests
- Pandas

## How to use
Clone this repository to your local machine.
Install the dependencies by running pip install -r requirements.txt in your terminal.
Run the script using the command python api_scraper.py.
The script will output the extracted data in a Pandas dataframe and save it to a CSV file.
Note: Before running the script, make sure to update the cookies variable in the script with valid cookies from your ASOS account. This is required to access the API and retrieve the product data.

## License
This script is licensed under the MIT License. Feel free to use and modify it for your own purposes.
