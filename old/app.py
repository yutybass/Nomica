import streamlit as st

# セッション状態でフォームのリストを管理。初期化がまだなら空のリストで初期化する。
if 'forms' not in st.session_state:
    st.session_state.positions = []

# フォームを追加する関数
def add_position():
    st.session_state.positions.append({'name': '', 'position': ''})

# フォームを削除する関数
def remove_position():
    if st.session_state.forms:
        st.session_state.forms.pop()


st.title("今日の天気は")
with st.form("役職"):
    for i, position in enumerate(st.session_state.positions):
        col1, col2 = st.columns(2)
        with col1:
            # 名前の入力
            position['name'] = st.text_input(f'役職 {i+1}', value=position['name'])
        with col2:
            # 役職の入力
            position['position'] = st.slider(f'傾斜 {i+1}', 5, 100, step=5)

    # フォームの内容を確定するボタン
    submitted = st.form_submit_button("確定")

# フォームの外でボタンを配置
st.button("役職の追加", on_click=add_position)
st.button("最後の役職を削除", on_click=remove_position)

if submitted:
    st.write("入力された情報：")
    for form in st.session_state.forms:
        st.write(f"名前: {form['name']}, 役職: {form['position']}")

