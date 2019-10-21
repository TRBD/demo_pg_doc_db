"""
Additional functions for enriching history data with additional metric columns
"""
from demo_importlib import np, sp, pd


def basic_delta(s, k, sigma, t=1./4, r=.02, q=0.):
    """
    Calculate european call black scholes delta, no divs
    :param s: spot price
    :param k: strike
    :param sigma: implied vol
    :param t: time to exp
    :param r: interest
    :param q: div
    :return: delta float value array
    """
    return np.exp(-q*t) * sp.stats.norm.cdf(basic_d1(s, k, sigma, t, r, q))


def basic_d1(s, k, sigma, t=1./4, r=.02, q=0.):
    """
    Calculate european black scholes d1 value
    :param s: spot price
    :param k: strike
    :param sigma: implied vol
    :param t: time to exp
    :param r: interest
    :param q: div
    :return: d1 float value array
    """
    return (np.log(1.*s/k) + (r-q+(sigma**2)/2.)*t) / (sigma * np.sqrt(t))


def add_calc_pnl_history(contract_history_frame, target_contract_row):
    """
    Add arbitrary metric to contract_history frame that has already been stored
    :param contract_history_frame: DataFrame
    :param target_contract_row: TargetContractRow
    :return: contract_history_frame
    """
    k = target_contract_row.strike
    exp = pd.Timestamp(target_contract_row.expiration_date).tz_localize('UTC')
    ttes = contract_history_frame.quote_date.apply(lambda d: (len(pd.bdate_range(d, exp))-1 + .01) / 252.)
    spots = contract_history_frame.underlyer_price
    vols = contract_history_frame.implied_vol
    contract_history_frame['calc_delta'] = basic_delta(spots, k, vols, t=ttes)
    return contract_history_frame
