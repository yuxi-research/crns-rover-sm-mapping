#%% LCCC
import numpy as np


#%%  Calculate correlation coefficient
def calc_corr(obs, pred):
    obs, pred = zip(*[[o, p] for o, p in zip(obs, pred) if ~np.isnan(o) & ~np.isnan(p)])
    corr = np.corrcoef(pred, obs)[0, 1]
    return corr


#%% Lin's concordance correlation coefficient
def calc_lccc(obs, pred):
    '''
    Calculate Lin's concordance correlation coefficient (LCCC) between observed and predicted values.
    NaN values are allowed in the input arrays, and they will be ignored in the calculation.
    Parameters:
    obs : array-like
        Observed values.
    pred : array-like
        Predicted values.
    Returns:
    lccc : float
        The calculated LCCC value.
    '''
    # Remove NaNs
    obs, pred = zip(*[[o, p] for o, p in zip(obs, pred) if ~np.isnan(o) & ~np.isnan(p)])
    if len(pred) == 0:
        return np.nan
    obs_mean = np.nanmean(obs)
    pred_mean = np.nanmean(pred)
    s_xy = np.nansum((obs - obs_mean) * (pred - pred_mean))
    s_xx = np.nansum((obs - obs_mean) ** 2)
    s_yy = np.nansum((pred - pred_mean) ** 2)
    lccc = 2 * s_xy / (s_xx + s_yy + (obs_mean - pred_mean) ** 2)
    return lccc


def calc_metrics(obs, pred):
    '''
    Calculate RMSE, LCCC, correlation coefficient, R2, and count of valid observations between observed and predicted values.
    NaN values are allowed in the input arrays, and they will be ignored in the calculation.
    Parameters:
    obs : array-like
        Observed values.
    pred : array-like
        Predicted values.
    Returns:
    metrics : dict
        A dictionary containing the calculated metrics:
        - 'RMSE': Root Mean Square Error
        - 'LCCC': Lin's Concordance Correlation Coefficient
        - 'corr': Pearson correlation coefficient
        - 'bias': Mean bias (mean of predicted - observed)
        - 'mean': Mean of observed values
        - 'ubRMSE': Unbiased Root Mean Square Error
        - 'Sample size': Count of valid observations used in the calculations
    '''
    # Remove NaNs
    obs, pred = zip(*[[o, p] for o, p in zip(obs, pred) if ~np.isnan(o) & ~np.isnan(p)])
    if len(obs) == 0:
        return {'RMSE': np.nan, 'LCCC': np.nan, 'corr': np.nan, 'bias': np.nan, 'mean': np.nan, 'ubRMSE': np.nan, 'Sample size': 0}

    obs = np.array(obs)
    pred = np.array(pred)
    rmse = np.sqrt(np.mean((pred - obs) ** 2))
    corr = np.corrcoef(pred, obs)[0, 1]
    lccc = calc_lccc(obs, pred)
    bias = np.mean(pred - obs)
    mean = np.mean(obs)
    ubRMSE = np.sqrt(np.mean((pred - obs - bias) ** 2))
    count = len(pred)

    return {'RMSE': rmse, 'LCCC': lccc, 'corr': corr, 'bias': bias, 'mean': mean, 'ubRMSE': ubRMSE, 'Sample size': count}

