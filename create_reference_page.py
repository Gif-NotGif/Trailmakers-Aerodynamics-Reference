
import streamlit as st
import pandas as pd

# Load block stats from CSV
df = pd.read_csv('block_stats.csv')

# Remove 'id' and 'display_name' columns if they exist
for col in ['id', 'display_name']:
	if col in df.columns:
		df = df.drop(columns=col)

# Default sort by drag multiplier forward (descending)
if 'm_dragMultiplierForward' in df.columns:
	df = df.sort_values(by='m_dragMultiplierForward', ascending=True)

st.set_page_config(page_title="Trailmakers Aerodynamics Stats Reference", layout="wide")
st.title("Trailmakers Aerodynamics Stats Reference Page")

# Search bar
search_query = st.text_input("Search blocks", "")
if search_query:
	filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
else:
	filtered_df = df

# Multi-select for comparison
block_names = filtered_df.iloc[:,0].tolist() if not filtered_df.empty else []
selected_blocks = st.multiselect("Select blocks for comparison", block_names)


# Show filtered table without index
st.dataframe(filtered_df, hide_index=True)


# Show comparison if blocks selected
if selected_blocks:
	comparison_df = filtered_df[filtered_df.iloc[:,0].isin(selected_blocks)]
	st.subheader("Block Comparison")
	st.dataframe(comparison_df, hide_index=True)
