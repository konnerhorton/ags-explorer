# Import standard libraries

# Import third party libraries

import streamlit as st

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
        min_elevation_chart, max_elevation_chart = st.slider(
            label="Select a range of elevations",
            value=(elevation_min, elevation_max),
            min_value=elevation_min,
            max_value=elevation_max,
        )
        company = st.selectbox(
            label="Select company", options=list(data.spt_table()["LOCA_ORCO"].unique())
        )
        alignment = st.selectbox(
            label="Select alignment",
            options=list(data.spt_table()["LOCA_ALID"].unique()),
        )

    st.header("SPT by Elevation")

    st.plotly_chart(
        plots.spt_by_depth(ags=data).update(layout=(st_plotly_layout_settings))
    )
    st.header("Relative Density")
    fig_cohesive, fig_granular = plots.spt_histogram(
        ags=data,
        elevations=(min_elevation_chart, max_elevation_chart),
        company=company,
        alignment=alignment,
    )

    st.subheader("Cohesive")
    st.plotly_chart(fig_cohesive.update(layout=(st_plotly_layout_settings)))
    st.subheader("Non-cohesive")
    st.plotly_chart(fig_granular.update(layout=(st_plotly_layout_settings)))


if "data" not in st.session_state:
    page_utilities.render_load_file_page()
else:
    render_page()
