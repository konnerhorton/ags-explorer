from collections import OrderedDict

import duckdb
import numpy as np
import pandas as pd
from python_ags4 import AGS4


def convert_series_to_float(series):
    try:
        return series.astype(float)
    except ValueError:
        return series


def get_dataframes_from_ags(path: str) -> dict[str, pd.DataFrame]:
    tables, headings = AGS4.AGS4_to_dataframe(path)

    data_frames = {}
    for name, df in tables.items():
        # TODO make use of the `column_unit_type` to assign dtypes and units
        column_unit_type = list(zip(df.columns, df.loc[0], df.loc[1]))
        df = df.loc[2:].reset_index().drop(columns="index")
        # TODO `LOCA_GL` is not converting to a float
        df = df.apply(lambda x: convert_series_to_float(x))
        data_frames[name] = df
    return data_frames


def get_range(series):
    return series.min(), series.max()


def get_sample_ids(df):
    return list(df["SAMP_ID"].unique())


class AGSdata:
    def __init__(self, path):
        self.dfs = get_dataframes_from_ags(path)
        self.project_name = self.dfs["PROJ"]["PROJ_NAME"].values[0]
        # self.valid_ags =

    def merge_geology(self, table, depth_column):
        df0 = self.dfs[table]
        df1 = self.dfs["GEOL"]
        df1 = df1[["LOCA_ID", "GEOL_TOP", "GEOL_BASE", "GEOL_LEG"]].loc[
            df1["GEOL_LEG"] != ""
        ]
        for c in ["GEOL_TOP", "GEOL_BASE"]:
            df1[c] = df1[c].astype(float)
        sql_query = f"""SELECT *
            FROM df0
            LEFT JOIN df1
            on df0.LOCA_ID = df1.LOCA_ID
            and df0.{depth_column}
            BETWEEN df1.GEOL_TOP
            and df1.GEOL_BASE;"""

        return duckdb.sql(f"{sql_query}").df()

    def spt_table(self):
        # TODO for the tkinter version, this should pull from a db
        df0 = self.merge_geology("ISPT", "ISPT_TOP")[
            ["LOCA_ID", "ISPT_TOP", "ISPT_NVAL", "GEOL_LEG"]
        ]
        df1 = self.dfs["LOCA"][["LOCA_ID", "LOCA_GL"]]
        df = pd.merge(left=df0, right=df1, how="left", on="LOCA_ID")
        # TODO fix the "LOCA_GL" to float problem and remove `.astype()`
        df["Top Elevation"] = df["LOCA_GL"].astype(float) - df["ISPT_TOP"]
        categories_lower_limits = OrderedDict(
            (
                ("V Loose (0-4)", 0),
                ("Loose (4-10)", 4),
                ("Med (10-30)", 10),
                ("Dense (30-50)", 30),
                ("V. Dense (>50)", 50),
                ("Ref.", 150),
            )
        )

        bins = [v for k, v in categories_lower_limits.items()]
        bins.append(np.inf)
        labels = [k for k, v in categories_lower_limits.items()]
        df["Category"] = pd.cut(df["ISPT_NVAL"], bins=bins, labels=labels)

        return df

    def gsd_details_table(self):
        df0 = self.dfs["GRAT"][
            ["LOCA_ID", "SAMP_ID", "SPEC_REF", "SPEC_DPTH", "GRAT_SIZE", "GRAT_PERP"]
        ]
        df1 = self.dfs["LOCA"][["LOCA_ID", "LOCA_GL"]]
        df = pd.merge(left=df0, right=df1, how="left", on="LOCA_ID")
        df["Elevation"] = df["LOCA_GL"].astype(float) - df["SPEC_DPTH"].astype(float)
        return df

    def rqd_table(self):
        df0 = self.dfs["CORE"][
            ["LOCA_ID", "CORE_TOP", "CORE_BASE", "CORE_PREC", "CORE_SREC", "CORE_RQD"]
        ]
        df1 = self.dfs["LOCA"][["LOCA_ID", "LOCA_GL"]]
        df = pd.merge(left=df0, right=df1, how="left", on="LOCA_ID")
        df["Elevation Top"] = df["LOCA_GL"].astype(float) - df["CORE_TOP"].astype(float)
        df["Elevation Base"] = df["LOCA_GL"].astype(float) - df["CORE_BASE"].astype(
            float
        )
        df["Elevation Mid"] = (df["Elevation Top"] + df["Elevation Base"]) / 2
        return df

    def atterberg_table(self):
        df0 = self.merge_geology("LLPL", "SAMP_TOP")[
            ["LOCA_ID", "SAMP_ID", "SAMP_TOP", "GEOL_LEG", "LLPL_LL", "LLPL_PL"]
        ]
        df1 = self.dfs["LOCA"][["LOCA_ID", "LOCA_GL"]]
        df = pd.merge(left=df0, right=df1, how="left", on="LOCA_ID")
        df["Plasticity Index"] = df["LLPL_LL"] - df["LLPL_PL"]
        return df
