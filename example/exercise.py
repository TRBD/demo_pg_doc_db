from demo_importlib import pd
from py_doc_db.contract_history_dao import ContractHistoryPersist
from py_doc_db.db_history_retrieval import pg_connection
from .new_history_funcs import add_calc_pnl_history


def store_run_params(dt, ticker, target_time_to_exp, option_type='C'):
    """
    Initialize and store a ContractHistory object
    :param dt: Timestamp
    :param ticker: str
    :param target_time_to_exp: int
    :param option_type: str
    :return: ContractHistory
    """
    x = ContractHistoryPersist.create_contract_history(ticker, dt, target_time_to_exp, option_type)
    ContractHistoryPersist.cache_local(x)
    return x


def retrieve_run_params(dt, ticker, target_time_to_exp, option_type='C'):
    """
    Retrieve an existing ContractHistory object
    :param dt: Timestamp
    :param ticker: str
    :param target_time_to_exp: int
    :param option_type: str
    :return: ContractHistory or None
    """
    x = ContractHistoryPersist.load_exists_cache_local(ticker, dt, target_time_to_exp, option_type)
    return x


def add_new_history_data(dt, ticker, target_time_to_exp, option_type='C'):
    """
    Retrieve an existing ContractHistory object, add data to it's history_frame, and update it in storage
    :param dt: Timestamp
    :param ticker: str
    :param target_time_to_exp: int
    :param option_type: str
    :return: ContractHistory
    """
    x = retrieve_run_params(dt, ticker, target_time_to_exp, option_type)
    add_calc_pnl_history(x.history_frame, x.target_contract_row)
    ContractHistoryPersist.cache_local(x)
    return x


def delete_history(id_delete):
    """
    Clears db of example data
    :param id_delete: int
    :return: None
    """
    query_delete = """delete from doc_contract_history
            where id = '{id}'
            ;""".format(id=id_delete)
    with pg_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query_delete)
        conn.commit()
        cursor.close()

def run_exercise():
    """
    Runs through exercies:
    first instancing/caching an object,
    retrieving it separately,
    modifying it,
    and retrieving it again with the modified changes

    Deletes the data afterwards.
    :return: None
    """
    dt = pd.Timestamp(2016, 6, 1)
    ticker = '^VIX'
    target_time_to_exp = 21
    option_type = 'C'

    existing_id = ContractHistoryPersist.check_exists_cache_local(ticker, dt, target_time_to_exp, option_type)
    if existing_id  is not None:
        delete_history(existing_id)

    contract_history_0 = store_run_params(dt, ticker, target_time_to_exp, option_type)
    print(contract_history_0.history_frame.tail(1).T)
    contract_history_1 = retrieve_run_params(dt, ticker, target_time_to_exp, option_type)
    print(contract_history_1.history_frame.tail(1).T)
    contract_history_2 = add_new_history_data(dt, ticker, target_time_to_exp)
    print(contract_history_2.history_frame.tail(1).T)
    contract_history_3 = retrieve_run_params(dt, ticker, target_time_to_exp, option_type)
    print(contract_history_3.history_frame.tail(1).T)


if __name__ == '__main__':
    run_exercise()