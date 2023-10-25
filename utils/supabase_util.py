from supabase import create_client
import streamlit as st


@st.cache_resource
def init_supabase():
    supabase_client = create_client(
        supabase_url=st.secrets["SUPABASE_URL"],
        supabase_key=st.secrets["SUPABASE_KEY"]
    )
    return supabase_client


def write_couseling(target_table, data):
    supabase_client = init_supabase()
    supabase_client.table(target_table).insert(data).execute()
