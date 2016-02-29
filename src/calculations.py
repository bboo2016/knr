
import logging
import stock_data as sd
import pandas as pd
import numpy as np
import datetime as dt
import sys

# --- calculations ----
# some simple stock calculations
#   - log retunrs
#   - covariance
#   - eignevalues

def get_data(ticker):
    """ given a symbol, return a dataframe of the downloaded yahoo data """
    full_path = sd.dataroot() + "/" + ticker + ".csv"
    df = pd.DataFrame()
    try:
        df = pd.read_csv(full_path)
    except IOError as e:
        logging.warn(e)
        logging.warn("missing data,run python src/stock_data.py?")
        sys.exit(-1)

    df['Ticker'] = ticker
    return df

# TODO: this makes no effort to ensure we have the same number of returns from all tickers, 
# possible solution require len(r) always = the first series
def get_returns(tickers,sdate,edate):
    """ for tickers, in date range (inclusive) pull into a single de-meaned log return dataframe """
    df = pd.DataFrame()

    for n in tickers:
        logging.info("Generating returns for ticker %s for %s to %s " % (n,sdate,edate))
        r = get_data(n)
        r['Return'] = np.log(r['Adj Close'] / r['Adj Close'].shift(-1))
        r['Return'] = r['Return'].sub(r['Return'].mean())
        r = r.loc[r['Date']>=sdate]
        r = r.loc[r['Date']<=edate]
        logging.info("Generating returns for %s shape %d by %d" % (n,r.shape[0],r.shape[1]))
        df[n] = r['Return']

    return df

def make_empirical_covariance(rets):
    """ for given returns , return empirical covariance matrix """ 
    rets = rets.as_matrix()
    cov = rets.T.dot(rets)
    # cov = rets.corr()
    return cov

# dedicated functions for full year 2016
def get_returns_2016(tickers):
    return get_returns(tickers,"2015-01-01","2016-01-1")

def make_covariance_2016():
    rets = get_returns_2016(sd.universe())
    return make_empirical_covariance(rets)

def get_eigens_2016():
    """ for our empirical covariance matirx, return the eigenvalues """
    c = make_covariance_2016()
    w,v = np.linalg.eig(c)
    return w

def get_eigens(cov):
    """ given covariance, return eigen values """
    w,v = np.linalg.eig(cov)
    return w
    
def get_eigen_ratio(cov):
    """ ratio of 1st and 2nd eigen values """
    w = get_eigens(cov)
    return w[0] / w[1]
 
def get_monthly_eigen_ratio():
    """ for every 30 days, what is the ratio of the first to the second eigen value """

    # make the dates
    n = dt.datetime.now()
    step = dt.timedelta(days=30)
    dates = []
    for i in range(0,36):
        n = n - step
        dates.append(n.strftime("%Y-%m-%d"))
  
    # grab returns, calc cov, calc eigens, take ratio, return date-eigen ratio pairs  
    ratios = [] 
    for j in range(len(dates)-1):
        sdate = dates[j+1]
        edate = dates[j]
        cov = make_empirical_covariance(get_returns(sd.universe(),sdate,edate))
        r = get_eigen_ratio(cov)
        logging.info("%s - %s [%4.2f]" % (sdate,edate,r))
        ratios.append((sdate,r))

    return ratios 

# ----------------------------------------- tests -------------------------------------- 
def test_dates():
    n = dt.datetime.now()
    step = dt.timedelta(days=30)
    dates = []
    for i in range(0,30):
        n = n - step
        dates.append(n.strftime("%Y-%m-%d"))
    print(dates)
 
def test():
    logging.info("eigens %s" % get_eigens_2016())
    logging.info("eratio %s" % get_monthly_eigen_ratio())

# poor man's testing
if __name__ == '__main__':
    logging.info("ok")
    test_dates()
    test()
    logging.info("done")

