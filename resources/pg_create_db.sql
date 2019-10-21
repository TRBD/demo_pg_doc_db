-- Windows: psql -U postgres -f <path_to_project>\demo_pg_doc_db\resources\pg_create_db.sql postgres
-- Linux: psql -U postgres postgres -f <path_to_project>\demo_pg_doc_db\resources\pg_create_db.sql


DROP DATABASE IF EXISTS demo_doc_db;

CREATE DATABASE demo_doc_db;

\c demo_doc_db

CREATE TABLE underlyer (
  id SERIAL PRIMARY KEY,
  underlying_symbol character varying(10),
  root character varying(10)
);

CREATE TABLE expirations (
  id SERIAL PRIMARY KEY,
  expiration date UNIQUE NOT NULL
);

CREATE TABLE option_type (
  id SERIAL PRIMARY KEY,
  option_type char(1) UNIQUE NOT NULL
);

CREATE TABLE contract (
  id SERIAL PRIMARY KEY,
  expiration_id int references expirations(id),
  option_type_id int references option_type(id),
  underlyer_id int references underlyer(id),
  strike float NOT NULL,
  CONSTRAINT contract_refs_unique UNIQUE (expiration_id, option_type_id, underlyer_id, strike)
  
);

CREATE TABLE quote_date (
  id SERIAL PRIMARY KEY,
  quote_date date UNIQUE NOT NULL
);

CREATE TABLE underlyer_prices (
  underlyer_id int references underlyer(id),
  date_id int references quote_date(id),
  underlyer_price float NOT NULL,
  PRIMARY KEY (date_id,underlyer_id)
);

CREATE TABLE quote_values (
  contract_id int references contract(id),
  date_id int references quote_date(id),
  underlying_bid float,
  underlying_ask float,
  bid float,
  ask float,
  implied_vol float,
  delta float,
  gamma float,
  vega float,
  theta float,
  volume float,
  PRIMARY KEY (date_id,contract_id)
);

CREATE TABLE doc_contract_history
(
  id                    SERIAL PRIMARY KEY,
  contract_history_data JSON                        NOT NULL,
  underlying_symbol     CHARACTER VARYING(16)       NOT NULL,
  quote_date            TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  target_time_to_exp    INTEGER                     NOT NULL,
  option_type           CHARACTER(1)                NOT NULL
);