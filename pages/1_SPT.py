# Import standard libraries

# Import third party libraries

import streamlit as st
import yaml

from scripts import ags, page_utilities, plots


def render_page():

    data = st.session_state["data"]
    elevation_min, elevation_max = ags.get_range(data.spt_table()["Top Elevation"])

    st_plotly_layout_settings = dict(
        height=500,
        width=700,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )
    with st.sidebar:
        elevation = st.slider(
            label="Choose and elevation:",
            min_value=elevation_min,
            max_value=elevation_max,
        )
    st.header("SPT by Elevation")
    st.plotly_chart(
        plots.spt_by_depth(ags=data).update(layout=(st_plotly_layout_settings))
    )
    st.header("Relative Density")

    st.plotly_chart(
        plots.spt_histogram(ags=data, elevation=elevation).update(
            layout=(st_plotly_layout_settings)
        )
    )


if "data" not in st.session_state:
    page_utilities.render_load_file_page()
else:
    render_page()
