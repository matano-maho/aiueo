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

st.set_page_config(page_title="ことわざバトル")

# Load the data
@st.cache_data
def load_data():
    return pd.read_excel("ことわざ集.xlsx")

words_df = load_data()

# ガチャ結果の履歴を保持するリスト
if 'history' not in st.session_state:
    st.session_state.history = []

if 'selected_word' not in st.session_state:
    st.session_state.selected_word = None

if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False


# タイトルと説明
st.title('ことわざバトル')
st.write('ことわざをランダムに表示して、勉強をサポートします！')
if st.button('ノーマルガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'N']
    selected_word = subset_df.sample().iloc[0]

    # セッションステートに選択されたことわざを保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    # 履歴に追加する
    st.session_state.history.append(selected_word)

if st.button('レアガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'R']
    selected_word = subset_df.sample().iloc[0]

    # セッションステートに選択されたことわざを保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    # 履歴に追加する
    st.session_state.history.append(selected_word)

if st.button('スーパーレアガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'SR']
    selected_word = subset_df.sample().iloc[0]

    # セッションステートに選択されたことわざを保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    # 履歴に追加する
    st.session_state.history.append(selected_word)

if st.button('超スーパーレアガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'SSR']
    selected_word = subset_df.sample().iloc[0]

    # セッションステートに選択されたことわざを保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    # 履歴に追加する
    st.session_state.history.append(selected_word)


if st.session_state.selected_word is not None:
    st.header(f"意味: {st.session_state.selected_word['意味']}")
    
    # ユーザーが入力するテキストボックス
    user_input = st.text_input("ことわざを入力してください:")

    if st.button('正誤判定をする'):
        # 入力された文字列とことわざを比較
        if user_input == st.session_state.selected_word['ことわざ']:
            st.success("正解です！")
            st.session_state.points += 1
        else:
            st.error("違います。")
            st.write('正解は' + st.session_state.selected_word['ことわざ'] + 'です')


# ガチャ履歴をサイドバーに表示する
st.sidebar.title('ガチャ履歴')
if st.session_state.history:
    for idx, word in enumerate(st.session_state.history):
        st.sidebar.subheader(f"ガチャ {idx + 1}")
        st.sidebar.write(f"ことわざ名: {word['ことわざ']}")
        st.sidebar.write(f"レア度: {word['レア度']}")