
import streamlit as st
import pandas as pd
import joblib

# カテゴリ変換用マッピング
axillary_mapping = {'Imaging': 0, 'FNA negative': 1, 'CNB negative': 2}
menopause_mapping = {'Pre': 0, 'Post': 1}
cT_mapping = {'T1': 1, 'T2': 2, 'T3': 3}
histology_mapping = {'IDC': 0, 'ILC': 1, 'DCIS': 2, 'Other': 3}
grade_mapping = {'1': 1, '2': 2, '3': 3}
her2_mapping = {'0': 0, '1+': 1, '2+': 2, '3+': 3}
her2_protein_mapping = {'Negative': 0, 'Positive': 1, 'Unknown': -1}

# モデル読み込み
model = joblib.load("model.pkl")

st.title("Lymph Node Metastasis Prediction")

# 入力フォーム
age = st.number_input("Age", 20, 90)
height = st.number_input("Height (cm)", 130, 200)
weight = st.number_input("Weight (kg)", 30, 120)
axillary = st.selectbox("Axillary Evaluation", list(axillary_mapping.keys()))
menopause = st.selectbox("Menopause", list(menopause_mapping.keys()))
cT = st.selectbox("Clinical T stage", list(cT_mapping.keys()))
histology = st.selectbox("CNB Histology", list(histology_mapping.keys()))
cHG = st.selectbox("Histological Grade", list(grade_mapping.keys()))
er = st.slider("cER (%)", 0, 100)
pgr = st.slider("cPgR (%)", 0, 100)
her2 = st.selectbox("cHER2", list(her2_mapping.keys()))
her2_protein = st.selectbox("HER2 Protein", list(her2_protein_mapping.keys()))
us_size = st.number_input("US tumor size (mm)", 0.0, 100.0)

# 入力をモデル用に整形
input_data = pd.DataFrame([{
    "Age": age,
    "Height": height,
    "Weight": weight,
    "Axillary": axillary_mapping[axillary],
    "Menopause": menopause_mapping[menopause],
    "cT": cT_mapping[cT],
    "Histology": histology_mapping[histology],
    "Grade": grade_mapping[cHG],
    "ER": er,
    "PgR": pgr,
    "HER2": her2_mapping[her2],
    "HER2_Protein": her2_protein_mapping[her2_protein],
    "US_Size": us_size
}])

# 予測ボタン
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    st.success(f"Prediction result: {'Metastasis' if prediction == 1 else 'No Metastasis'}")
