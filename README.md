# Whisper-Live-Translator

An incredibly messy whisper interface to live translate audio from an input audio device  
Requires a CUDA compatible GPU

## Instructions

1) Install pytorch with cuda support
2) Install OpenAI's Whisper through pip: ```pip install openai-whisper```
3) Push your audio to translate through an audio device (an easy solution is something like this: https://vb-audio.com/Cable/)
4) Make sure the settings in whisperlive.py are correct(IMPORTANT), and run it
5) Select the audio device your audio to translate is coming through from the dropdown
6) Click start to start translating
7) You can also toggle the interface during translation, which will hide the options and make the window semi-transparent

## Additional Info
The translation process takes about 4-8 seconds depending on your hardware/model, so if you use the "Listen" option the audio will be "Seconds/Sample" + 4-8 seconds ahead of the translation

If you want to use this to watch a livestream, I recommend opening 2 copies of the video.
One just to get the audio to translate, and the other to watch and listen to, on a 6ish second delay. For a youtube live stream, you could use two seperate browsers for example.

The "Sound Mixer Options" setting in windows will let you easily set the output device, such as a virtual audio cable, for a given program

Only tested in windows, but if you use linux you should be able to figure it out pretty easily  

If you don't know how to use python you are probably wasting your time trying to run this

## Setup help
Python version must be >=3.7,<3.11  (Only tested with 3.9 and 3.10.8)  
You may need to install additional packages like pyaudio.  
If you get the error ```RuntimeError: "slow_conv2d_cpu" not implemented for 'Half'``` then pytorch isn't using your GPU for whatever reason. Might be the wrong version of pytorch, old drivers, many things.
