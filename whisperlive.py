import whisper
import torch
import tkinter as tk
import pyaudio
import numpy as np
import threading
import time

#Settings (make SURE these are correct, especially model_name)
model_name = "medium" #tiny, base, small(3.2+ GB vram), medium(6+ GB vram), large-v2(11+ GB vram)
language = "Japanese" #language of the audio to translate

with torch.inference_mode():
    model = whisper.load_model(model_name)

def ProcessAudio(mel):
    with torch.inference_mode():
        # decode the audio
        options = whisper.DecodingOptions("translate", language)
        result = whisper.decode(model, mel, options)

    return result.text

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Whisper Live Translator")
        self.devices, self.device_indexes = self.get_devices()
        self.device_var = tk.StringVar(value=self.devices[0])
        self.seconds_var = tk.StringVar()
        self.samples_var = tk.StringVar()
        self.sample_rate = 16000
        self.show = True
        self.out_stream = False
        self.to_listen = tk.IntVar()
        self.create_widgets()

    def on_closing(self):
        if(self.recording):
            self.recording = False
        

    def get_devices(self):
        p = pyaudio.PyAudio()
        devices = []
        indexes = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if (device_info["maxInputChannels"] > 0) and (device_info["hostApi"] == 0):
                devices.append(device_info["name"])
                indexes.append(i)
        p.terminate()
        return devices, indexes

    def toggle_display(self, wset):
        if(self.show):
            self.show = False
            self.master.attributes('-alpha',0.5)
            for w in wset:
                w.grid_remove()
        else:
            self.show = True
            self.master.attributes('-alpha',1.0)
            for w in wset:
                w.grid()


    def create_widgets(self):
        f1 = tk.Frame(self.master)
        listencb = tk.Checkbutton(f1, text="Listen (Not Recommended)", variable=self.to_listen)
        self.widget_set = [
            tk.Label(f1, text="Device:  "),
            tk.OptionMenu(f1, self.device_var, *self.devices),

            tk.Label(f1, text="Seconds/Sample:  "),
            tk.Entry(f1, textvariable=self.seconds_var),

            tk.Label(f1, text="Buffer Size: "),
            tk.Entry(f1, textvariable=self.samples_var),

            tk.Button(f1, text="Start", command=self.start_recording),
            tk.Button(f1, text="Stop", command=self.stop_recording),
            listencb,
            f1
        ]
        for i in range(len(self.widget_set)):
            self.widget_set[i].grid(row=i//2, column=i%2, sticky="W")

        #special position for listen CB
        listencb.grid(row=0, column=3, sticky="W")

        f1.grid(row=0, column=0, sticky="W")
        tk.Button(self.master, text="Toggle Interface", command=lambda: self.toggle_display(self.widget_set)).grid(row=2, column=0, sticky="W")
        self.output_text = tk.Text(self.master, height=5, width=40, font=("Helvetica", 32))
        self.output_text.grid(row=3, column=0, columnspan=3)
        self.seconds_var.set(1)
        self.samples_var.set(30)

    def start_recording(self):
        #self.ffmpeg = subprocess.Popen(self.ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.p = pyaudio.PyAudio()
        self.seconds = float(self.seconds_var.get())
        self.samples = float(self.samples_var.get())
        self.stream = self.p.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=self.sample_rate,
                                input=True,
                                input_device_index=self.device_indexes[self.devices.index(self.device_var.get())],
                                frames_per_buffer=int(self.sample_rate * self.seconds))
        self.recording = True
        self.buffer_ready = False
        self.buffer_init = True
        self.buffer_samples = 0
        self.rolling_buffer = np.zeros(int(self.sample_rate * self.seconds * self.samples), dtype=np.float32)
        self.stream.start_stream()
        self.t_buffer = threading.Thread(target=self.save_audio_to_buffer, args=())
        self.t_buffer.start()
        self.t_translate = threading.Thread(target=self.translate, args=())
        self.t_translate.start()
        print("Translation Started")

    def save_audio_to_buffer(self):
        while self.recording:
            data = self.stream.read(int(self.sample_rate * self.seconds))
            if(self.to_listen.get()):
                if(self.out_stream):
                    self.out_stream.write(data)
                else:
                    self.out_stream = self.p.open(format=pyaudio.paInt16,
                                            channels=1,
                                            rate=16000,
                                            output=True)
            data = np.frombuffer(data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
            self.rolling_buffer = np.roll(self.rolling_buffer, -len(data))
            self.rolling_buffer[-len(data):] = data
            if (self.buffer_samples >= self.samples):
                #make log-Mel spectrogram
                audio = whisper.pad_or_trim(self.rolling_buffer)
                self.mel = whisper.log_mel_spectrogram(audio).to(model.device)
                self.buffer_ready = True
                self.buffer_init = False
            else:
                self.buffer_samples += 1

        #clean up streams etc
        self.t_translate.join()
        self.stream.stop_stream()
        self.stream.close()
        self.out_stream.stop_stream()
        self.out_stream.close()
        self.out_stream = False
        self.p.terminate()
        print("Translation Stopped")
        return

    def translate(self):
        while self.recording:
            if (self.buffer_ready):
                output_text = ProcessAudio(self.mel)
                self.buffer_ready = False
            elif (self.buffer_init):
                output_text = f"Filling Buffer... {self.buffer_samples}/{int(self.samples)}"
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output_text[-150:])
            self.output_text.config(state=tk.DISABLED)
            time.sleep(0.5)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Translation Stopped")
        self.output_text.config(state=tk.DISABLED)
        return

    def stop_recording(self):
        if(self.recording):
            self.recording = False

root = tk.Tk()
app = App(root)
root.mainloop()