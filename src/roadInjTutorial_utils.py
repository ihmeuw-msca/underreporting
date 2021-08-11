import numpy as np
import pickle
from regmod.data import Data

def logit(p):
    return np.log(p/(1-p))

def expit(x):
    return np.exp(x)/(1+np.exp(x))


###################################
# Functions for generating        #
# synthetic data for p and lambda #
###################################
def pFunGenerator(noise=lambda size: np.zeros(size)):
    """
    Returns a function that takes processed_data and returns
      expit(-3*(seatBeltUse-1) - 1 + noise(size=n))
    where noise is a function and n is the number of observations
    """
    def pGen(processed_data):
        noiseObs = noise(size=len(processed_data))
        f = -3*(processed_data.seatbeltUse_synthetic-1) - 1 + noiseObs
        return expit(f)
        
    return pGen


def lamFunGenerator(noise=lambda size: np.zeros(size)):
    """
    Returns a function that takes processed_data and returns a lambda estimate for each row,
    of the form
       spline(age) + sex + offset + noise(size=n)
    where noise is a function and n is the number of observations
    Note, this returns an estimate of the RATE OF TOTAL INJURIES, ie it's in units of 
    'injuries/year,' not 'injuries per person per year'
    """
    def lamGen(processed_data):
        """
        processed_data must have columns age, sex, and (Intercept)
        """
        with open('roadInj_lamModel.pickle', 'rb') as f:
            # Load the lambda model that we saved earlier
            modelLam, resultLam = pickle.load(f)
        # Use that model to generate synthetic lambda for processed_data
        pd_dat = Data(col_covs=["age", "sex", "(Intercept)"], df=processed_data)
        
        logLam = modelLam.params[0].get_mat(pd_dat) @ resultLam['coefs']
        
        f = logLam + noise(size=len(processed_data))
        return np.exp(f)*processed_data.sample_size
    
    return lamGen



