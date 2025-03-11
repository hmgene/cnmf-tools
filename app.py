import streamlit as st
cnmf_page = st.Page("pages/cnmf_tools.py", title="cNMF Program tools", icon=":material/arrow_forward:")
localtools_page = st.Page("pages/deploy.py", title="Install Local cNMFTools", icon=":material/arrow_forward:")

pg = st.navigation({ 
    "Tools" : [ cnmf_page, localtools_page ]
})
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
