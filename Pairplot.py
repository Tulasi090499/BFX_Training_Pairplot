import streamlit as st
from pathlib import Path
import pandas as pd
import seaborn as sns


description = """
Application to explore the numerical columns as a pair plot.
"""

def get_datasets():
    datasets = root.glob("*.csv")
    return list(datasets)

def upload_dataset():
    st.header("Upload a New Dataset")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type="csv")
    upload = st.button("Upload")

    if upload:
        data = uploaded_file.getvalue()
        path = root.joinpath(uploaded_file.name)
        path.write_bytes(data)
        st.write("saved the file to", path)

        # force streamlit to rerun
        st.experimental_rerun()
        
def pairplot(df, color):
	if color != "None":
		ax = sns.pairplot(data=df, hue = color)
	else:
		ax = sns.pairplot(data=df)
	st.pyplot(ax.figure)
	
def get_categorical_columns(df):
	return (df.loc[:, df.apply(lambda x: x.nunique()) <= 10]).select_dtypes(include='object').columns.tolist()

root = Path("datasets")

label_upload = "Upload a New Dataset"
label_color = "None"

with st.sidebar:
    st.title("Pair Plot")
    st.markdown(description)

    options = [label_upload] + get_datasets()
    path = st.selectbox("Select a dataset", options)

    if path != label_upload:
        df = pd.read_csv(path)
        options = [label_color] + get_categorical_columns(df)
        path = st.selectbox("Color by", options)

if path == label_upload:
    upload_dataset()
else:
    st.title("Pair Plot")
    pairplot(df, path)

