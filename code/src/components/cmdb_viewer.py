import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from services.data_service import DataService

class CMDBViewer:
    def __init__(self):
        self.data_service = DataService()

    def render(self):
        st.header("CMDB & Dependencies")

        # Load CMDB and network dependency data
        cmdb_df = self.data_service.load_dataset("cmdb")
        network_df = self.data_service.load_dataset("network")

        # Create tabs for different views
        tabs = st.tabs(["CI Details", "Network Dependencies", "Relationship Graph"])
        
        with tabs[0]:
            self.render_ci_details(cmdb_df)
        
        with tabs[1]:
            self.render_network_dependencies(network_df)
        
        with tabs[2]:
            self.render_relationship_graph(cmdb_df, network_df)

    def render_ci_details(self, cmdb_df):
        st.subheader("Configuration Items")
        
        # Filter and search options
        ci_type = st.selectbox("CI Type", cmdb_df['type'].unique())
        filtered_cis = cmdb_df[cmdb_df['type'] == ci_type]
        
        # Display CI details
        st.dataframe(filtered_cis, use_container_width=True)

    def render_network_dependencies(self, network_df):
        st.subheader("Network Dependencies")
        
        # Create network graph
        G = nx.from_pandas_edgelist(network_df, 'source', 'target')
        
        # Visualize using Plotly
        pos = nx.spring_layout(G)
        self.plot_network_graph(G, pos) 