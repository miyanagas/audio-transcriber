import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def split_audio(input_file, min_silence_len=1500, silence_thresh=-30, keep_silence=500):
    audio = AudioSegment.from_file(input_file)
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=keep_silence)
    return chunks

def transcribe_audio(file_path, lang="ko"):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=lang)
            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_file = input("Enter the path of the audio file: ")

chunks = split_audio(input_file)
for i, chunk in enumerate(chunks):
    if not os.path.exists("splited-audio"):
        os.makedirs("splited-audio")
    chunk.export(f"splited-audio/chunk_{i}.wav", format="wav")
    transcribed_chunk = transcribe_audio(f"splited-audio/chunk_{i}.wav")
    if transcribed_chunk:
        print(f"Chunk {i} Transcription:")
        print(transcribed_chunk)
    else:
        print(f"Chunk {i} Transcription failed.")

print("Transcription completed.")