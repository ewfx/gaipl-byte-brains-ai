from services.data_service import DataService
import streamlit as st

def test_dataset_loading():
    data_service = DataService()
    
    datasets = ["incidents", "stack_overflow", "syslog"]
    
    for dataset_name in datasets:
        try:
            st.write(f"Loading {dataset_name}...")
            df = data_service.get_dataset(dataset_name)
            st.success(f"Successfully loaded {dataset_name}")
            st.write(f"Sample data from {dataset_name}:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error loading {dataset_name}: {str(e)}")

if __name__ == "__main__":
    st.title("Dataset Loading Test")
    test_dataset_loading() 