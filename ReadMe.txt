Run Main.py to use the AudioBook reader class

To use a custom voice, place an at least 6s audio file of the desired voice in voiceAudio 
and change the path within line 104: self.tts.tts_to_file(text=pageText, speaker_wav="voiceAudio/YourVoiceHere.wav", language="en", output_path=file_path)

Place books to listen to in the Books Folder