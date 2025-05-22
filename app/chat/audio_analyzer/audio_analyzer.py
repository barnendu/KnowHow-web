
from datetime import datetime
from functools import reduce
from http import HTTPStatus
from itertools import chain
from json import dumps, loads
from os import linesep
from pathlib import Path
from time import sleep
from typing import Dict, List, Tuple
import uuid
from .helper import *
from .rest_helper import *
from .user_config_helper import *
from .audio_embeddings import *
from .save_transcript import *
import pprint

# This should not change unless you switch to a new version of the Speech REST API.
SPEECH_TRANSCRIPTION_PATH = "/speechtotext/v3.0/transcriptions"

# These should not change unless you switch to a new version of the Cognitive Language REST API.
SENTIMENT_ANALYSIS_PATH = "/language/:analyze-text"
SENTIMENT_ANALYSIS_QUERY = "?api-version=2022-05-01"
CONVERSATION_ANALYSIS_PATH = "language/analyze-conversations/jobs"
CONVERSATION_ANALYSIS_QUERY = "?api-version=2022-05-15-preview"
CONVERSATION_SUMMARY_MODEL_VERSION = "2022-05-15-preview"

# How long to wait while polling batch transcription and conversation analysis status.
WAIT_SECONDS = 10

class TranscriptionPhrase(object) :
    def __init__(self, id : int, text : str, itn : str, lexical : str, speaker_number : int, offset : str, offset_in_ticks : float) :
        self.id = id
        self.text = text
        self.itn = itn
        self.lexical = lexical
        self.speaker_number = speaker_number
        self.offset = offset
        self.offset_in_ticks = offset_in_ticks
        
class SentimentAnalysisResult(object) :
    def __init__(self, speaker_number : int, offset_in_ticks : float, document : Dict) :
        self.speaker_number = speaker_number
        self.offset_in_ticks = offset_in_ticks
        self.document = document

class ConversationAnalysisSummaryItem(object) :
    def __init__(self, aspect : str, summary : str) :
        self.aspect = aspect
        self.summary = summary

class ConversationAnalysisPiiItem(object) :
    def __init__(self, category : str, text : str) :
        self.category = category
        self.text = text

class ConversationAnalysisForSimpleOutput(object) :
    def __init__(self, summary : List[ConversationAnalysisSummaryItem], pii_analysis : List[List[ConversationAnalysisPiiItem]]) :
        self.summary = summary
        self.pii_analysis = pii_analysis

# This needs to be serialized to JSON, so we use a Dict instead of a class.
def get_combined_redacted_content(channel : int) -> Dict :
    return {
        "channel" : channel,
        "display" : "",
        "itn" : "",
        "lexical" : ""
    }

def create_transcription(user_config : Read_Only_Dict) -> str :
    uri = f"https://{user_config['speech_endpoint']}{SPEECH_TRANSCRIPTION_PATH}"

    # Create Transcription API JSON request sample and schema:
    # Notes:
    # - locale and displayName are required.
    # - diarizationEnabled should only be used with mono audio input.
    content = {
        "contentUrls" : [user_config["input_audio_url"]],
        "properties": {
            "diarizationEnabled": False,
            "wordLevelTimestampsEnabled": False,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        },
        "locale" : user_config["locale"],
        "displayName" : f"call_center_{datetime.now()}",
    }
    response = send_post(uri=uri, content=content, key=user_config["speech_subscription_key"], expected_status_codes=[HTTPStatus.CREATED])
    
    # Create Transcription API JSON response sample and schema:
    transcription_uri = response["json"]["self"]
    # The transcription ID is at the end of the transcription URI.
    transcription_id = transcription_uri.split("/")[-1]
    # Verify the transcription ID is a valid GUID.
    try :
        uuid.UUID(transcription_id)
        return transcription_id
    except ValueError:
        raise Exception(f"Unable to parse response from Create Transcription API:{linesep}{response['text']}")

def get_transcription_status(transcription_id : str, user_config : Read_Only_Dict) -> bool :
    uri = f"https://{user_config['speech_endpoint']}{SPEECH_TRANSCRIPTION_PATH}/{transcription_id}"
    response = send_get(uri=uri, key=user_config["speech_subscription_key"], expected_status_codes=[HTTPStatus.OK])
    if "failed" == response["json"]["status"].lower() :
        raise Exception(f"Unable to transcribe audio input. Response:{linesep}{response['text']}")
    else :
        return "succeeded" == response["json"]["status"].lower()

def wait_for_transcription(transcription_id : str, user_config : Read_Only_Dict) -> None :
    done = False
    while not done :
        print(f"Waiting {WAIT_SECONDS} seconds for transcription to complete.")
        sleep(WAIT_SECONDS)
        done = get_transcription_status(transcription_id, user_config=user_config)

def get_transcription_files(transcription_id : str, user_config : Read_Only_Dict) -> Dict :
    uri = f"https://{user_config['speech_endpoint']}{SPEECH_TRANSCRIPTION_PATH}/{transcription_id}/files"
    response = send_get(uri=uri, key=user_config["speech_subscription_key"], expected_status_codes=[HTTPStatus.OK])
    return response["json"]

def get_transcription_uri(transcription_files : Dict, user_config : Read_Only_Dict) -> str :
    # Get Transcription Files JSON response sample and schema:
    value = next(filter(lambda value: "transcription" == value["kind"].lower(), transcription_files["values"]), None)    
    if value is None :
        raise Exception (f"Unable to parse response from Get Transcription Files API:{linesep}{transcription_files['text']}")
    return value["links"]["contentUrl"]

def get_transcription(transcription_uri : str) -> Dict :
    response = send_get(uri=transcription_uri, key="", expected_status_codes=[HTTPStatus.OK])
    return response["json"]

def get_transcription_phrases(transcription : Dict, user_config : Read_Only_Dict) -> List[TranscriptionPhrase] :
    def helper(id_and_phrase : Tuple[int, Dict]) -> TranscriptionPhrase :
        (id, phrase) = id_and_phrase
        best = phrase["nBest"][0]
        speaker_number : int
        # If the user specified stereo audio, and therefore we turned off diarization,
        # only the channel property is present.
        # Note: Channels are numbered from 0. Speakers are numbered from 1.
        if "speaker" in phrase :
            speaker_number = phrase["speaker"] - 1
        elif "channel" in phrase :
            speaker_number = phrase["channel"]
        else :
            raise Exception(f"nBest item contains neither channel nor speaker attribute.{linesep}{best}")
        return TranscriptionPhrase(id, best["display"], best["itn"], best["lexical"], speaker_number, phrase["offset"], phrase["offsetInTicks"])
    # For stereo audio, the phrases are sorted by channel number, so resort them by offset.
    return list(map(helper, enumerate(transcription["recognizedPhrases"])))

def delete_transcription(transcription_id : str, user_config : Read_Only_Dict) -> None :
    uri = f"https://{user_config['speech_endpoint']}{SPEECH_TRANSCRIPTION_PATH}/{transcription_id}"
    send_delete(uri=uri, key=user_config["speech_subscription_key"], expected_status_codes=[HTTPStatus.NO_CONTENT])

def get_sentiments_helper(documents : List[Dict], user_config : Read_Only_Dict) -> Dict :
    uri = f"https://{user_config['language_endpoint']}{SENTIMENT_ANALYSIS_PATH}{SENTIMENT_ANALYSIS_QUERY}"
    content = {
        "kind" : "SentimentAnalysis",
        "analysisInput" : { "documents" : documents },
    }
    response = send_post(uri = uri, content=content, key=user_config["language_subscription_key"], expected_status_codes=[HTTPStatus.OK])
    return response["json"]["results"]["documents"]

def get_sentiment_analysis(phrases : List[TranscriptionPhrase], user_config : Read_Only_Dict) -> List[SentimentAnalysisResult] :
    retval : List[SentimentAnalysisResult] = []
    # Create a map of phrase ID to phrase data so we can retrieve it later.
    phrase_data : Dict = {}
    # Convert each transcription phrase to a "document" as expected by the sentiment analysis REST API.
    # Include a counter to use as a document ID.
    documents : List[Dict] = []
    for phrase in phrases :
        phrase_data[phrase.id] = (phrase.speaker_number, phrase.offset_in_ticks)
        documents.append({
            "id" : phrase.id,
            "language" : user_config["language"],
            "text" : phrase.text,
        })
    # We can only analyze sentiment for 10 documents per request.
    # Get the sentiments for each chunk of documents.
    result_chunks = list(map(lambda xs : get_sentiments_helper(xs, user_config), chunk (documents, 10)))
    for result_chunk in result_chunks :
        for document in result_chunk :
            retval.append(SentimentAnalysisResult(phrase_data[int(document["id"])][0], phrase_data[int(document["id"])][1], document))
    return retval

def get_sentiments_for_simple_output(sentiment_analysis_results : List[SentimentAnalysisResult]) -> List[str] :
    sorted_by_offset = sorted(sentiment_analysis_results, key=lambda x : x.offset_in_ticks)
    return list(map(lambda result : result.document["sentiment"], sorted_by_offset))

def get_sentiment_confidence_scores(sentiment_analysis_results : List[SentimentAnalysisResult]) -> List[Dict] :
    sorted_by_offset = sorted(sentiment_analysis_results, key=lambda x : x.offset_in_ticks)
    return list(map(lambda result : result.document["confidenceScores"], sorted_by_offset))

def merge_sentiment_confidence_scores_into_transcription(transcription : Dict, sentiment_confidence_scores : List[Dict]) -> Dict :
    for id, phrase in enumerate(transcription["recognizedPhrases"]) :
        for best_item in phrase["nBest"] :
            best_item["sentiment"] = sentiment_confidence_scores[id]
    return transcription

def transcription_phrases_to_conversation_items(phrases : List[TranscriptionPhrase]) -> List[Dict] :
    return [{
        "id" : phrase.id,
        "text" : phrase.text,
        "itn" : phrase.itn,
        "lexical" : phrase.lexical,
        # The first person to speak is probably the agent.
        "role" : "Agent" if 0 == phrase.speaker_number else "Customer",
        "participantId" : phrase.speaker_number
    } for phrase in phrases]

def format_text(text, max_chars_per_line=120):
    # Split the text into words
    words = text.split()
    # Initialize an empty list to store formatted lines
    formatted_lines = []
    # Initialize a temporary line
    current_line = ''
    # Iterate over each word
    for word in words:
        # Check if adding the word to the current line would exceed the maximum characters per line
        if len(current_line) + len(word) > max_chars_per_line:
            # If so, add the current line to the formatted lines list and start a new line
            formatted_lines.append(current_line.strip())
            current_line = ''
        # Add the word to the current line
        current_line += word + ' '
    # Add the last line to the formatted lines list
    if current_line:
        formatted_lines.append(current_line.strip())
    # Join the formatted lines back into a single string
    formatted_text = '\n'.join(formatted_lines)
    return formatted_text

def print_full_output(output_file_path : str, transcription : Dict, sentiment_confidence_scores : List[Dict], phrases : List[TranscriptionPhrase], document_id : str) -> None :

    final_transcription = merge_sentiment_confidence_scores_into_transcription(transcription, sentiment_confidence_scores)
    pprint.pp(final_transcription)
    with open(output_file_path, mode = "w", newline = "") as f :
        f.write(format_text(final_transcription["combinedRecognizedPhrases"][0]["display"]))
    audio_embeddings(output_file_path, document_id)
    sent_transcript_to_blob_storage(output_file_path)

def run_audio_analyzer(input_file_path:str, output_file_path:str, document_id:str) -> None :
    user_config = user_config_from_args(input_file_path, output_file_path )
    transcription : Dict
    transcription_id : str
    if user_config["input_audio_url"] is not None :
        transcription_id = create_transcription(user_config)
        wait_for_transcription(transcription_id, user_config)
        print(f"Transcription ID: {transcription_id}")
        transcription_files = get_transcription_files(transcription_id, user_config)
        transcription_uri = get_transcription_uri(transcription_files, user_config)
        print(f"Transcription URI: {transcription_uri}")
        transcription = get_transcription(transcription_uri)
    else :
        raise Exception(f"Missing input audio URL.{linesep}")
    # For stereo audio, the phrases are sorted by channel number, so resort them by offset.
    transcription["recognizedPhrases"] = sorted(transcription["recognizedPhrases"], key=lambda phrase : phrase["offsetInTicks"])
    phrases = get_transcription_phrases(transcription, user_config)
    sentiment_analysis_results = get_sentiment_analysis(phrases, user_config)
    sentiment_confidence_scores = get_sentiment_confidence_scores(sentiment_analysis_results)
    if user_config["output_file_path"] is not None :
        print_full_output(user_config["output_file_path"], transcription, sentiment_confidence_scores, phrases, document_id)


