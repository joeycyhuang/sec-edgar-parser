import pandas as pd
import duckdb
import json
import os

with open("data/tesla/tesla.json", "r") as f:
    data = json.load(f)

records = []
for k, v in data["facts"]["us-gaap"].items():
    for unit_name, unit_values in v.get("units", {}).items():
        for d in unit_values:
            d["fact"] = k
            d["unit"] = unit_name
            records.append(d)

df = pd.DataFrame(records)

with duckdb.connect("sec.duckdb") as con:
    try:
        con.execute("INSTALL delta;")
        con.execute("LOAD delta;")
        print("Delta extension loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load delta extension: {e}")
        print("Falling back to Parquet format")
    
    con.execute("CREATE SCHEMA IF NOT EXISTS filling;")
    con.register("df_view", df)
    
    if not os.path.exists('data/tesla/tesla_facts_delta'):
        os.makedirs('data/tesla/tesla_facts_delta')
    
    try:
        from deltalake import write_deltalake
        write_deltalake('data/tesla/tesla_facts_delta', df)
        result = con.execute("SELECT * FROM delta_scan('data/tesla/tesla_facts_delta') LIMIT 5").df()
        print("Successfully saved as Delta format using deltalake package")
    except ImportError:
        print("deltalake package not available.")
    except Exception as e:
        print(f"Delta format failed: {e}")

print(result)