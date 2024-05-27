from sqlalchemy import MetaData, Integer, String, Table, Column, VARCHAR, FLOAT, TIMESTAMP, DATETIME

metadata = MetaData()

article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", VARCHAR(256)),
    Column("url", VARCHAR(128)),
    Column("published_dt", TIMESTAMP),
    Column("currency_curs", FLOAT),
    Column("text", String),
)
