"""
Queries for the primary historical database table workflows
"""

# Find the correct Expiration
QUERY_LISTED_EXPIRATIONS = """
  SELECT
    DISTINCT
  exp.expiration,
  u.underlying_symbol,
  d.quote_date
  from quote_values quote
      join quote_date d on quote.date_id=d.id
      join contract ctr on ctr.id=quote.contract_id
      join expirations exp on ctr.expiration_id=exp.id
      join option_type ot on ot.id=ctr.option_type_id
      join underlyer u on u.id=ctr.underlyer_id

  where u.underlying_symbol = '{ticker}'
        and exp.expiration >= d.quote_date
        and d.quote_date = '{quote_date}'
  ORDER BY d.quote_date, exp.expiration
;
"""

# Find the correct contract at expiration
QUERY_BY_EXPIRATION_AT_DATE = """
SELECT
  ctr.id as security_id,
  u.underlying_symbol,
  u.root,
  exp.expiration,
  ctr.strike,
  ot.option_type,
  d.quote_date,
  .5*(underlying_bid + underlying_ask) as underlyer_price,
  quote.ask,
  quote.bid,
  quote.delta,
  quote.vega,
  quote.gamma,
  quote.theta,
  quote.implied_vol
  from quote_values quote
      join quote_date d on quote.date_id=d.id
      join contract ctr on ctr.id=quote.contract_id
      join expirations exp on ctr.expiration_id=exp.id
      join option_type ot on ot.id=ctr.option_type_id
      join underlyer u on u.id=ctr.underlyer_id
  where u.underlying_symbol = '{ticker}'
        and exp.expiration = '{expiration_date}'
        and d.quote_date = '{quote_date}'
order BY expiration, option_type, strike;
"""

# Find the contract data

QUERY_CONTRACT_MULTI_DATE = """
SELECT
  quote.contract_id as security_id,
  d.quote_date,
  .5*(underlying_bid + underlying_ask) as underlyer_price,
  quote.ask,
  quote.bid,
  quote.delta,
  quote.vega,
  quote.gamma,
  quote.theta,
  quote.implied_vol
  from quote_values quote
      join quote_date d on quote.date_id=d.id
  where quote.contract_id = {security_id}
      and d.quote_date in (
        select quote_date
          from quote_date d
          where d.quote_date >= '{quote_date}' and d.quote_date <= '{expiration_date}')
order BY d.quote_date;
"""
