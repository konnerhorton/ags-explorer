import plotly.graph_objects as go
import streamlit as sts

from scripts import ags, page_utilities, plots


def render_page():
    data = st.session_state["data"]
    df = data.atterberg_table()
    df = data.atterberg_table()
    fig = plots.plot_empty_uscs_plot()
    for geology, dfx in df.groupby("GEOL_LEG"):
        fig.add_trace(
            go.Scatter(
                x=dfx["LLPL_LL"],
                y=dfx["Plasticity Index"],
                name=geology,
                mode="markers",
            )
        )

    st.plotly_chart(fig)


if "data" not in st.session_state:
    page_utilities.render_load_file_page()
else:
    render_page()
