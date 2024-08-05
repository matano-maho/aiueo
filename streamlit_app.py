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

# ガチャ結果の履歴を保持するリスト
if 'history' not in st.session_state:
    st.session_state.history = []

if 'selected_word' not in st.session_state:
    st.session_state.selected_word = None

if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False

if 'point1' not in st.session_state:
    st.session_state.point1 = 150

if 'point2' not in st.session_state:
    st.session_state.point2 = 150

if 'last_rarity' not in st.session_state:
    st.session_state.last_rarity = None

if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# タイトルと説明
st.title('ことわざバトル')
st.write('レアリティの高い、答えるのが難しいことわざガチャを引くことで相手に高いダメージを与えられます！ガチャを引くごとに、相手からダメージを受けるので注意！')

damage = -1
owndamage = 0

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
# ガチャボタンの処理
with col1:
    if st.button('回復ガチャを引く！'):
        subset_df = words_df[words_df['レア度'] == 'N']
        selected_word = subset_df.sample().iloc[0]

        st.session_state.selected_word = selected_word
        st.session_state.display_meaning = False
        st.session_state.history.append(selected_word)
        owndamage = np.random.randint(10, 20)
        st.session_state.point2 += owndamage
        st.session_state.is_answered = False
        st.session_state.user_input = ""

with col2:
    if st.button('ノーマルガチャを引く！'):
        subset_df = words_df[words_df['レア度'] == 'R']
        selected_word = subset_df.sample().iloc[0]

        st.session_state.selected_word = selected_word
        st.session_state.display_meaning = False
        st.session_state.history.append(selected_word)
        owndamage = np.random.randint(10, 30)
        st.session_state.point2 -= owndamage
        st.session_state.is_answered = False
        st.session_state.user_input = ""

with col3:
    if st.button('レアガチャを引く！'):
        subset_df = words_df[words_df['レア度'] == 'SR']
        selected_word = subset_df.sample().iloc[0]

        st.session_state.selected_word = selected_word
        st.session_state.display_meaning = False
        st.session_state.history.append(selected_word)
        owndamage = np.random.randint(10, 25)
        st.session_state.point2 -= owndamage
        st.session_state.is_answered = False
        st.session_state.user_input = ""

with col4:
    if st.button('スーパーレアガチャを引く！'):
        subset_df = words_df[words_df['レア度'] == 'SSR']
        selected_word = subset_df.sample().iloc[0]

        st.session_state.selected_word = selected_word
        st.session_state.display_meaning = False
        st.session_state.history.append(selected_word)
        owndamage = np.random.randint(10, 25)
        st.session_state.point2 -= owndamage
        st.session_state.is_answered = False
        st.session_state.user_input = ""

# ユーザーが選択したことわざの意味を表示
if st.session_state.selected_word is not None:
    st.header(f"意味: {st.session_state.selected_word['意味']}")

    user_input = st.text_input("ことわざを入力してください(ひらがなでお願いします)", value=st.session_state.user_input, key='user_input_key')

    if st.button('正誤判定をする'):
        if not st.session_state.is_answered:
            if user_input == st.session_state.selected_word['ことわざの読み方']:
                st.success("正解です！")
                rarity = st.session_state.selected_word['レア度']
                if rarity == 'N':
                    damage = -1
                elif rarity == 'R':
                    damage = np.random.randint(0, 25)
                elif rarity == 'SR':
                    damage = np.random.randint(20, 45)
                elif rarity == 'SSR':
                    damage = np.random.randint(40, 55)
                
                st.session_state.last_rarity = rarity
                st.session_state.is_answered = True
            else:
                st.error("違います。")
                st.write('正解は' + st.session_state.selected_word['ことわざ'] + 'です')
                rarity = st.session_state.selected_word['レア度']
                if rarity == 'N':
                    owndamage = np.random.randint(26, 50)
                    st.session_state.point2 -= owndamage
                else:
                    owndamage = np.random.randint(20, 50)
                    st.session_state.point2 -= owndamage
                st.session_state.is_answered = True

        else:
            st.warning("正誤判定はすでに行われました。新しいガチャを引いてください。")

# ダメージコメントの作成
damagecoment = ""
if damage == -1:
    damagecoment = ""
elif damage == 0:
    damagecoment = '残念！あなたはダメージを与えられなかった'
    st.session_state.point1 -= damage
elif damage <= 10:
    damagecoment = '相手に' + str(damage) + 'ダメージ！かすり傷を与えた'
    st.session_state.point1 -= damage
elif damage <= 35:
    damagecoment = '相手に' + str(damage) + 'ダメージ！そこそこのダメージを与えた'
    st.session_state.point1 -= damage
elif damage <= 45:
    damagecoment = '相手に' + str(damage) + 'ダメージ！大ダメージを与えた'
    st.session_state.point1 -= damage
    
st.write(damagecoment)
st.write(f"相手の体力: {st.session_state.point1}")

# 自分の体力に関する表示
if st.session_state.selected_word is not None:
    rarity = st.session_state.selected_word['レア度']
    if rarity == 'N':
        if owndamage >= 26:
            st.write('自分は' + str(owndamage) + 'の大ダメージを受けた...')
        elif owndamage > 0:
            st.write('自分は' + str(owndamage) + '回復した')
    else:
        st.write('自分は' + str(owndamage) + 'ダメージを受けた')

st.write(f"自分の体力: {st.session_state.point2}")

# 勝敗の判定
if st.session_state.point1 <= 0:
    st.write('敵を倒した！')
    st.session_state.point1 = 0
    if st.button('もう一度戦う'):
        st.session_state.point1 = 150
        st.session_state.point2 = 150

if st.session_state.point2 <= 0:
    st.write('あなたは倒れてしまった')
    st.session_state.point2 = 0
    if st.button('もう一度戦う'):
        st.session_state.point1 = 150
        st.session_state.point2 = 150

