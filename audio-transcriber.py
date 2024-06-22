import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_format(input_file, output_file, target_format="wav"):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format=target_format)

input_file = input("Enter the path of the audio file: ")
output_file = input_file.split('.')[0] + ".wav"

convert_audio_format(input_file, output_file)