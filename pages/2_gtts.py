# lib gtts - google text to speech
# usar ffmpeg para executar o audio (pode ser qqer programa, mas o ffmpeg vai via cmd)
# para isso, via cmd precisamos da lib os
import streamlit as st
import os
from gtts import gTTS

st.title('GTTS - Google Text To Speech')

input_texto = st.text_input('Digite o texto', value='')
bt_go = st.button('falar!')

if input_texto and bt_go:
    my_audio = gTTS(text=input_texto, lang='pt')
    my_audio.save('audio.mp3')
    # executando o arquivo
    os.system('ffplay -autoexit -nodisp audio.mp3')
    st.write(
        f'Texto para speech *{input_texto}* foi salvo como audio.mp3 e removido após speech')
    os.unlink('audio.mp3')
