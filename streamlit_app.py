# Streamlitライブラリをインポート
import streamlit as st

# ページ設定（タブに表示されるタイトル、表示幅）
st.set_page_config(page_title="タイトル", layout="wide")

# タイトルを設定
st.title('BMI計算')

user_input = st.number_input('あなたの体重を入力してください',min_value=1)
user_input2 = st.number_input("あなたの身長を入力してください(単位ｍ)",min_value=0.1)

bmi = (user_input / user_input2 / user_input2)

st.button("Say hello")

if 1==1:
    st.write("あなたのBMIは" + bmi + "です。")

