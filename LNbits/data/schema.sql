CREATE TABLE IF NOT EXISTS accounts (
    userhash text PRIMARY KEY,
    email text,
    pass text
);

CREATE TABLE IF NOT EXISTS wallets (
    hash text PRIMARY KEY,
    name text NOT NULL,
    user text NOT NULL,
    adminkey text NOT NULL,
    inkey text
);

CREATE TABLE IF NOT EXISTS apipayments (
    payhash text PRIMARY KEY,
    amount integer NOT NULL,
    fee integer NOT NULL DEFAULT 0,
    wallet text NOT NULL,
    pending boolean NOT NULL,
    memo text
);

DROP VIEW IF EXISTS balances;

CREATE VIEW balances AS
  SELECT wallet, coalesce(sum(s), 0) AS balance FROM (
      SELECT wallet, sum(amount) AS s -- incoming
      FROM apipayments
      WHERE amount > 0 AND pending = false -- don't sum pending
      GROUP BY wallet
    UNION ALL
      SELECT wallet, sum(amount + fee) AS s -- outgoing, sum fees
      FROM apipayments
      WHERE amount < 0 -- do sum pending
      GROUP BY wallet
  )
  GROUP BY wallet;
