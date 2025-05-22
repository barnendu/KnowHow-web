import os
from .helper import *


# This should not change unless the Speech REST API changes.
PARTIAL_SPEECH_ENDPOINT = ".api.cognitive.microsoft.com";

def user_config_from_args(input_audio_url : str, output_file_path: str ) -> Read_Only_Dict :
    speech_subscription_key = os.getenv("SPEECH_KEY")
    speech_region = os.getenv("SPEECH_REGION")
    language_subscription_key = os.getenv("LANGUAGE_KEY")
    language_endpoint = os.getenv("LANGUAGE_ENDPOINT")
    language_endpoint = language_endpoint.replace("https://", "")
    language = "en"
    locale = "en-US"

    return Read_Only_Dict({
        "use_stereo_audio" : True,
        "language" : language,
        "locale" : locale,
        "input_audio_url" : input_audio_url,
        "output_file_path" : output_file_path,
        "speech_subscription_key" : speech_subscription_key,
        "speech_endpoint" : f"{speech_region}{PARTIAL_SPEECH_ENDPOINT}",
        "language_subscription_key" : language_subscription_key,
        "language_endpoint" : language_endpoint,
    })