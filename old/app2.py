import streamlit as st
import pandas as pd

st.set_page_config("Nomica")

st.title("Nomica🍻")
st.write("飲み会の傾斜計算を行うツールです。ご意見やご感想はy27-yoshida@xxx.co.jpmまで")
st.divider()
print(f"")
print(f"********** sessionの開始 **********")


# Flagの設定
is_party = False
is_position = False
is_participant = False


# party_dfの初期化
if "party_df" not in st.session_state:
    party_data = {
        "金額": [120000, 80000]
    }
    st.session_state.party_df = pd.DataFrame(party_data)
    print(f"*** party_dfの新規作成 ***")
    print(f"{st.session_state.party_df=}")

# party_dfのレコード追加関数
def add_party(index):
    for inner_index, row in st.session_state.party_df.iterrows():
        st.session_state.party_df.at[inner_index, "金額"] = st.session_state[f"amount{inner_index}"]
    st.session_state.party_df = st.session_state.party_df.append({"金額": 0}, ignore_index=True)
    print(f"*** party_dfのレコード追加 ***")
    print(f"{st.session_state.party_df=}")

# party_dfのレコード削除関数
def delete_party(index):
    for inner_index, row in st.session_state.party_df.iterrows():
        st.session_state.party_df.at[inner_index, "金額"] = st.session_state[f"amount{inner_index}"]
    st.session_state.party_df.drop(index=index, inplace=True)
    st.session_state.party_df.reset_index(drop=True, inplace=True)
    print(f"*** party_dfのindex={index}レコード削除 ***")
    print(f"{st.session_state.party_df=}")

# party_dfの入力フォーム
st.subheader("飲み会の追加")
st.markdown("各飲み会の支払い金額を入力してください。")
with st.form("飲み会"):
    for index, row in st.session_state.party_df.iterrows():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"{index+1}次会")
        with col2:
            amount_init = st.session_state.party_df.at[index, "金額"]
            st.session_state.party_df.at[index, "金額"] = st.number_input(f"金額 {index+1}", key=f"amount{index}", step=1, value=amount_init)
        with col3:
            st.form_submit_button(f"{index+1}次会を削除", args=[index], on_click=delete_party)
        
    st.form_submit_button("追加", args=[index], on_click=add_party)

    is_party = st.form_submit_button("飲み会を確定")
    print(f"*** party_dfの確定 ***")    
    print(f"{st.session_state.party_df=}")
    
    if '飲み会データ' in st.session_state:
        is_party=True
    if is_party:
        st.session_state["飲み会データ"] = 1
    

# postion_dfの初期化
if "position_df" not in st.session_state:
    position_data = {
        "役職": ["先生", "先輩"],
        "傾斜": [90, 50]
    }
    st.session_state.position_df = pd.DataFrame(position_data)    
    print(f"*** party_dfの新規作成 ***")
    print(f"{st.session_state.party_df=}")
    
# position_dfのレコード追加関数
def add_position(index):
    for inner_index, row in st.session_state.position_df.iterrows():
        st.session_state.position_df.at[inner_index, "役職"] = st.session_state[f"pos{inner_index}"]
        st.session_state.position_df.at[inner_index, "傾斜"] = st.session_state[f"inc{inner_index}"]
    st.session_state.position_df = st.session_state.position_df.append({"役職": "", "傾斜": 50}, ignore_index=True)
    print(f"*** position_dfのレコード追加 ***")
    print(f"{st.session_state.position_df=}")

# position_dfのレコード削除関数
def delete_position(index):
    for inner_index, row in st.session_state.position_df.iterrows():
        st.session_state.position_df.at[inner_index, "役職"] = st.session_state[f"pos{inner_index}"]
        st.session_state.position_df.at[inner_index, "傾斜"] = st.session_state[f"inc{inner_index}"]
    st.session_state.position_df.drop(index=index, inplace=True)
    st.session_state.position_df.reset_index(drop=True, inplace=True)
    print(f"*** position_dfのindex={index}レコード削除 ***")
    print(f"{st.session_state.position_df=}")

# position_dfの入力フォーム
if is_party:
    st.subheader("役職の追加")
    st.markdown("参加者の役職と傾斜を入力してください。（傾斜は5~100の値で設定できます。)")
    with st.form("役職"):
        for index, row in st.session_state.position_df.iterrows():
            col1, col2, col3 = st.columns(3)
            with col1:
                pos_init = st.session_state.position_df.at[index, "役職"]
                st.session_state.position_df.at[index, "役職"] = st.text_input(f"役職 {index+1}", key=f"pos{index}" , value=pos_init)
            with col2:
                incli_init = st.session_state.position_df.at[index, "傾斜"]
                incli_init = int(incli_init)
                print(f"{st.session_state.position_df=}")
                st.session_state.position_df.at[index, "傾斜"] = st.slider(f"傾斜 {index+1}", min_value=5, max_value=100, value=incli_init, step=5, key=f"inc{index}")
            with col3:
                st.form_submit_button(f"役職{index+1}を削除", args=[index], on_click=delete_position)
        
        st.form_submit_button("追加", args=[index], on_click=add_position)

        is_position = st.form_submit_button("役職を確定")
        print(f"*** position_dfの確定 ***")
        print(f"{st.session_state.position_df=}")

        if '役職データ' in st.session_state:
            is_position=True
        if is_position:
            st.session_state["役職データ"] = 1
    

# participant_dfの初期化
if "participant_df" not in st.session_state:
    participant_data = {
        "名前": ["五条","パンダ"],
        "役職": ["先生","先輩"]
    }
    st.session_state.participant_df = pd.DataFrame(participant_data)    
    print(f"*** participant_dfの新規作成 ***")
    print(f"{st.session_state.participant_df=}")

# participant_dfのレコード追加関数
def add_participant(index):
    # DataFrameの型を確認
    print(f"add_participantが呼び出される前のparticipant_dfの型: {type(st.session_state.participant_df)}")

    for inner_index, row in st.session_state.participant_df.iterrows():
        st.session_state.participant_df.at[inner_index, "名前"] = st.session_state[f"name{inner_index}"]
        st.session_state.participant_df.at[inner_index, "役職"] = st.session_state[f"par_pos{inner_index}"]
    pos_temp = st.session_state.position_df.at[0, "役職"]
    st.session_state.participant_df = st.session_state.participant_df.append({"名前": "", "役職": pos_temp}, ignore_index=True)
    print(f"*** participant_dfのレコード追加 ***")
    print(f"{st.session_state.participant_df=}")

# participant_dfのレコード削除関数
def delete_participant(index):
    for inner_index, row in st.session_state.participant_df.iterrows():
        st.session_state.participant_df.at[inner_index, "名前"] = st.session_state[f"name{inner_index}"]
        st.session_state.participant_df.at[inner_index, "役職"] = st.session_state[f"par_pos{inner_index}"]
    st.session_state.participant_df.drop(index=index, inplace=True)
    st.session_state.participant_df.reset_index(drop=True, inplace=True)
    print(f"*** participant_dfのindex={index}レコード削除 ***")
    print(f"{st.session_state.participant_df=}")

# participant_dfの入力フォーム
if is_position:
    st.subheader("参加者の追加")
    st.markdown("参加者とその役職を入力してください。")
    with st.form("参加者"):
        for index, row in st.session_state.participant_df.iterrows():
            col1, col2, col3 = st.columns(3)
            with col1:
                name_init = st.session_state.participant_df.at[index, "名前"]
                st.session_state.participant_df.at[index, "名前"] = st.text_input(f"名前 {index+1}", key=f"name{index}" , value=name_init)
            with col2:
                position_init = st.session_state.participant_df.at[index, "役職"]
                position_list = st.session_state.position_df["役職"].to_list()
                print(position_list)
                if not position_init in position_list:
                    position_index = 0
                else:
                    position_index = st.session_state.position_df["役職"].to_list().index(position_init)
                pos_list = st.session_state.position_df["役職"].to_list()
                st.session_state.participant_df.at[index, "役職"] = st.selectbox(f"役職 {index+1}", pos_list, key=f"par_pos{index}", index=position_index)
            with col3:
                st.form_submit_button(f"名前{index+1}を削除", args=[index], on_click=delete_participant)

        st.form_submit_button("追加", args=[index], on_click=add_participant)

        is_participant = st.form_submit_button("参加者を確定")
        print(f"*** participant_dfの確定 ***")
        print(f"{st.session_state.participant_df=}")

        if '参加者データ' in st.session_state:
            is_participant=True
        if is_participant:
            st.session_state["参加者データ"] = 1


# 表示用データフレーム作成関数
def calculate_display_df(party_df, position_df, participant_df_init, unit="1000円単位", attendance_df=None):
    # 役職に基づいて初期参加者データフレームを拡張
    display_df = pd.merge(participant_df_init, position_df, on="役職", how="left")

    # 各飲み会ごとの出欠を設定
    if attendance_df is None:
        for party in party_df.itertuples():
            display_df[f"{party.Index+1}次会出欠"] = True
    else:
        for party in party_df.itertuples():
            display_df[f"{party.Index+1}次会出欠"] = attendance_df[f"{party.Index+1}次会出欠"]
        

    # 支払い比率の計算
    for party in party_df.itertuples():
        total = (display_df["傾斜"] * display_df[f"{party.Index+1}次会出欠"]).sum()
        display_df[f"{party.Index+1}次会支払い比率"] = display_df["傾斜"] * display_df[f"{party.Index+1}次会出欠"] / total

    # 各飲み会の支払いの計算（丸め前）
    for party in party_df.itertuples():
        total_payment = party.金額
        display_df[f"{party.Index+1}次会_丸め前"] = display_df[f"{party.Index+1}次会支払い比率"] * total_payment

    diff_list = []

    # 各飲み会の支払いの丸めと合計計算
    for party in party_df.itertuples():
        # 丸め処理
        if unit == "1円単位":
            print("1円単位")
            display_df[f"{party.Index+1}次会（円）"] = display_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, 0)).astype(int)
        elif unit == "10円単位":
            display_df[f"{party.Index+1}次会（円）"] = display_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, -1)).astype(int)
        elif unit == "100円単位":
            display_df[f"{party.Index+1}次会（円）"] = display_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, -2)).astype(int)
        elif unit == "1000円単位":
            display_df[f"{party.Index+1}次会（円）"] = display_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, -3)).astype(int)

        # 合計金額の計算と差額表示
        total_before = party.金額
        total_after = display_df[f"{party.Index+1}次会（円）"].sum()
        diff = - total_before + total_after
        diff_list.append(diff)

    # 全飲み会の合計金額の計算
    display_df["合計"] = 0
    for party in party_df.itertuples():
        display_df["合計"] += display_df[f"{party.Index+1}次会（円）"]

    return display_df, diff_list


if is_participant:
    st.subheader("支払い金額")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.unit = st.selectbox("支払い単位", ["1000円単位", "100円単位", "10円単位", "1円単位"])
    # with col2:
    #     st.button("傾斜を広げる", on_click=adjust_slope_variance, args=[0.1])
    # with col3:
    #     st.button("傾斜を縮める", on_click=adjust_slope_variance, args=[-0.1])
    # 精算表の作成
    if "attendance_df" not in st.session_state:
        display_df, diff_list = calculate_display_df(st.session_state.party_df, st.session_state.position_df, st.session_state.participant_df, st.session_state.unit)
        st.session_state.attendance_df = pd.DataFrame()
    else:
        display_df, diff_list = calculate_display_df(st.session_state.party_df, st.session_state.position_df, st.session_state.participant_df, st.session_state.unit, st.session_state.attendance_df)

    # 表示カラムの定義
    display_col = ["名前", "役職"]
    for i in range(st.session_state.party_df.shape[0]):
        display_col += [f"{i+1}次会（円）"]
        display_col += [f"{i+1}次会出欠"]
    display_col += ["合計"]
    
    st.markdown("精算表")
    st.session_state.display_df_changed = st.data_editor(
        display_df[display_col],
        hide_index=True,
        disabled=["名前", "役職", "合計"]+[f"{i+1}次会（円）" for i in range(st.session_state.party_df.shape[0])]
        )
    

    if (st.session_state.attendance_df.equals(st.session_state.display_df_changed[[f"{i+1}次会出欠" for i in range(st.session_state.party_df.shape[0])]])) == False:
        st.session_state.attendance_df = st.session_state.display_df_changed[[f"{i+1}次会出欠" for i in range(st.session_state.party_df.shape[0])]]
        st.experimental_rerun()    
    
    for i, diff in enumerate(diff_list):
        if diff == 0:
            st.info(f"{i+1}次会：幹事の支払額と合計精算額は一致しています")
        elif diff > 0:
            st.warning(f"{i+1}次会：幹事の支払額が合計精算額よりも{diff}円多くなっています")
        elif diff < 0:
            st.warning(f"{i+1}次会：幹事の支払額よりも合計精算額の方が{-diff}円多くなっています")
            
            
    




