import plotly.graph_objects as go
import streamlit as st
import yaml

from scripts import ags, page_utilities, plots


def render_page():
    data = st.session_state["data"]
    # df = data.rqd_table()
    st_plotly_layout_settings = dict(
        height=500,
        width=700,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )
    # with st.sidebar:
    #     elevation = st.slider(
    #         label="Choose and elevation:",
    #         min_value=elevation_min,
    #         max_value=elevation_max,
    #     )
    st.header("RQD by Elevation")
    st.plotly_chart(
        plots.rqd_by_depth(ags=data).update(layout=(st_plotly_layout_settings))
    )


if "data" not in st.session_state:
    page_utilities.render_load_file_page()
else:
    render_page()
