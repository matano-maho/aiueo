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
owndamage = 0

# ガチャ結果の履歴を保持するリスト
if 'history' not in st.session_state:
    st.session_state.history = []

if 'selected_word' not in st.session_state:
    st.session_state.selected_word = None

if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False

if 'point1' not in st.session_state:
    st.session_state.point = 0

if 'point2' not in st.session_state:
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

    user_input = st.text_input("ことわざを入力してください(ひらがなでお願いします):")

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
                owndamage = np.random.randint(10,30)
                st.session_state.point1 -= damage
                st.session_state.point2 -= owndamage
                st.session_state.last_rarity = rarity
                st.session_state.is_answered = True
            else:
                st.error("違います。")
                st.write('正解は' + st.session_state.selected_word['ことわざ'] + 'です')
                owndamage = np.random.randint(10,30)
                st.session_state.point2 -= owndamage
                st.session_state.is_answered = True
        else:
            st.warning("正誤判定はすでに行われました。新しいガチャを引いてください。")

    if damage == -1:
        damagecoment = ""
    elif damage == 0:
        damagecoment = '残念！あなたはダメージを与えられなかった'
    elif damage <= 10:
        damagecoment = '相手に'+damage+'ダメージ！かすり傷を与えた'
    elif damage <= 35:
        damagecoment = '相手に'+damage+'ダメージ！そこそこのダメージを与えた'
    elif damage <= 45:
        damagecoment = '相手に'+damage+'ダメージ！大ダメージを与えた'
    
    st.write(damagecoment)
    st.write(f"相手の体力: {st.session_state.point1}")

    st.write('自分は'+owndamage+'のダメージを受けた')

    if st.session_state.point1 <= 0:
        st.write('敵を倒した！')
        st.session_state.point1 = 150


