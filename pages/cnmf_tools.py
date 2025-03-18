import streamlit as st
import scanpy as sc
import pandas as pd
import io
from src.cnmf import *
rr=[
"",
"data/spectra/All_Cells_NMF_Average_Gene_Spectra_nz.txt",
"data/spectra/Myeloid_NMF_Average_Gene_Spectra.txt",
"data/spectra/T_Cell_NMF_Average_Gene_Spectra_v1.txt",
"data/spectra/Malignant_Cell_NMF_Average_Gene_Spectra_v1.txt"
]

st.title("cNMF Back Calculation")

uploaded_file = st.file_uploader("Upload an `.h5ad` File", type=["h5ad"])

if "tt" not in st.session_state:
    st.session_state.tt = None
    st.session_state.f = None  

if uploaded_file:
    st.success(f"File `{uploaded_file.name}` uploaded successfully!")
    try:
        with io.BytesIO(uploaded_file.getvalue()) as file_buffer:
            st.session_state.tt = sc.read_h5ad(file_buffer)
        st.session_state.f = uploaded_file.name
        st.write("### File Loaded Successfully!")
    except Exception as e:
        st.error(f"Error loading `.h5ad` file: {e}")

if "tt" not in st.session_state:
    st.session_state.tt = None
    st.session_state.f = None  

f = st.session_state.f
tt = st.session_state.tt
if tt is not None:
    st.write(f"{f}.obs:")
    st.dataframe(tt.obs)

f1 = st.selectbox("Select a Program file", rr)
H = None
if f1 != "":
    H = pd.read_table(f1, sep="\t", index_col=0, encoding="latin1").T

if st.button("Run cNMF Back Calculation") and H is not None:
    st.write("calculating..")
    p = anno_program_sparse(tt, H)
    st.write("done")
        
    st.write("Cell by Program Scores")
    st.dataframe(p, width=500, height=300, hide_index=False)

    st.write("Cell by Program Fractions (Columns were merged)")
    p1 = fract(p)
    st.dataframe(p1, width=500, height=300, hide_index=False)

