import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import data_management, form_handlers, utils

st.set_page_config("Nomica")
st.title("Nomica🍻")
st.write("飲み会の傾斜計算を行うツールです。")
st.divider()


# Flagの設定
is_party = False
is_position = False
is_participant = False

# party_dfの初期化
party_data = {
    "金額": [120000, 80000]
}
data_management.initialize_dataframe("party_df", party_data)

# position_dfの初期化
position_data = {
    "役職": ["先生", "先輩"],
    "傾斜": [90, 50]
}
data_management.initialize_dataframe("position_df", position_data)

# participant_dfの初期化
participant_data = {
    "名前": ["五条", "パンダ"],
    "役職": ["先生", "先輩"]
}
data_management.initialize_dataframe("participant_df", participant_data)


st.session_state["tab_labels"] = [
    f"1.飲み会の入力", 
    f"2.役職の入力", 
    f"3.参加者の入力"
]

tab1, tab2, tab3 = st.tabs(st.session_state["tab_labels"])
with tab1:
    st.subheader("Step1：飲み会の入力")
    st.markdown("各飲み会の支払い金額を入力してください。")
    form_handlers.create_party_form()
    if '飲み会データ' in st.session_state:
        is_party=True
        st.success("飲み会を確定しました")

with tab2:
    st.subheader("Step2：役職の入力")
    st.markdown("参加者の役職と傾斜を入力してください。傾斜は5（支払いが少ない）~100（支払いが多い）の範囲で設定できます。")
    form_handlers.create_position_form()
    if '役職データ' in st.session_state:
        if utils.check_empty(st.session_state["position_df"], "役職", 2, "役職"):    
            is_position=True
            st.success("役職を確定しました")
with tab3:
    st.subheader("Step3：参加者の追加")
    st.markdown("参加者の名前とその役職を入力してください。")
    form_handlers.create_participant_form()
    if '参加者データ' in st.session_state:
        if utils.check_empty(st.session_state["participant_df"], "名前", 3, "名前"):            
            is_participant=True
            st.success("参加者を確定しました")   

tab_labels_temp = st.session_state["tab_labels"]

if not "complete_flag" in st.session_state:
    st.session_state["complete_flag"] = False
if (is_party and is_position and is_participant) or st.session_state["complete_flag"]:
    st.session_state["complete_flag"] = True
    st.divider()
    st.subheader("精算表")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.unit = st.selectbox("支払い単位", ["1000円単位", "100円単位", "10円単位", "1円単位"])
    with col3:
    # コピーするテキスト
        st.markdown("  ")
        st.markdown("  ")
        form_handlers.create_copybutton()

    form_handlers.create_worksheet()
