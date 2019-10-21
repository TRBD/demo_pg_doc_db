from demo_importlib import pd, Schema, fields, post_load, pre_dump
from .contract_row import TargetContractRowSchema


class ContractHistorySchema(Schema):
    """
    JSON schema template for ContractHistory
    """
    target_contract_row = fields.Nested(TargetContractRowSchema)
    history_frame = fields.Str()

    @pre_dump
    def jsonify_history_frame(self, in_data, **kwargs):
        out_data = {'target_contract_row': in_data.target_contract_row,
                    "history_frame": in_data.history_frame.to_json(date_format='iso')}
        return out_data

    @post_load
    def make_contract_history(self, data, **kwargs):
        obj = ContractHistory(data['target_contract_row'], False)
        obj.history_frame = pd.read_json(data['history_frame'], convert_dates=['quote_date'])
        obj.history_frame.sort_values(by='quote_date', inplace=True)
        return obj

    def loads(self, data, **kwargs):
        return super(ContractHistorySchema, self).loads(data, **kwargs)

    def dump(self, obj, **kwargs):
        return super(ContractHistorySchema, self).dump(obj, **kwargs)

    def dumps(self, obj, *args, **kwargs):
        return super(ContractHistorySchema, self).dumps(obj, *args, **kwargs)

    def load(self, data, **kwargs):
        return super(ContractHistorySchema, self).load(data, **kwargs)


class ContractHistory(object):
    """
    Composite for holding a target initial contract and the following history/analytics

    Attributes:
        target_contract_row: TargetContractRow
        history_frame: DataFrame
        target_time_to_exp: int
    """
    JSON_SCHEMA = ContractHistorySchema()

    def __init__(self, target_contract_row, target_time_to_exp):
        """
        :param target_contract_row: TargetContractRow
        :param target_time_to_exp: int
        :return: ContractHistory
        """
        self.target_time_to_exp = target_time_to_exp
        self.target_contract_row = target_contract_row
        self.history_frame = None

    @property
    def sid(self):
        return self.target_contract_row.security_id

    @property
    def ticker(self):
        return self.target_contract_row.underlying_symbol

    @property
    def exp_date(self):
        return self.target_contract_row.expiration_date

    @property
    def option_type(self):
        return self.target_contract_row.option_type

    @property
    def quote_date(self):
        return self.target_contract_row.quote_date

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.target_contract_row == other.target_contract_row

    def __hash__(self):
        return hash(self.target_contract_row)