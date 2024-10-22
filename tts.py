# -*- coding: utf-8 -*-


from google.cloud import texttospeech
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
TOKEN_PICKLE = 'token.pickle'
CREDENTIALS_JSON = 'credentials.json'  # Ensure this matches your credentials file name

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

def synthesize_speech(text, output_filename, credentials):
    # Initialize the Text-to-Speech client with credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Set the text input to be synthesized
    input_text = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("he-IL") and the SSML voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="he-IL",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Write the response to the output file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_filename}"')

# Example usage with Niqqud
text = """
בַּיּוֹם שֶׁלִּפְנֵי הָיוֹם שֶׁבּוֹ נִתְעַלָּמָה הַשֶּׁמֶשׁ, יָשְׁבוּ הָאֲנָשִׁים בְּבָתֵּיהֶם וְקָרְאוּ סְפָרִים שׁוֹנִים. הָיוּ בַּחֲצֵרוֹת הַבָּתִּים הַרְבֵּה צִפֳּרִים שֶׁשָּׁרוּ בְּקוֹלוֹת רַנָּנִים, וְהָאֲנָשִׁים הִתְעַלְּסוּ וְשָׂמְחוּ מְאֹד. בְּאֶמְצַע הָעִיר עָמְדָה מִטָּה גְּדוֹלָה וְיָפָה, שֶׁהָיְתָה מְקֻשֶּׁטֶת בְּפְרָחִים רַבִּים.

אַחַת הַנָּשִׁים, אֲשֶׁר הָיְתָה לָהּ יָלְדָּה קְטַנָּה, הִתְיָשְׁבָה לְיַד הַמִּטָּה וְהִתְחִילָה לְסַפֵּר לָהּ סִפּוּרִים מִזְּמַן עַתִּיק. הָיְתָה זֹאת תְּקוּפָה שֶׁל שָׁלוֹם וְאַהֲבָה, וְכֻלָּם הָיוּ מְסֻבִּים סָבִיב הָאֵשׁ בַּלַּיְלָה וְשָׂמְחוּ בְּיַחַד. אֲבָל בְּתוֹךְ הַלַּיְלָה, כְּשֶׁהַכֹּל שָׁקַט וְנִרְגַּע, הִשְׁתַּגְּשׁוּ גַּלִּים גְּדוֹלִים עַל הַיָּם.

בְּאוֹתוֹ רֶגַע, כְּשֶׁהַשֶּׁקֶט הָפַךְ לְרַעַשׁ גָּדוֹל, הִתְעוֹרְרוּ הָאֲנָשִׁים וְהִתְחִילוּ לְחַפֵּשׂ מַחֲסֶה. הָיְתָה רְעִידַת אֲדָמָה חֲזָקָה, וּבַתֵּי הָעִיר הִתְמוֹטְטוּ זֶה אַחַר זֶה. אֲבָל הָיְתָה תְּקוּפָה שֶׁל תִּקְוָה, וְכֻלָּם הִתְיַחֲדוּ לְחַדֵּשׁ אֶת הָעִיר וְלִבְנוֹתָהּ מֵחָדָשׁ.

כָּךְ הָיְתָה הִסְתַּיְּרוּת שֶׁל זְמַן רַבִּים, שֶׁבּוֹ נִצְּחוּ הָאֲנָשִׁים אֶת הַקֹּשִׁי וְהַיִּרְאָה, וְהֵם הִתְגַּבְּרוּ עַל כָּל הַמִּשְׁבָּרִים וְהַקּוֹשִׁי שֶׁהָיוּ לִפְנֵיהֶם. בְּאֶמְצַע הָעִיר הַמְּחֻדֶּשֶׁת, הָיְתָה מִטָּה גְּדוֹלָה וְיָפָה, מְקֻשֶּׁטֶת בְּפְרָחִים רַבִּים, וְהָאֲנָשִׁים יָשְׁבוּ סְבִיבָהּ וְשָׂמְחוּ מְאֹד.

הָיְתָה זֹאת סִפּוּרָהּ שֶׁל הָעִיר, סִפּוּר שֶׁל נִצָּחוֹן וְתִקְוָה, שֶׁכָּל דּוֹר וָדוֹר מְסַפֵּר וּמְשַׁמֵּר בְּזִכְרוֹנוֹ. וְכָךְ הָיְתָה הָעִיר מְשַׁמֶּרֶת אֶת הָרוּחַ שֶׁלָּהּ, בְּתוֹךְ כָּל הַשָּׁנוֹת וְהַדּוֹרוֹת, וּמְשַׁמֶּרֶת אֶת הַתִּקְוָה וְהָאַהֲבָה שֶׁהָיְתָה בָּהּ מֵהַתְּחִלָּה.
"""

output_filename = "output.mp3"

# Authenticate and obtain credentials
credentials = authenticate()

# Synthesize speech
synthesize_speech(text, output_filename, credentials)
