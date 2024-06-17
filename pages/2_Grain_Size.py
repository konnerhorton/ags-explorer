import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from scripts import ags, page_utilities, plots, soil_classification


def render_page():
    data = st.session_state["data"]
    df = data.gsd_details_table()
    sample_ids = ags.get_sample_ids(df)
    fig = plots.empty_grain_size_distribution_detail()
    with st.sidebar:
        selected_samples = st.multiselect(label="Select Sample ID", options=sample_ids)
    records = []
    for samp_id, dfx in df.groupby("SAMP_ID"):

        if samp_id in selected_samples:
            data = dfx[["GRAT_SIZE", "GRAT_PERP"]].sort_values("GRAT_SIZE").to_numpy()
            fig.add_trace(
                go.Scatter(x=data[:, 0], y=data[:, 1], mode="lines", name=samp_id)
            )
            gsd_data = dfx[["GRAT_SIZE", "GRAT_PERP"]].to_numpy()
            gsd = soil_classification.get_gsd_general(gsd_data)
            gsd["Sample ID"] = samp_id
            records.append(gsd)

    st.plotly_chart(fig)
    if len(selected_samples) > 0:
        results = pd.DataFrame(records).set_index("Sample ID")
        st.write(results[["Gravel", "Sand", "Fines"]])


if "data" not in st.session_state:
    page_utilities.render_load_file_page()
else:
    render_page()
