import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os, ffmpeg

def convert_mp4_to_wav(input_file, output_file):
    print("Converting mp4 to wav...")
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream)
    print("Conversion completed.")

def audio_volume_normalizer(input_file, output_file):
    print("Normalizing audio volume...")
    audio = AudioSegment.from_file(input_file)
    print("Audio dBFS:", audio.dBFS)
    while audio.dBFS < -10:
        audio = audio.apply_gain(+1)
    processed_audio = audio.apply_gain(+1)
    print("Processed audio dBFS:", processed_audio.dBFS)
    processed_audio.export(output_file, format="wav")
    print("Normalization completed.")

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
if input_file.split(".")[-1] == "mp4":
    output_file = input_file.replace(".mp4", ".wav")
    convert_mp4_to_wav(input_file, output_file)
    input_file = output_file

audio_volume_normalizer(input_file, "normalized-audio.wav")
# Stop here until enter key is pressed
input("Press Enter to continue...")

chunks = split_audio("normalized-audio.wav")
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