import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="ことわざバトル")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_excel("ことわざ集.xlsx")
    df.columns = df.columns.str.strip()  # 列名の前後の空白を削除
    return df

words_df = load_data()
damage = -1

# ガチャ結果の履歴を保持するリスト
if 'history' not in st.session_state:
    st.session_state.history = []

if 'selected_word' not in st.session_state:
    st.session_state.selected_word = None

if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False

if 'point' not in st.session_state:
    st.session_state.point = 0

if 'last_rarity' not in st.session_state:
    st.session_state.last_rarity = None

if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False

# タイトルと説明
st.title('ことわざバトル')
st.write('ことわざをランダムに表示して、勉強をサポートします！')

if st.button('ノーマルガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'N']
    selected_word = subset_df.sample().iloc[0]

    # セッションステートに選択されたことわざを保存
    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    st.session_state.history.append(selected_word)
    st.session_state.is_answered = False

if st.button('レアガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'R']
    selected_word = subset_df.sample().iloc[0]

    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    st.session_state.history.append(selected_word)
    st.session_state.is_answered = False

if st.button('スーパーレアガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'SR']
    selected_word = subset_df.sample().iloc[0]

    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    st.session_state.history.append(selected_word)
    st.session_state.is_answered = False

if st.button('超スーパーレアガチャを引く！'):
    subset_df = words_df[words_df['レア度'] == 'SSR']
    selected_word = subset_df.sample().iloc[0]

    st.session_state.selected_word = selected_word
    st.session_state.display_meaning = False
    st.session_state.history.append(selected_word)
    st.session_state.is_answered = False

# ユーザーが選択したことわざの意味を表示
if st.session_state.selected_word is not None:
    st.header(f"意味: {st.session_state.selected_word['意味']}")

    user_input = st.text_input("ことわざを入力してください:")

    if st.button('正誤判定をする'):
        if not st.session_state.is_answered:
            if user_input == st.session_state.selected_word['ことわざの読み方']:
                st.success("正解です！")

                rarity = st.session_state.selected_word['レア度']
                if rarity == 'N':
                    damage = np.random.randint(0, 16)
                elif rarity == 'R':
                    damage = np.random.randint(10, 25)
                elif rarity == 'SR':
                    damage = np.random.randint(20, 45)
                elif rarity == 'SSR':
                    damage = np.random.randint(40, 55)

                st.session_state.point -= damage
                st.session_state.last_rarity = rarity
                st.session_state.is_answered = True
            else:
                st.error("違います。")
                st.write('正解は' + st.session_state.selected_word['ことわざ'] + 'です')
                st.session_state.is_answered = True
        else:
            st.warning("正誤判定はすでに行われました。新しいガチャを引いてください。")

    if damage == -1:
        damagecoment = st.write ()
    if damage == 0:
        damagecoment = st.write('残念！あなたはダメージを与えられなかった')
    elif damage <= 10:
        damagecoment = st.write('相手にかすり傷を与えた')
    elif damage <= 45:
        damagecoment = st.write('相手にそこそこのダメージを与えた')
    elif damage <= 55:
        damagecoment = st.write('相手に大ダメージを与えた')
    st.write(damagecoment)
    st.write(f"相手の体力: {st.session_state.point}")

    if st.session_state.point <= 0:
        st.write('敵を倒した！')
        st.session_state.point = 150

# ガチャ履歴をサイドバーに表示する
st.sidebar.title('ガチャ履歴')
if st.session_state.history:
    for idx, word in enumerate(st.session_state.history):
        st.sidebar.subheader(f"ガチャ {idx + 1}")
        st.sidebar.write(f"ことわざ名: {word['ことわざ']}")
        st.sidebar.write(f"レア度: {word['レア度']}")
