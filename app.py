import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

url = 'https://drive.google.com/uc?id=' + 'https://drive.google.com/file/d/1ZtQB7aJ4Z_0ocg1n9azUM7C3XV-RYoMC/view?usp=drive_link'.split('/')[-2]
SCOPES = ['https://www.googleapis.com/auth/drive']
#SERVICE_ACCOUNT_FILE = 'remedyupdate2-e2cc4272654b.json'
PARENT_FOLDER_ID = "1yVLvSlfA830BjWOfCT_OxQguRe1Qj1dD"
file_id = '1ZtQB7aJ4Z_0ocg1n9azUM7C3XV-RYoMC'

SERVICE_ACCOUNT_FILE = {
  "type": st.secrets["type"],
  "project_id": st.secrets["project_id"],
  "private_key_id": st.secrets["private_key_id"],
  "private_key": st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id": st.secrets["client_id"],
  "auth_uri": st.secrets["auth_uri"],
  "token_uri": st.secrets["token_uri"],
  "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
  "client_x509_cert_url": st.secrets["client_x509_cert_url"],
  "universe_domain": st.secrets["universe_domain"]
}

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def update_file(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    media = MediaFileUpload("controle_remedios_test.csv", mimetype="text/csv")
    file = (service
          .files()
          .update(fileId=file_id,
                  media_body=media)
          .execute()
          )

def update(edf):
    edf.to_csv('controle_remedios_test.csv', index=False)
    update_file('controle_remedios_test.csv')
    st.write('Planilha base de controle atualizada!')
    load_df.clear()
    

@st.cache_data(ttl='1d')
def load_df():
    return pd.read_csv(url)


df = load_df()
edf = st.data_editor(df)
st.button('Save', on_click=update, args=(edf, ))
