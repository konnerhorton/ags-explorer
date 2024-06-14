import plotly.graph_objects as go
import streamlit as st

from scripts import ags, page_utilities, plots


def render_page():
    data = st.session_state["data"]
    df = data.gsd_details_table()
    sample_ids = ags.get_sample_ids(df)
    fig = plots.empty_grain_size_distribution_detail()
    with st.sidebar:
        selected_samples = st.multiselect(label="Select Sample ID", options=sample_ids)

    for samp_id, dfx in df.groupby("SAMP_ID"):

        if samp_id in selected_samples:
            data = dfx[["GRAT_SIZE", "GRAT_PERP"]].sort_values("GRAT_SIZE").to_numpy()
            fig.add_trace(
                go.Scatter(x=data[:, 0], y=data[:, 1], mode="lines", name=samp_id)
            )

    st.plotly_chart(fig)


if "data" not in st.session_state:
    page_utilities.render_load_file_page()
else:
    render_page()
