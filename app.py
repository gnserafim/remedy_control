import json
import streamlit as st
import pandas as pd

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

url = 'https://drive.google.com/uc?id=' + 'https://drive.google.com/file/d/1ZtQB7aJ4Z_0ocg1n9azUM7C3XV-RYoMC/view?usp=drive_link'.split('/')[-2]
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = st.secrets['SERVICE_ACCOUNT_FILE']
PARENT_FOLDER_ID = "1yVLvSlfA830BjWOfCT_OxQguRe1Qj1dD"
file_id = '1TqXIyuyL0Knw0Dz1pCH7R_K8MIdpJpp1'

def authenticate():
    creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES) ###  from_service_account_file
    return creds

def load_file(file_id):
  
  creds = authenticate()
  service = build('drive', 'v3', credentials=creds)
  request = service.files().get_media(fileId=file_id)
  file_handle = io.BytesIO()
  downloader = MediaIoBaseDownload(file_handle, request)

  done = False
  while not done:
      status, done = downloader.next_chunk()

  file_handle.seek(0)

  return pd.read_csv(file_handle)

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
    return load_file(file_id)

df = load_df()
edf = st.data_editor(df)
st.button('Save', on_click=update, args=(edf, ))
