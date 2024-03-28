import streamlit as st
import pandas as pd

# 指定されたDataFrameの特定の列が空の行をチェックする関数
def check_empty(df, column_name, warning_number, entity_name):
    """
    df: チェックするDataFrame
    column_name: 空かどうかをチェックする列の名前
    warning_number: 警告メッセージに表示する番号
    entity_name: 警告メッセージに含めるエンティティの名前
    """
    # 空の値を持つ行のインデックスを格納するリスト
    empty_indices = []
    # df の各行を確認
    for index, row in df.iterrows():
        if row[column_name] == "":
            # インデックスをリストに追加（人間が読むために1を加えている）
            empty_indices.append(index + 1)
    # 空の値がある場合、警告を表示
    if empty_indices:
        indices_text = ', '.join(map(str, empty_indices)) # 修正部分
        st.warning(f"{warning_number}.{entity_name}の入力：{entity_name} {indices_text}を入力してください。")
        return 0
    else:
        return 1

