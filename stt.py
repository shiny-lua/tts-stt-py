# -*- coding: utf-8 -*-

import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
TOKEN_PICKLE = 'token.pickle'
CREDENTIALS_JSON = 'credentials.json'  # Ensure this matches your credentials file name
SERVICE_ACCOUNT_FILE = 'serviceKey.json'  # Replace with the correct path


def authenticate():
    creds = None
    # Check if the token.pickle file exists
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_JSON,
                scopes=['https://www.googleapis.com/auth/cloud-platform'],
                redirect_uri='http://localhost:8080/'
            )
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Explicitly set the environment variable for the service account key
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    # Explicitly set the environment variable for the service account key
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="he-IL",
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Write the transcription to a text file
    with open('textoutput.txt', 'w', encoding='utf-8') as f:
        for result in response.results:
            f.write(result.alternatives[0].transcript + '\n')
            print("Transcript: {}".format(result.alternatives[0].transcript))


# Set your variables
bucket_name = 'tomersbucket'
source_file_name = '7.ogg'
destination_blob_name = '7.ogg'
gcs_uri = f'gs://{bucket_name}/{destination_blob_name}'

# Authenticate and obtain credentials
credentials = authenticate()

# Upload the file to Google Cloud Storage
upload_blob(bucket_name, source_file_name, destination_blob_name)

# Transcribe the audio file and save the transcript to a text file
transcribe_gcs(gcs_uri)
