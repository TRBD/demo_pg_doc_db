
\c demo_doc_db

create TEMP TABLE tmp_load(
  underlying_symbol CHARACTER VARYING(10),
  quote_date date,
  root CHARACTER VARYING(10),
  expiration date,
  strike float,
  option_type char(1),
  open float,
  high float,
  low float,
  close FLOAT,
  trade_volume int,
  bid_size_1545 FLOAT,
  bid_1545 FLOAT,
  ask_size_1545 FLOAT,
  ask_1545 FLOAT,
  underlying_bid_1545 FLOAT,
  underlying_ask_1545 FLOAT,
  implied_underlying_price_1545 FLOAT,
  active_underlying_price_1545 FLOAT,
  implied_volatility_1545 FLOAT,
  delta_1545 FLOAT,
  gamma_1545 FLOAT,
  theta_1545 FLOAT,
  vega_1545 FLOAT,
  rho_1545 FLOAT,
  bid_size_eod FLOAT,
  bid_eod FLOAT,
  ask_size_eod FLOAT,
  ask_eod FLOAT,
  underlying_bid_eod FLOAT,
  underlying_ask_eod FLOAT,
  vwap FLOAT,
  open_interest int
);

-- WINDOWS: Uncomment first and comment out second.  If given access error, copy sample data to c:/tmp
-- \COPY tmp_load from '<path_to_project>/data/sample_data.txt' DELIMITER E'\t' CSV HEADER;
\COPY tmp_load from :'copy_file' DELIMITER E'\t' CSV HEADER;

alter table tmp_load
    add column underlyer_id int,
    add column expiration_id int,
    add column option_type_id int,
    add column contract_id int,
    add column quote_date_id int;


INSERT INTO underlyer(underlying_symbol, root)
    SELECT DISTINCT underlying_symbol, root
    FROM tmp_load
    WHERE NOT EXISTS (
        SELECT 'X'
        FROM underlyer
        WHERE
            tmp_load.underlying_symbol          = underlyer.underlying_symbol
            AND tmp_load.root = underlyer.root
    );


update tmp_load
  set underlyer_id = underlyer.id
from underlyer
  where
  tmp_load.underlying_symbol          = underlyer.underlying_symbol
  AND tmp_load.root = underlyer.root
;


INSERT INTO expirations(expiration)
    SELECT DISTINCT expiration
    FROM tmp_load
    WHERE NOT EXISTS (
        SELECT 'X'
        FROM expirations
        WHERE
            tmp_load.expiration          = expirations.expiration
    );


update tmp_load
  set expiration_id = expirations.id
from expirations
  where
  tmp_load.expiration          = expirations.expiration
;


INSERT INTO option_type(option_type)
    SELECT DISTINCT option_type
    FROM tmp_load
    WHERE NOT EXISTS (
        SELECT 'X'
        FROM option_type
        WHERE
            tmp_load.option_type          = option_type.option_type
    );


update tmp_load
  set option_type_id = option_type.id
from option_type
  where
  tmp_load.option_type          = option_type.option_type
;


insert into contract(expiration_id, option_type_id, underlyer_id, strike)
    SELECT DISTINCT
      expiration_id,
      option_type_id,
      underlyer_id,
      strike
    FROM tmp_load
      WHERE NOT EXISTS (
        SELECT 'X'
        FROM contract
        WHERE
            tmp_load.expiration_id          = contract.expiration_id
      and tmp_load.option_type_id          = contract.option_type_id
      and tmp_load.underlyer_id          = contract.underlyer_id
      and tmp_load.strike = contract.strike
    );


update tmp_load
  set contract_id = contract.id
from contract
        WHERE
            tmp_load.expiration_id          = contract.expiration_id
            and tmp_load.option_type_id          = contract.option_type_id
            and tmp_load.underlyer_id          = contract.underlyer_id
            and tmp_load.strike = contract.strike
;


INSERT INTO quote_date(quote_date)
    SELECT DISTINCT quote_date
    FROM tmp_load
    WHERE NOT EXISTS (
        SELECT 'X'
        FROM quote_date
        WHERE
            tmp_load.quote_date          = quote_date.quote_date
    );


update tmp_load
  set quote_date_id = quote_date.id
from quote_date
  where
  tmp_load.quote_date          = quote_date.quote_date
;


INSERT INTO quote_values(contract_id, date_id, underlying_bid, underlying_ask, bid, ask, implied_vol, delta,
                          gamma, vega, theta, volume)
    SELECT DISTINCT
      contract_id,
      quote_date_id,
      underlying_bid_1545,
      underlying_ask_1545,
      bid_1545,
      ask_1545,
      implied_volatility_1545,
      delta_1545,
      gamma_1545,
      vega_1545,
      theta_1545,
      trade_volume
    FROM tmp_load
    WHERE NOT EXISTS (
        SELECT 'X'
        FROM quote_values
        WHERE
            tmp_load.contract_id          = quote_values.contract_id
            and tmp_load.quote_date_id          = quote_values.date_id
    );


INSERT INTO underlyer_prices(underlyer_id, date_id, underlyer_price)
    SELECT DISTINCT
      underlyer_id,
      quote_date_id,
      .5*(underlying_bid_1545 + underlying_ask_1545)
    FROM tmp_load
    WHERE NOT EXISTS (
        SELECT 'X'
        FROM underlyer_prices
        WHERE
            tmp_load.underlyer_id          = underlyer_prices.underlyer_id
            and tmp_load.quote_date_id          = underlyer_prices.date_id
    );