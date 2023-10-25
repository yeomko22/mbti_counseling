import streamlit as st
from supabase import create_client


@st.cache_resource
def init_supabase():
    supabase_client = create_client(
        supabase_url=st.secrets["SUPABASE_URL"],
        supabase_key=st.secrets["SUPABASE_KEY"]
    )
    return supabase_client


def write_data(target_table, data):
    supabase_client = init_supabase()
    supabase_client.table(target_table).insert(data).execute()


def read_page(target_table, last_id=None, pagesize=10):
    supabase_client = init_supabase()
    response = (supabase_client.table(target_table)
                .select("*", count="exact")
                .lt("id", last_id)
                .order("id", desc=True)
                .limit(pagesize)
                .execute())
    return response.data


def count_records(target_table):
    supabase_client = init_supabase()
    response = (supabase_client.table(target_table)
                .select("*", count="exact")
                .execute())
    return response.count
