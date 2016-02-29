from cvxpy import *
import numpy as np
import cvxopt
from multiprocessing import Pool

import calculations as c
import stock_data as sd
import logging

# --- opto---- 
# Uses cvxpy + the returns downloaded to generate a convex optimization problem
# of creating a hedge portfolio for the given ticker
#
# NB: these are all dense matricies, if you want to do 
# this "for real" consider scipy.sparse and SCS (via cvxpy)

def get_hedge(hedge_ticker): 
    """ Returns a hedge portfolio """
    #  We are going to match the returns of hedge_ticker 
    #  with a weighted combination of the rest of the universe

    sdate = "2015-01-01"
    edate = "2016-01-01"

    # hedge symbols returns
    b = c.get_returns([hedge_ticker],sdate,edate)
    b = cvxopt.matrix(b.as_matrix())

    n = b.size[0]

    # rest of returns, remove hedge we can't hedge with ourself.
    # leave hedge in, see it assign all the hedge to itself
    names = sd.universe()
    names.remove(hedge_ticker)
    A = c.get_returns(names,sdate,edate)
    A = cvxopt.matrix(A.as_matrix())

    m = A.size[1] 

    # check dimensions
    logging.info("bsize: %d %d " % b.size)
    logging.info("Asize: %d %d " % A.size)

    gamma = Parameter(sign="positive")

    # Construct the problem.
    # A is a matrix of hedge returns
    #
    # x is a set of weights against the other names, 
    # the l1 norm penalty pushes 
    #
    # Ax - b  is minimized when the difference between the weighted returns and qqq returns are small
    #
    # for ease of interpretation, let's make the weights sum to 1
    x = Variable(m)
    objective = Minimize(sum_squares(A*x - b) + gamma*norm(x, 1))
    constraints = [sum_entries(x) == 1, x>=0]
    p = Problem(objective,constraints)

    # Turning off sparsity term for the moment
    gamma.value =  0
    result = p.solve()
    for n,w in zip(names,x.value):
        logging.info("%s weight: %2.4f" % (n,w))
    logging.info("total: %s" % sum(x.value))
    logging.info("objective: %.5f" % objective.value)

    # sparsity term would encourage x coefs to be zero
    #gammas = np.linspace(0, 1, num=10)
    #logging.info(gammas)
    #for gamma_value in gammas:
    #    logging.info("gamma: %s" % gamma_value)
    #    gamma.value = gamma_value
    #    result = p.solve()
    #    logging.info(x.value)
    #    logging.info(np.linalg.norm(x.value))

    # return [(name, hedge weight),(name ...
    return zip(names,x.value)


# we test, therefore we exist....
def test():
    return get_hedge("QQQ")

def test_another():
    return get_hedge("FB")

if __name__ == '__main__':
    logging.info("ok")
    logging.info(test())
    logging.info(test_another())
    logging.info("done.")
