'''# Streamlitライブラリをインポート
import streamlit as st

# ページ設定（タブに表示されるタイトル、表示幅）
st.set_page_config(page_title="タイトル", layout="wide")

# タイトルを設定
st.title('BMI計算')

user_input = st.number_input('あなたの体重を入力してください',min_value=1)
user_input2 = st.number_input("あなたの身長を入力してください(単位ｍ)",min_value=0.1)

bmi = (user_input / user_input2 / user_input2)

if st.button("計算する"):
    st.write("あなたのBMIは" +str(bmi) + "です。")'''


import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="ことわざガチャ")

# タイトルと説明
st.title('ことわざガチャ')

st.write('ことわざをランダムに表示して、勉強をサポートします！')

# Load the data
@st.cache
def load_data():
    return pd.read_excel("ことわざ集.xlsx")

words_df = load_data()

# ガチャ結果の履歴を保持するリスト
if 'history' not in st.session_state:
    st.session_state.history = []

# ガチャ機能
if st.button('ガチャを引く！'):
    rarity_probs = {
        'N': 0.4,
        'R': 0.3,
        'SR': 0.2,
        'SSR': 0.1
    }
    chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
    subset_df = words_df[words_df['レア度'] == chosen_rarity]
    selected_word = subset_df.sample().iloc[0]

    # セッションステートに選択されたことわざを保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False

    # 履歴に追加する
    st.session_state.history.append(selected_word)

# ガチャ履歴を表示する
if st.session_state.history:
    st.header('ガチャ履歴')
    for idx, word in enumerate(st.session_state.history):
        st.subheader(f"ガチャ {idx + 1}")
        st.write(f"ことわざ名: {word['ことわざ']}")
        st.write(f"レア度: {word['レア度']}")
        st.write(f"意味: {word['意味']}")