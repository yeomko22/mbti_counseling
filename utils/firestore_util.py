from datetime import datetime, timezone

import firebase_admin
import streamlit as st
from firebase_admin.credentials import Certificate
from firebase_admin import firestore


@st.cache_resource
def init_filestore_connection():
    if not firebase_admin._apps:
        cred = Certificate(dict(st.secrets["FIRESTORE_KEY"]))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    ref = db.collection(st.secrets.FIRESTORE_KEY.project_id)
    return ref


def save_result(prompt: str, generated_text: str) -> str:
    firestore_ref = init_filestore_connection()
    doc = firestore_ref.document()
    doc.set(
        {
            "env": st.secrets["ENV"],
            "created_at": datetime.now(timezone.utc),
            "prompt": prompt,
            "generated_text": generated_text
        }
    )
    return doc.id
