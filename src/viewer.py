

import numpy as np
import random 
import matplotlib
import matplotlib.pyplot as plt
# this will be the Agg backend, 
matplotlib.use('Agg')
import tempfile
import stock_data as sd
import calculations as c
import opto as opto
import os
import sys

# TODO: consider interaction with flask logging
import logging

# ----- viewer ----
# A simple flask app to drive some of the things in opto.py & calculations.py
# + log returns for universe of stocks
# + calculation of empirical covariance matrix for returns
# + plot eigen values of covariance
# + windowed covariance matrix over last couple years
# + plot ratio of 1st/2nd eigenvalue over time
# + determine hedge portfolio for one ticker from universe
 
# From root dir source setup.env, download data, then run python src/viewer.py

from flask import Flask,send_from_directory
app = Flask(__name__)

# TODO: mess with fonts
def header():
    return """<p style="font-family:Palatino Linotype; font-size:22pt">Kite & Rocket Research.<hr></p><br>"""

def footer():
    return """<br><hr><a href="/">return</a><br>"""

def i(desc,i):
    """add an (i)tem to our index page"""
    return "<a href=\"%s\">%s</a><br>"  %(i,desc)

def image(title,name):
   return "%s<br><img src=\"/generated/%s\" height=500 width=700>" % (title,name)

# use flask to serve back static/generated content
@app.route('/generated/<path:path>')
def send_generated(path):
    genroot = generated_dir()
    return send_from_directory(genroot, path)

# ----------- main page  -----------------------
@app.route("/")
def index():
    body = header() 
    body += i("welcome","hello")
    body += i("Eigenvalues of the 2016 empirical covariance","eigens")
    body += i("Ratio of 1/2nd eigen value month by month","eigens/m")
    body += i("Hedge QQQ","hedge/QQQ")
    body += i("Hedge FB","hedge/FB")
    body += "<br><br><hr>"
    return body

@app.route("/hello")
def hello():
    return header() + "<h2>Hello World!</h2>" + footer()

# you can hack the url and get a hedge for anything in the universe
@app.route("/hedge/<ticker>")
def hedge(ticker):
    body = header()
    # valid symbol?
    if not ticker in sd.universe():
        body += "invalid hedge symbol %s" % ticker
        return body + footer()
    # okay got a symbol we know
    body += "We hedge %s with <br>" % ticker 
    for n,w in opto.get_hedge(ticker):
        body += "<a href=\"/hedge/%s\">%s</a> %2.4f<br>" % (n,n,w)
        
    return body + footer()

# meat  TODO: seperate file?
@app.route('/eigens')
def plot_eigens():
    """ Simple plot of our covarinace matrix eigen values """
    w = c.get_eigens_2016()
    x = range(0,len(w))
    plt.clf()
    fig = plt.plot(x,w)
    tf = tempfile.TemporaryFile()
    plt.savefig(tf,format='png')
    header = {'Content-type': 'image/png'}
    tf.seek(0)
    data = tf.read()
    return data, 200, header


@app.route('/eigens/m')
def plot_monthly_eigen_ratio():
    """ for every 30 days, what's the ratio of the first to second eigen value"""
    vals = c.get_monthly_eigen_ratio()
    # unzip tuple [(a,b)...] --> [[a,a,a,a,a];[b,b,b,b] with zip *
    ratios = zip(*vals)[1] 
    x = range(0,len(vals))

    # the plot is holding some global state, so "new" plots remember the old unless you clear the figure 
    plt.clf()

    # make room for label at bottom
    # see: http://stackoverflow.com/questions/6774086/why-is-my-xlabel-cut-off-in-my-matplotlib-plot
    #   plt.gca().tight_layout()
    plt.gcf().subplots_adjust(bottom=0.25)
    fig  = plt.plot(x,ratios)

    # add these dates as labels
    xlabels = zip(*vals)[0] 
    plt.xticks(x, xlabels, rotation='vertical')
    plt.xlabel("date")
    plt.ylabel("ratio")
    plt.title("ratio of 1st eigenvalue to 2nd eigenvalue")

    # we write the file to the full_path, give the name in HTML as /generated/<imagename>.png and flask knows how to find /generated at the fullpath
    fname = "em" + str(random.randint(20000,40000)) + ".png"
    full_path = generated_dir() + fname
    with open(full_path, "wb") as ifile:
        plt.savefig(ifile, format="png")

    return header() + image("monthly eigenvalue ratios",fname) + footer() 

def generated_dir():
    """ path to generated dir, dynamic images go here """
    # need KNR_ROOT env
    root = ""
    try:
        root = os.environ['KNR_ROOT']
    except:
        logging.warn("missing KNR_ROOT env variable. source setup.env?")
        sys.exit()

    return root + "/generated/"

def make_generated_dir():
    """ if we generate files for serving put them in KNR_ROOT/generated """

    # need KNR_ROOT env
    root = ""
    try:
        root = os.environ['KNR_ROOT']
    except:
        logging.warn("missing KNR_ROOT env variable. source setup.env?")
        sys.exit()

    # make dir if it doesn't exist
    full_path = root + "/generated"
    try:
        os.stat(full_path)
    except:
        os.mkdir(full_path)


# host 0.0.0.0 will make the server externally visibile, listen on all public IPs
# deubg - reload src on edit
if __name__ == "__main__":
    make_generated_dir()
    app.run(debug=True,host='0.0.0.0',port=5000)


