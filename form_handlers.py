import pandas as pd
import streamlit as st
import pyperclip
import data_management



def create_party_form():
    """飲み会の入力フォームを作成する関数"""
    with st.form("飲み会"):
        for index, row in st.session_state.party_df.iterrows():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"{index + 1}次会")
            with col2:
                amount_init = int(row["金額"])
                st.session_state.party_df.at[index, "金額"] = st.number_input(f"金額 {index + 1}", key=f"party_df_金額_{index}", step=1, value=amount_init)
            with col3:
                st.form_submit_button(f"{index+1}次会を削除", args=["party_df", index], on_click=data_management.delete_record)
        
        st.form_submit_button("追加", args=["party_df", {"金額":0}], on_click=data_management.add_record)

        is_party = st.form_submit_button("飲み会を確定")
        if is_party:
            st.session_state["飲み会データ"] = 1


def create_position_form():
    """役職の入力フォームを作成する関数"""
    with st.form("役職"):
        for index, row in st.session_state.position_df.iterrows():
            col1, col2, col3 = st.columns(3)
            with col1:
                pos_init = st.session_state.position_df.at[index, "役職"]
                st.session_state.position_df.at[index, "役職"] = st.text_input(f"役職 {index+1}", key=f"position_df_役職_{index}" , value=pos_init)
            with col2:
                incli_init = st.session_state.position_df.at[index, "傾斜"]
                incli_init = int(incli_init)
                st.session_state.position_df.at[index, "傾斜"] = st.slider(f"傾斜 {index+1}", min_value=5, max_value=100, value=incli_init, step=5, key=f"position_df_傾斜_{index}")
            with col3:
                st.form_submit_button(f"役職{index+1}を削除", args=["position_df", index], on_click=data_management.delete_record)
        
        st.form_submit_button("追加", args=["position_df", {"役職": "", "傾斜": 50}], on_click=data_management.add_record)
        is_position = st.form_submit_button("役職を確定")
        if is_position:
            st.session_state["役職データ"] = 1
            st.rerun()


def create_participant_form():
    with st.form("参加者"):
        for index, row in st.session_state.participant_df.iterrows():
            col1, col2, col3 = st.columns(3)
            with col1:
                name_init = st.session_state.participant_df.at[index, "名前"]
                st.session_state.participant_df.at[index, "名前"] = st.text_input(f"名前 {index+1}", key=f"participant_df_名前_{index}" , value=name_init)
            with col2:
                position_init = st.session_state.participant_df.at[index, "役職"]
                position_list = st.session_state.position_df["役職"].to_list()
                if not position_init in position_list:
                    position_index = 0
                else:
                    position_index = st.session_state.position_df["役職"].to_list().index(position_init)
                pos_list = st.session_state.position_df["役職"].to_list()
                st.session_state.participant_df.at[index, "役職"] = st.selectbox(f"役職 {index+1}", pos_list, key=f"participant_df_役職_{index}", index=position_index)
            with col3:
                st.form_submit_button(f"名前{index+1}を削除", args=["participant_df", index], on_click=data_management.delete_record)

        pos_temp = st.session_state.position_df.at[0, "役職"]
        st.form_submit_button("追加", args=["participant_df", {"名前": "", "役職": pos_temp}], on_click=data_management.add_record)
        is_participant = st.form_submit_button("参加者を確定")        
        if is_participant:
            st.session_state["参加者データ"] = 1
            st.rerun()

def initialize_attendance_df():
    # session_stateに出欠表がない場合は作成
    st.session_state["attendance_df"] = pd.DataFrame()
    st.session_state["attendance_df"]["名前"] = st.session_state["participant_df"]["名前"]
    for party in st.session_state["party_df"].itertuples():
        st.session_state["attendance_df"][f"{party.Index+1}次会出欠"] = True

def update_attendance_df():
    initialize_attendance_df()
    # xx次会が存在する場合、その出欠列を更新
    for party in st.session_state["party_df"].itertuples():
        if f"{party.Index+1}次会出欠" in st.session_state["worksheet_df_changed"].columns:
            # 名前がある場合、その出欠を更新
            for participant_name in st.session_state["participant_df"]["名前"]:
                if participant_name in st.session_state["worksheet_df_changed"]["名前"].values:
                    # x次会のparticipant_nameの出欠を入力
                    attendance = st.session_state["worksheet_df_changed"].loc[st.session_state["worksheet_df_changed"]["名前"]==participant_name, f"{party.Index+1}次会出欠"].values[0]
                    st.session_state["attendance_df"].loc[st.session_state["attendance_df"]["名前"]==participant_name, f"{party.Index+1}次会出欠"] = attendance

def create_copybutton():
    if st.button('精算表をコピー'):
        copy_text = st.session_state["worksheed_df"].to_markdown(index=False)
        pyperclip.copy(copy_text)

def create_worksheet():
    # 参加者dfに役職dfをマージする
    participant_df = st.session_state["participant_df"]
    position_df = st.session_state["position_df"]    
    worksheet_df = pd.merge(participant_df, position_df, on="役職", how="left")
    
    party_df = st.session_state["party_df"]
    
    ## 出欠dfがない場合は新規作成
    if "worksheet_df_changed" not in st.session_state:
        initialize_attendance_df()
    ## 出欠dfがある場合はdfに従って更新
    else:
        update_attendance_df()

    # 出欠表を元に精算表の出欠部分を更新
    for party in st.session_state["party_df"].itertuples():
        worksheet_df[f"{party.Index+1}次会出欠"] = st.session_state["attendance_df"][f"{party.Index+1}次会出欠"]
        
    # 支払い比率の計算
    for party in party_df.itertuples():
        total = (worksheet_df["傾斜"] * worksheet_df[f"{party.Index+1}次会出欠"]).sum()
        worksheet_df[f"{party.Index+1}次会支払い比率"] = worksheet_df["傾斜"] * worksheet_df[f"{party.Index+1}次会出欠"] / total
        if total == 0:
            worksheet_df[f"{party.Index+1}次会支払い比率"] = 0
    # 各飲み会の支払いの計算（丸め前）
        total_payment = party.金額
        worksheet_df[f"{party.Index+1}次会_丸め前"] = worksheet_df[f"{party.Index+1}次会支払い比率"] * total_payment

    diff_list = []

    # 各飲み会の支払いの丸めと合計計算
    for party in party_df.itertuples():
        # 丸め処理
        if st.session_state["unit"] == "1円単位":
            print("1円単位")
            worksheet_df[f"{party.Index+1}次会（円）"] = worksheet_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, 0)).astype(int)
        elif st.session_state["unit"] == "10円単位":
            worksheet_df[f"{party.Index+1}次会（円）"] = worksheet_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, -1)).astype(int)
        elif st.session_state["unit"] == "100円単位":
            worksheet_df[f"{party.Index+1}次会（円）"] = worksheet_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, -2)).astype(int)
        elif st.session_state["unit"] == "1000円単位":
            worksheet_df[f"{party.Index+1}次会（円）"] = worksheet_df[f"{party.Index+1}次会_丸め前"].apply(lambda x: round(x, -3)).astype(int)

        # 合計金額の計算と差額表示
        total_before = party.金額
        total_after = worksheet_df[f"{party.Index+1}次会（円）"].sum()
        diff = - total_before + total_after
        diff_list.append(diff)

    # 全飲み会の合計金額の計算
    worksheet_df["合計（円）"] = 0
    for party in party_df.itertuples():
        worksheet_df["合計（円）"] += worksheet_df[f"{party.Index+1}次会（円）"]
    # 表示カラムの定義
    display_col = ["名前", "役職"]
    copy_col = ["名前", "役職"]
    for i in range(st.session_state.party_df.shape[0]):
        display_col += [f"{i+1}次会（円）"]
        copy_col += [f"{i+1}次会（円）"]
        display_col += [f"{i+1}次会出欠"]
    display_col += ["合計（円）"]
    copy_col += ["合計（円）"]
    
    st.session_state["worksheed_df"] = worksheet_df[copy_col]
    st.session_state.worksheet_df_changed = st.data_editor(
        worksheet_df[display_col],
        hide_index=True,
        disabled=["名前", "役職", "合計（円）"]+[f"{i+1}次会（円）" for i in range(st.session_state.party_df.shape[0])]
        )

    # ユーザーから出欠の変更を受け付けた場合、出欠表を更新
    if (st.session_state.attendance_df[[f"{i+1}次会出欠" for i in range(st.session_state.party_df.shape[0])]].equals(st.session_state.worksheet_df_changed[[f"{i+1}次会出欠" for i in range(st.session_state.party_df.shape[0])]])) == False:
        # for party in party_df.itertuples():
        #     st.session_state["attendance_df"][f"{party.Index+1}次会出欠"] = st.session_state["work_sheet_df_changed"][f"{party.Index+1}次会出欠"]
        st.rerun()    

    for i, diff in enumerate(diff_list):
        if diff == 0:
            st.info(f"{i+1}次会：幹事の支払額と合計精算額は一致しています")
        elif diff < 0:
            st.warning(f"{i+1}次会：幹事の支払額が合計精算額よりも{-diff}円多くなっています")
        elif diff > 0:
            st.warning(f"{i+1}次会：幹事の支払額よりも合計精算額の方が{diff}円多くなっています")
            
            