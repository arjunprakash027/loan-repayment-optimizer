import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dummy Page Two", layout="wide")

st.title("Dummy Page Two")

st.markdown("This is the second dummy page. More features to come!")

st.subheader("More Sample Inputs")
options = ["Option A", "Option B", "Option C"]
select_box_val = st.selectbox("Choose an option", options)

slider_val = st.slider("Select a range", 0, 100, (25, 75))

st.text_area("Enter multi-line text", height=150, placeholder="Your thoughts here...")

# Example of a dummy dataframe
st.subheader("Sample Data Display")
sample_df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': [10, 20, 30, 40],
    'Column 3': ['A', 'B', 'C', 'D']
})
st.dataframe(sample_df, use_container_width=True)

st.write(f"Selected option: {select_box_val}")
st.write(f"Slider range: {slider_val}")
