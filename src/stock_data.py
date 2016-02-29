
import requests
import os
import sys
import logging

# -- stock_data ----
# Feb 2016
# Grab OHLC prices from Yahoo

# root logger everywhere please ...
logging.getLogger().setLevel(logging.INFO)

# stocks we care about
# TODO: dropped KHC, short history
def universe():
    return ["QQQ","MSFT","AMZN","FB","GOOG","GOOGL","CMCSA","INTC","CSCO","GILD","AMGN","SBUX","WBA"]

def make_url(ticker):
    base = "http://ichart.finance.yahoo.com/table.csv?s="
    return base + ticker 

def dataroot():
    try: 
        root = os.environ['KNR_ROOT']
    except:
        logging.warn("missing KNR_ROOT env variable. source setup.env?")
        sys.exit()

    return root + "/data/closes/"

def make_filename(ticker):
    """ Return full path with filename for a given symbol """
    full_path = dataroot() 

    # make dir if it doesn't exist
    # TODO: we make data/closes if data exists. handle data not existing
    try:
        os.stat(full_path)
    except:
        os.mkdir(full_path)

    return full_path + "/" + ticker + ".csv"

def download_close_history(ticker):
    """ For given ticker, pull all available OHLC data.  Save as csv """
    try:
        r = requests.get(make_url(ticker))
        outfile = open(make_filename(ticker),"w")
        outfile.write(r.text)
        outfile.close()
        logging.info("Pulled and saved. http status %s,ticker %s",r.status_code,ticker)
    except requests.exceptions.RequestException as e:
        # TODO: ConnectionError vs. HTTPError vs. Timeout
        logging.warn(e)
        sys.exit()

def download_all_history():
    """ Pull data for entire universe """
    for n in universe():
        download_close_history(n)

# poor man's testing
def test():
    logging.info(dataroot())
    download_close_history("AAPL")
 
if __name__ == '__main__':
    logging.info("ok")
    download_all_history()
    logging.info("done")

