import streamlit as st
import pandas as pd

def initialize_dataframe(df_name, initial_data):
    """
    指定された名前のデータフレームを、指定された初期データで初期化する。
    すでにデータフレームが存在する場合は、初期化を行わない。

    Args:
        df_name (str): データフレーム名 (st.session_stateのキー)
        initial_data (dict): 初期化に使用するデータ
    """
    if df_name not in st.session_state:
        st.session_state[df_name] = pd.DataFrame(initial_data)

def add_record(df_name, new_record):
    """
    指定されたデータフレームに新規レコードを追加する。

    Args:
        df_name (str): データフレーム名 (st.session_stateのキー)
        new_record (dict): 追加するレコードの内容
    """
    # 新しいレコードを DataFrame に変換
    new_df = pd.DataFrame([new_record])
    # pd.concat を用いて既存の DataFrame と新しい DataFrame を結合
    st.session_state[df_name] = pd.concat([st.session_state[df_name], new_df], ignore_index=True)

# レコード削除関数
def delete_record(df_name, delete_index):
    """
    指定されたデータフレームから指定されたインデックスのレコードを削除する。
    ただし、データフレームのレコード数が1である場合は削除を行わない。

    Args:
        df_name (str): データフレーム名 (st.session_stateのキー)
        delete_index (int): 削除するレコードのインデックス
    """
    # DataFrame のレコード数をチェック
    if len(st.session_state[df_name]) <= 1:
        # レコード数が1以下の場合は何もしない
        return

    # 指定されたインデックスのレコードを削除
    for index, row in st.session_state[df_name].iterrows():
        for column in st.session_state[df_name].columns:
            st.session_state[df_name].at[index, column] = st.session_state[f"{df_name}_{column}_{index}"]
    st.session_state[df_name].drop(index=delete_index, inplace=True)
    st.session_state[df_name].reset_index(drop=True, inplace=True)



# レコード更新関数
def update_record(df_name, index, new_values):
    """
    指定されたデータフレームの指定されたインデックスのレコードを更新する。

    Args:
        df_name (str): データフレーム名 (st.session_stateのキー)
        index (int): 更新するレコードのインデックス
        new_values (dict): 更新するレコードの新しい値
    """
    for column, value in new_values.items():
        st.session_state[df_name].at[index, column] = value

