import streamlit as st

st.set_page_config("Unlimited forms demo")

if "list" not in st.session_state:
    st.session_state.list = [0]

st.info("Sums the numbers entered.")

with st.form("form"):
    print("form")
    st_input_area = st.container()
    st_add_button_area = st.container()

    if st_add_button_area.form_submit_button("ADD FORM"):
        st.session_state.list.append(0)

    if st_add_button_area.form_submit_button("REMOVE FORM"):
        del st.session_state.list[-1]

    for i in range(len(st.session_state.list)):
        st.session_state.list[i] = st_input_area.number_input(f"Value {i+1}", step=1, key=i)

    is_calc = st.form_submit_button("DONE")

if is_calc:
    sum = 0
    for _value in st.session_state.list:
        sum += _value
    st.success(f"Total: {sum}")
else:
    pass  # DO NOTHING

