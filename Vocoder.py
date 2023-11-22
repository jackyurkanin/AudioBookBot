from elevenlabs import voices, generate
from elevenlabs import clone, generate, play,  set_api_key
from API_KEYS import API_KEY



set_api_key(API_KEY)

# use already exiting voices
voices = voices()
audio = generate(text="Hello there!", voice=voices[-2])


# make a voice to use


# voice = clone(
#     name="Alex",
#     files=["mogranFreemanAudio/sample_0.mp3", "mogranFreemanAudio/sample_1.mp3", "mogranFreemanAudio/sample_2.mp3"],
# )

# audio = generate(text="Hi! I'm a cloned voice!", voice=voice)

play(audio)
