import streamlit as st
import sounddevice as sd
import soundfile as sf

def record_audio(file_name, duration, samplerate=44100, channels=2):
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    sf.write(file_name, recording, samplerate)

def main():
    st.title("Audio Recorder")

    duration = st.slider("Recording Duration (seconds)", min_value=1, max_value=30, value=5)
    file_name = st.text_input("Enter File Name", value="recorded_audio.wav")

    if st.button("Record"):
        st.write("Recording...")
        record_audio(file_name, duration)
        st.write(f"Recording saved as {file_name}")

if __name__ == "__main__":
    main()
