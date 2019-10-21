from demo_importlib import pd, Schema, fields, post_load


class TargetContractRow(object):
    """
    For given filter, returns this with all relevant info on contract

    Quote date row of all info for a contract (used in a strategy)
    """
    def __init__(self):
        self.security_id = None
        self.underlying_symbol = None
        self.root_symbol = None
        self.expiration_date = None
        self.strike = None
        self.option_type = None
        self.quote_date = None
        self.underlying_price = None
        self.ask = None
        self.bid = None
        self.delta = None
        self.vega = None
        self.implied_vol = None
        self.gamma = None
        self.theta = None

    @classmethod
    def of_row(cls, row):
        """
        Class method for returning new object from database queried input row
        :param row: pd.Series, database return row
        :return: TargetContractRow
        """
        obj = cls()
        obj.security_id = row.security_id
        obj.underlying_symbol = row.underlying_symbol
        obj.root_symbol = row.root
        obj.expiration_date = row.expiration
        obj.strike = row.strike
        obj.option_type = row.option_type
        obj.quote_date = row.quote_date
        obj.underlying_price = row.underlyer_price
        obj.ask = row.ask
        obj.bid = row.bid
        obj.delta = row.delta
        obj.vega = row.vega
        obj.gamma = row.gamma
        obj.theta = row.theta
        obj.implied_vol = row.implied_vol
        return obj

    def to_series(self):
        """Convert object to pd.Series
        """
        values = [self.security_id, self.underlying_symbol, self.root_symbol, self.expiration_date, self.strike,
                  self.option_type, self.quote_date, self.underlying_price, self.ask, self.bid, self.delta,
                  self.implied_vol, self.vega, self.gamma, self.theta]
        columns = ['security_id', 'underlying_symbol', 'root_symbol', 'expiration_date', 'strike',
                   'option_type', 'quote_date', 'underlying_price', 'ask', 'bid', 'delta', 'implied_vol',
                   'vega', 'gamma', 'theta']
        return pd.Series(values, index=columns)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.security_id == other.security_id and \
               self.quote_date == other.quote_date

    def __hash__(self):
        return hash((self.security_id, self.quote_date))

    def __str__(self):
        return 'TargetContractRow: {!s} | {!s} | {!s}'.format(self.underlying_symbol,
                                                              self.security_id,
                                                              self.quote_date)


class TargetContractRowSchema(Schema):
    """
    JSON schema template for TargetContractRow
    """
    security_id = fields.Int()
    underlying_symbol = fields.Str()
    root_symbol = fields.Str()
    expiration_date = fields.Date()
    strike = fields.Float()
    option_type = fields.Str()
    quote_date = fields.Date()
    underlying_price = fields.Float()
    ask = fields.Float()
    bid = fields.Float()
    delta = fields.Float()
    vega = fields.Float()
    implied_vol = fields.Float()
    gamma = fields.Float()
    theta = fields.Float()

    @post_load
    def make_target_contract_row(self, data, **kwargs):
        obj = TargetContractRow()
        for k, v in data.items():
            obj.__dict__[k] = v
        return obj

    def loads(self, data, **kwargs):
        return super(TargetContractRowSchema, self).loads(data, **kwargs)

    def dump(self, obj, **kwargs):
        return super(TargetContractRowSchema, self).dump(obj, **kwargs)

    def dumps(self, obj, *args, **kwargs):
        return super(TargetContractRowSchema, self).dumps(obj, *args, **kwargs)

    def load(self, data, **kwargs):
        return super(TargetContractRowSchema, self).load(data, **kwargs)