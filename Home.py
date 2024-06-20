# Import third party libraries

from io import StringIO

import streamlit as st

import scripts.ags as ags

# TODO import table details / names from the ags documentation df = pd.read_csv("ISPT Table Details.csv").set_index("Heading").to_dict("index")


st.header("Getting Started")
st.write("Use the button below to upload the `.ags` file that you want to view.")

uploaded_file = st.file_uploader("Load and `.ags` file")
if uploaded_file is not None:
    if "data" not in st.session_state:
        st.session_state["data"] = ags.AGSdata(uploaded_file)

if "data" in st.session_state:
    data = st.session_state["data"]
    project_name = data.project_name
    df = data.dfs["LOCA"]
    st.write(f"Project Name: {project_name}")
    st.subheader("Your project `Location Details` table")
    st.write(df)
