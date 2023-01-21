# Whisper-Live-Translator

An incredibly messy whisper interface to live translate audio from an input audio device

## Instructions

1) Install OpenAIs Whisper with pip: ```pip install git+https://github.com/openai/whisper.git```
2) Push your audio to translate through an audio device (an easy solution is something like this: https://vb-audio.com/Cable/)
3) Make sure the settings in whisperlive.py are correct(IMPORTANT), and run the application
4) Select the audio device your audio to translate is coming through from the dropdown
5) Click start to start translating
6) You can also toggle the interface durign translation, which will hide the options and make the window semi-transparent

## Additional Info
The translation process takes about 4-8 seconds depending on your hardware/model, 
  so if you use the "Listen" option the audio will be "Seconds/Sample" + 4-8 seconds ahead of the translation

If you want to use this to watch a livestream, I recommend opening 2 copies of the video.
One just to get the audio to translate, and the other to watch and listen to, on a 6ish second delay.

For a youtube live stream, you could use two seperate browsers for example.

The "Sound Mixer Options" setting in windows will let you easily set the output device, such as a virtual audio cable, for a given program

Only tested in windows, but if you use linux you should be able to figure it out pretty easily
