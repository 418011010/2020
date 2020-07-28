#-*-coding:utf-8-*-
from pydub import AudioSegment
import simpleaudio as sa


def trans_mp3_to_wav(filepath, outfile):
    song = AudioSegment.from_mp3(filepath)
    song.export(outfile, format="wav")


def playwave(filepath):
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()


# trans_mp3_to_wav("s1.mp3", "s1.wav")
# playwave("s1.wav")