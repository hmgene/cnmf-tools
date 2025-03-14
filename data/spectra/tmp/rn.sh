

import pandas as pd
a=pd.read_csv("results_Tcells/cnmf_run.gene_spectra_score.k_4.dt_2_00.txt",sep="\t",index_col=0).T
a1=pd.read_csv("results_Tcells/cnmf_run.spectra.k_4.dt_2_00.consensus.txt",sep="\t",index_col=0).T
A=pd.read_csv("../T_Cell_NMF_Average_Gene_Spectra.txt",sep="\t",index_col=0,encoding="ISO-8859-1")
x = pd.merge(a,A, how='left', left_index=True, right_index=True)
j = [j for j in x.columns if str(j).isnumeric() ] 
J = [j for j in x.columns if not str(j).isnumeric() ] 
c=[ x for x in x.corr().loc[J,j].idxmax() ]
y=a1.copy()
y.columns = c
y.to_csv("../T_Cell_NMF_Average_Gene_Spectra_v1.txt",sep="\t")


a=pd.read_csv("results_cancer/cnmf_run.gene_spectra_score.k_7.dt_2_00.txt",sep="\t",index_col=0).T
a1=pd.read_csv("results_cancer/cnmf_run.spectra.k_7.dt_2_00.consensus.txt",sep="\t",index_col=0).T
A=pd.read_csv("../Malignant_Cell_NMF_Average_Gene_Spectra.txt",sep="\t",index_col=0)
x = pd.merge(a,A, how='left', left_index=True, right_index=True)
j = [j for j in x.columns if str(j).isnumeric() ] 
J = [j for j in x.columns if not str(j).isnumeric() ] 
c=[ x for x in x.corr().loc[J,j].idxmax() ]
c[2] = "MES1_like"
c[4] = "Other"
y=a1.copy()
y.columns = c
y.to_csv("../Malignant_Cell_NMF_Average_Gene_Spectra_v1.txt",sep="\t")


kjapply(lambda x: x if x in valid_columns else "Others")

x = pd.merge(b.T,B, how='left', left_index=True, right_index=True)
x.corr()

Parse
Monocyte : cluster 0,6,9
Menengeoma : cluster 1
Glioma-cell : cluster 2
ImmSup Myeloid : cluster 3,10
immune Cell :cluster 4
mast cell : cluster 5
SysImm Myeloid : cluster 7
Oligod : cluster 8

10x
ImmSup Myeloid : cluster 0
SysImm Myeloid : cluster 1
Oligd : cluster 2
Monocyte : cluster 3,5,7,9
Immune cell : cluster 4
Glioma cell : cluster 8







