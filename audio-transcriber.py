import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_format(input_file, output_file, target_format="wav"):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format=target_format)

def transcribe_audio(file_path, langauge="ko-KR"):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, langauge=langauge)
            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

input_file = input("Enter the path of the audio file: ")
output_file = input_file.split('.')[0] + ".wav"

convert_audio_format(input_file, output_file)

transcribed_text = transcribe_audio(output_file)

if transcribed_text:
    print("Transcription:")
    print(transcribed_text)
else:
    print("Transcription failed.")