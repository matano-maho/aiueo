# Streamlitライブラリをインポート
import streamlit as st

# ページ設定（タブに表示されるタイトル、表示幅）
st.set_page_config(page_title="タイトル", layout="wide")

# タイトルを設定
st.title('MBI計算')

st.write("あなたの体重を教えてください")
user_input = st.number_input('あなたの体重を入力してください')

