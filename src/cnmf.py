import pandas as pd
import sklearn.decomposition,sys
from sklearn.decomposition import non_negative_factorization
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import numpy as np

def fract(tt):
    x={
        "All_cell": ["T-cell", "Cancer", "Myeloid", "Oligo","Cycling","Vasculature","Other Immune"],
        "Malignant_cell":["NPC-like", "AC-like", "MES2", "MES1", "OPC-like"],
        "Myeloid_cell": ["Microglia", "Complement_Immunosuppressive", "Neutrophil", "Scavenger_Immunosuppressive", "G2_M", "IFN_Response", "IL1B_CD83_TNF_Inflammatory", "cDC", "G1_S", "Hypoxia", "Inflammatory_microglia", "HS_UPR", "Macrophage", "Monocyte"],
        "T_cell": ["Treg","Cycling_y", "Naive/Memory", "Effector"]
    }
    r = pd.DataFrame(index=tt.index)  # Create a copy of tt

    for k, v in x.items():
        j = tt.columns.str.contains("|".join(v), regex=True)
        if not j.any():  # Check if any column matches
            continue  # Skip to the next iteration if no match is found

        t = tt.loc[:, j].sum(axis=1).replace(0, 1)  # Avoid division by zero
        for ss in v:
            r[f"{ss}"] = (
                tt.loc[:, tt.columns.str.contains(ss)].sum(axis=1) / t
            ).fillna(0)  # Replace NaNs with 0

    # Output the result
    return r


#r=pd.DataFrame(tt) #index=tt["bc_wells"])
#import re
#for k,v in x.items():
#    j= tt.columns.str.contains("|".join(v), regex=True)
#    t=tt.loc[:,j].sum(axis=1) #row_total
#    y=pd.DataFrame() #index=tt["bc_wells"])
#    for ss in v:
#        r[f"frac_{ss}"] = tt.loc[:,tt.columns.str.contains(ss)].apply(lambda x: sum(x),axis=1).div(t,axis=0).values
#r.to_csv(sys.stdout)

def merge(x):
#a="bigdata/cell_metadata.csv"
#b="bigdata/cluster_assignment.csv"
#c="bigdata/cluster_assignment_by_ty.csv"
#d="bigdata/parse_seq_tymillerlab_nov2024.csv"
#x=[a,b,c,d]
    r=pd.merge(pd.read_csv(x[0]),pd.read_csv(x[1])); 
    for i in x[2:]:
        r=pd.merge(r,pd.read_csv(i))
def anno_program_sparse(tt, H):
    #tt=sc.read_h5ad("../x-parse/bigdata/parse/scanpy/anndata.h5ad")
    #j = tt.var_names.intersection(H.columns)
    j = H.columns.intersection(tt.var_names)
    X = tt[:, j].copy()
    X.obs_names_make_unique()
    X = X[:,j]
    if "counts" in X.layers:
        X_data = X.layers["counts"].astype(np.float64)
    else:
        X_data = X.X.astype(np.float64)
    H = H.filter(items=j)
    H = H.reindex(columns=j)
    if np.min(H.values) < 0:
        H = H - np.min(H.values)
    H1 = H.to_numpy()
    W, _, _ = non_negative_factorization(
        X_data, W=None, H=H1, n_components=H.shape[0], init="random", update_H=False,
        solver="cd", beta_loss="frobenius", tol=0.0001, max_iter=1000,
        alpha_W=0.0, alpha_H="same", l1_ratio=0.0, random_state=None,
        verbose=0, shuffle=False
    )
    processed = pd.DataFrame(W, columns=H.index, index=tt.obs_names)
    row_sums = processed.sum(axis=1)
    return (processed.div(row_sums, axis=0) * 100)

def anno_program(tt,x):
    #x="data/spectra/Myeloid_NMF_Average_Gene_Spectra.txt"
    #tt=sc.read_h5ad("bigdata/anndata.h5ad")
    X = tt
    X.obs_names_make_unique()
    try:
        X3 = pd.DataFrame(data=X.layers["counts"].toarray(), columns=X.var_names, index=X.obs.index)
    except KeyError:
        X3 = pd.DataFrame(data=X.X.toarray(), columns=X.var_names, index=X.obs.index)
    if x.endswith(".npz") :
        tmp = np.load(x, allow_pickle=True)
        H = pd.DataFrame(tmp["data"].T,index=tmp["columns"],columns=tmp["index"])
        H.columns=["T-cell", "Cancer-1", "Cancer-2", "Myeloid-1", "Cancer-3", "Cancer-4","Oligo", "Cancer-5", "Myeloid-2", "Myeloid-3", "Myeloid-4", "Cancer-6","Giant Cell Cancer", "Cycling", "Vasculature-2", "Other Immune-1","Vasculature-2.1","Other Immune-2"]
    else:
        H = pd.read_table(x, sep="\t", index_col=0,  encoding="latin1");
    H = H - np.min(H) ;## "frobenius" loss may produce negative values
    H2 = H.T
    H3 = H2.filter(items=X3.columns)
    X4 = X3.filter(items=H3.columns)
    #X4 = X3[list(set(X3.columns).intersection(set(H3.columns)))]
    X5 = X4.values
    H4 = H3.to_numpy()
    X6 = X5.astype(np.float64)
    test = non_negative_factorization(X6, W=None, H=H4, n_components=H4.shape[0], init="random", update_H=False, solver="cd", beta_loss="frobenius", tol=0.0001, max_iter=1000, alpha_W=0.0, alpha_H="same", l1_ratio=0.0, random_state=None, verbose=0, shuffle=False)
    test2 = list(test)
    processed = pd.DataFrame(test2[0], columns=H.columns, index=X.obs.index)
    row_sums = processed.sum(axis=1)
    return (processed.div(row_sums, axis=0) * 100)
    #processed_data.to_csv(sys.stdout)

def merge_columns(df):
    merged = {}
    for col in df.columns:
        if re.search(r"(.+)-\d+$",col):  # Match columns with suffixes
            base_name = re.sub(r"-\d+$", "", col)
            if base_name not in merged:
                merged[base_name] = df.filter(regex=rf"^{base_name}(-\d+)?$").sum(axis=1)
        else:
            if col not in merged:
                merged[col] = df[col]
    return pd.DataFrame(merged)

def count_colname(p,thre,g):
    k=p.columns.intersection(g.columns)
    j=g.columns.difference(k).tolist();
    x = pd.merge(p, g.astype(str), how="left")
    tmp = x.select_dtypes(include=['number']) > thre  
    tmp[j] = x[j].astype(str)  # Ensure grouping columns are strings
    y = tmp.groupby(j).sum().reset_index()
    y = y[~y.apply(lambda row: row.astype(str).eq("nan").any(), axis=1)]
    return y

test="""
from utils.cnmf import *
x="data/spectra/All_Cells_NMF_Average_Gene_Spectra_nz.txt"
tt=sc.read_h5ad("data/sample.h5ad")
a=anno_program(tt,x)
b=anno_program_sparse(tt,x)
"""

#p=pd.read_csv("bigdata/parse_tm01to34_4programset.csv")
#m=pd.read_csv("bigdata/merged_meta.csv")
#g=m[["bc_wells","sample"]]
#count_colname(p,20,m[["bc_wells","sample"]])
#r.to_csv("data/summary_sample_program.csv")
#
#r=pd.DataFrame(index=tt["bc_wells"])
#import re
#for k,v in x.items():
#    j= tt.columns.str.contains("|".join(v), regex=True)
#    t=tt.loc[:,j].sum(axis=1) #row_total
#    y=pd.DataFrame(index=tt["bc_wells"])
#    for ss in v:
#        #y[ss] = tt.loc[:,tt.columns.str.contains(ss)].apply(lambda x: sum(x),axis=1).div(t,axis=0).values
#        r[f"frac_{ss}"] = tt.loc[:,tt.columns.str.contains(ss)].apply(lambda x: sum(x),axis=1).div(t,axis=0).values
#        #y.apply(lambda x: ",".join(list(y.columns[x > 0.2])), axis=1)
#    #r[k] = y.apply(lambda x: ",".join(list(y.columns[x > 0.2])), axis=1)















