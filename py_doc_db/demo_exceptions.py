

class NoRDBMSDataException(Exception):
    def __init__(self, ticker, quote_date, *args, **kwargs):
        super(NoRDBMSDataException, self).__init__(*args, **kwargs)
        self.ticker = ticker
        self.quote_date = quote_date


class IllegalArgumentException(Exception):
    def __init__(self, function_name, arg_name, arg_type, *args, **kwargs):
        super(IllegalArgumentException, self).__init__(*args, **kwargs)
        self.function_name = function_name
        self.arg_name = arg_name
        self.arg_type = arg_type
