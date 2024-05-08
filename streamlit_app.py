# Streamlitライブラリをインポート
import streamlit as st

# ページ設定（タブに表示されるタイトル、表示幅）
st.set_page_config(page_title="タイトル", layout="wide")

# タイトルを設定
st.title('MBI計算')

if st.button:
  st.write = ("あなたのBPMは"+str(BMI)+"です。")

user_input = st.number_input('あなたの体重を入力してください',min_value=1)
user_input2 = st.number_input("あなたの身長を入力してください(単位ｍ)",min_value=0.1)

BMI = (user_input / user_input2 / user_input2)

st.button = ("計算")
