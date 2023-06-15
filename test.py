import pandas as pd

df = pd.DataFrame()
df = df.sort_values("update_at", ascending=False)
df_latest = df.groupby(["cupid_id", "product_id"]).head(1)
df_machine = df[df.source=="machine"].rename(columns={"tags": "tags_2"})
df_machine = df_machine.groupby(["cupid_id", "product_id"]).head(1)
df_machine = df_machine.drop(columns=["source", "update_at"])
df_latest = df_latest.merge(df_machine, how="left", on=["cupid_id", "product_id"])
