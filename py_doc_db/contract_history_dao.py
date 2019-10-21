from demo_importlib import pd
from .contract_row import TargetContractRow
from .contract_history import ContractHistory
from .db_conn import pg_connection
from .db_history_retrieval import retrieve_atm_call_history
from .history_funcs import add_pnl_history
from .queries import hjson_qrys
from .demo_exceptions import IllegalArgumentException


class ContractHistoryPersist(object):

    @classmethod
    def create_contract_history(cls, ticker, quote_date, target_time_to_exp, option_type):
        """
        Pull input data and instance a new ContractHistory object
        :param ticker: str
        :param quote_date: Timestamp
        :param target_time_to_exp: int
        :param option_type: 'C' or 'P', 'P' not implemented
        :return: ContractHistory object
        """
        if option_type == 'C':
            tc, history_frame = retrieve_atm_call_history(ticker, quote_date, target_time_to_exp)
            target_row = TargetContractRow.of_row(tc)
            history_frame = add_pnl_history(history_frame)
            ctr_hist = ContractHistory(target_row, target_time_to_exp)
            ctr_hist.history_frame = history_frame
            return ctr_hist
        else:
            raise IllegalArgumentException('create_contract_history', 'option_type', 'str',
                                           'Not configured for {!s} only calls'.format(option_type))

    @classmethod
    def load_exists_cache_local(cls, ticker, quote_date, target_time_to_exp, option_type):
        """
        Retrieve a ContractHistory for parameters if one exists
        :param ticker: str
        :param quote_date: Timestamp
        :param target_time_to_exp: int
        :param option_type: 'C' or 'P', 'P' not implemented
        :return: ContractHistory object if one exists, else return None
        """
        current_id = cls.check_exists_cache_local(ticker, quote_date, target_time_to_exp, option_type)
        if current_id is not None:
            with pg_connection() as conn:
                qry = hjson_qrys.QRY_FROM_ID.format(ID=current_id)
                df_current = pd.read_sql(qry, conn)

            json_value = df_current.iloc[0, 0]
            tte = df_current.iloc[0, 1]
            obj_new = ContractHistory.JSON_SCHEMA.load(json_value)
            obj_new.target_time_to_exp = tte
            return obj_new
        return False

    @classmethod
    def check_exists_cache_local(cls, ticker, quote_date, target_time_to_exp, option_type):
        """
        Retrieve a ContractHistory id for parameters if one exists
        :param ticker: str
        :param quote_date: Timestamp
        :param target_time_to_exp: int
        :param option_type: 'C' or 'P', 'P' not implemented
        :return: int ID if one exists, else return None
        """
        with pg_connection() as conn:
            qry = hjson_qrys.QRY_CHECK_ROW.format(underlying_symbol=ticker,
                                                  quote_date=quote_date,
                                                  target_time_to_exp=target_time_to_exp,
                                                  option_type=option_type)
            df_check = pd.read_sql(qry, conn)
        if df_check.shape[0] > 0:
            return df_check.iloc[0, 0]
        else:
            return None

    @classmethod
    def cache_local(cls, contract_history):
        """
        Store a ContractHistory object, if exists update
        :param contract_history: ContractHistory object to cache
        :return: None
        """
        schema_data = contract_history.JSON_SCHEMA.dumps(contract_history)
        current_id = cls.check_exists_cache_local(contract_history.ticker,
                                                  contract_history.quote_date,
                                                  contract_history.target_time_to_exp,
                                                  contract_history.option_type)
        if current_id is None:
            query_insert = hjson_qrys.QRY_INSERT_CONTRACT_HISTORY.format(
                json=schema_data,
                underlying_symbol=contract_history.ticker,
                quote_date=contract_history.quote_date,
                target_time_exp=contract_history.target_time_to_exp,
                option_type=contract_history.option_type
            )
            with pg_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query_insert)
                conn.commit()
        else:
            query_update = hjson_qrys.QRY_UPDATE.format(ID=current_id, json=schema_data)
            with pg_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query_update)
                conn.commit()

