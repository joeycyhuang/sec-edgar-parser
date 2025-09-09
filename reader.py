import duckdb
import pandas as pd


with duckdb.connect("sec.duckdb") as con:
    delta = con.execute("""
        SELECT * FROM delta_scan('data/tesla/tesla_facts_delta')
""").df()

print(delta)