

Kite & Rocket Research, Inc.
============================

Feb 2016

INSTALL
=======
On an AWS Amzn AMI t2.large

sudo yum -y install gcc
sudo yum -y install gcc48-c++.x86_64
sudo yum -y install git
sudo pip install pandas
sudo pip install flask
sudo yum -y install libpng-devel.x86_64
sudo yum -y install freetype-devel.x86_64
sudo pip install matplotlib

// for cvxpy
sudo yum -y install blas64-devel.x86_64
sudo yum -y install atlas-devel.x86_64
sudo yum -y install lapack-devel.x86_64
sudo pip install cvxpy

RUN
===
. setup.env
python src/stock_data.py
python src/viewer.py


WHAT
====
stock_data.py  - download yahoo OHLC data to data/closes
calculations.py - some calcs on that data
viewer.py - flask web server, front end to calculations. charts.

Resources
=========

on requests
http://docs.python-requests.org/en/master/
http://stackoverflow.com/questions/12433076/download-history-stock-prices-automatically-from-yahoo-finance-in-python

on flask
http://flask.pocoo.org/

on matplotlib
http://matplotlib.org/faq/howto_faq.html
http://matplotlib.org/examples/ticks_and_spines/ticklabels_demo_rotation.html
http://matplotlib.org/users/pyplot_tutorial.html
http://stackoverflow.com/questions/8213522/matplotlib-clearing-a-plot-when-to-use-cla-clf-or-close

on cvxpy/convex optimization
https://github.com/cvxgrp/cvxpy
http://stanford.edu/~boyd/cvxbook/
https://web.stanford.edu/~boyd/papers/scs.html


Github
======
https://github.com/bboo2016/knr


