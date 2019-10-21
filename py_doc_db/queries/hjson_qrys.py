"""
Queries for the doc_contract_history table
"""

QRY_CHECK_ROW = """
  select
  ID
  from
  doc_contract_history
  where
  underlying_symbol = '{underlying_symbol}'
  and quote_date = '{quote_date}'
  and target_time_to_exp = {target_time_to_exp}
  and option_type = '{option_type}'
;
"""


QRY_FROM_ID = """
  select
  contract_history_data
  ,target_time_to_exp
  from
  doc_contract_history
  where ID = {ID}
;
"""


QRY_INSERT_CONTRACT_HISTORY = """
    insert into
    doc_contract_history(
    contract_history_data,
    underlying_symbol,
    quote_date,
    target_time_to_exp,
    option_type) values
    ('{json}',
    '{underlying_symbol}',
    '{quote_date}',
    {target_time_exp},
    '{option_type}')
"""

QRY_UPDATE = """
  update doc_contract_history
  set contract_history_data = '{json}'
  where ID = {ID}
 """
