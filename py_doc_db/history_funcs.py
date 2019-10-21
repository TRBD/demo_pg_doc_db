"""
Functions for enriching history data with additional metric columns
"""

def gamma_pnl(contract_history_frame):
    """
    Pnl Derived from Gamma
    :param contract_history_frame: DataFrame
    :return: pd.Series
    """
    return (
        (.5*(
            contract_history_frame.gamma + contract_history_frame.gamma.shift(-1))
         ).shift(1) * .5 * (contract_history_frame.underlyer_price.diff() ** 2))


def theta_pnl(contract_history_frame):
    """
    Pnl Derived from Theta
    :param contract_history_frame: DataFrame
    :return: pd.Series
    """
    return contract_history_frame.theta.shift(1)

def vega_pnl(contract_history_frame):
    """
    Pnl Derived from Vega
    :param contract_history_frame: DataFrame
    :return: pd.Series
    """
    tmp = contract_history_frame.vega.shift(1) * contract_history_frame.implied_vol.diff() * 100
    return tmp


def delta_hedge_pnl(contract_history_frame):
    """
    Pnl Derived from Hedging contract delta
    :param contract_history_frame: DataFrame
    :return: pd.Series
    """
    return -contract_history_frame.delta.shift(1) * contract_history_frame.underlyer_price.diff()


def mark_pnl(contract_history_frame):
    """
    Mark-to-market pnl on contract
    :param contract_history_frame: DataFrame
    :return: pd.Series
    """
    mids = .5*(contract_history_frame.bid + contract_history_frame.ask)
    return mids.diff()


def add_pnl_history(contract_history_frame):
    """
    Add columns to enrich contract history frame
    :param contract_history_frame: DataFrame
    :param target_contract_row: TargetContractRow
    :return: pd.DataFrame
    """
    contract_history_frame['vega_pnl'] = vega_pnl(contract_history_frame)
    contract_history_frame['gamma_pnl'] = gamma_pnl(contract_history_frame)
    contract_history_frame['theta_pnl'] = theta_pnl(contract_history_frame)
    contract_history_frame['greek_pnl'] = contract_history_frame.vega_pnl + contract_history_frame.gamma_pnl + \
                                          contract_history_frame.theta_pnl
    contract_history_frame['delta_hedge_pnl'] = delta_hedge_pnl(contract_history_frame)
    contract_history_frame['mark_pnl'] = mark_pnl(contract_history_frame)
    contract_history_frame['hedged_mark_pnl'] = contract_history_frame.delta_hedge_pnl + \
                                                contract_history_frame.mark_pnl
    contract_history_frame['unexplained_pnl'] = contract_history_frame.hedged_mark_pnl - \
                                                contract_history_frame.greek_pnl
    return contract_history_frame




