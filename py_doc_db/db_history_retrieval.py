"""
Methods for retrieving relevant information for a given input parameter and filter set
"""
from demo_importlib import pd
from .db_conn import pg_connection
from .queries import rdbms_qrys
from .demo_exceptions import NoRDBMSDataException


def pull_underlyer_at_date_atm_call(ticker, quote_date, target_time_to_exp):
    """
    For a given ticker, given start date, given target time to expiration, find the best matched
    row of data from the historic database.

    :param ticker: str
    :param quote_date: Timestamp
    :param target_time_to_exp: int
    :return: pd.Series of a single date best qualified row
    """
    listed_expiration_query = rdbms_qrys.QUERY_LISTED_EXPIRATIONS.format(ticker=ticker,
                                                                         quote_date=quote_date)

    with pg_connection() as conn:
        ticker_expirations = pd.read_sql(listed_expiration_query, conn)
    if ticker_expirations.shape[0] == 0:
        raise NoRDBMSDataException(ticker, quote_date)
    ticker_expirations.expiration = pd.to_datetime(ticker_expirations.expiration)
    time_to_exps = ticker_expirations.expiration.apply(lambda x: len(pd.bdate_range(quote_date, x)))
    time_to_exps = time_to_exps[time_to_exps > target_time_to_exp]
    best_exp = ticker_expirations.loc[(time_to_exps - target_time_to_exp).abs().idxmin()]
    with pg_connection() as conn:
        qry = rdbms_qrys.QUERY_BY_EXPIRATION_AT_DATE.format(ticker=ticker,
                                                            quote_date=quote_date,
                                                            expiration_date=best_exp.expiration)
        expiration_contracts = pd.read_sql(qry, conn)
    call_contracts = expiration_contracts[expiration_contracts.option_type=='C']
    target_contract = call_contracts[call_contracts.strike > call_contracts.underlyer_price]
    target_contract = target_contract[target_contract.delta <= 0.5]
    target_contract = target_contract.loc[target_contract.strike.idxmin()]
    return target_contract


def pull_contract_history(sid, quote_date, expiration_date):
    """
    For a given contract id, quote date and expiration date, pull the relevant history on dates on and between

    :param sid: int
    :param quote_date: Timestamp
    :param expiration_date: Timestamp
    :return: pd.DataFrame history_df
    """
    query = rdbms_qrys.QUERY_CONTRACT_MULTI_DATE.format(security_id=sid,
                                                        quote_date=quote_date,
                                                        expiration_date=expiration_date)
    with pg_connection() as conn:
        contract_history_full = pd.read_sql(query, conn)
    return contract_history_full.sort_values(by='quote_date')


def retrieve_atm_call_history(ticker, quote_date, target_time_to_exp):
    """
    For a given ticker, given start date, given target time to expiration, find the best matched
    TargetContractRow and history_df
    :param ticker: str
    :param quote_date: Timestamp
    :param target_time_to_exp: int
    :return: (pd.Series of a single date best qualified row, pd.DataFrame history_df)
    """
    tc = pull_underlyer_at_date_atm_call(ticker, quote_date, target_time_to_exp)
    contract_history_frame = pull_contract_history(tc.security_id, pd.Timestamp(tc.quote_date), tc.expiration)
    return tc, contract_history_frame



