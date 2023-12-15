import streamlit as st
from fafm.my_pyautogui import *

au = MyAutoGui()

st.title('My pyautogui - automatização')

col1, col2 = st.columns(2)

open_terminal = col1.button('abrir terminal')

if open_terminal:
    au.open_terminal()

open_browser = col2.button('abrir navegador firefox')

if open_browser:
    au.start_application('firefox')

the_url = st.text_input('URL')
go_to_url = st.button('abrir firefox e ir para URL informada')

if go_to_url:
    if the_url != '':
        st.empty()
        au.go_to_url(url=the_url, browser='firefox', delay=.5)
    else:
        st.warning('informe a URL')


funcionalidade_todo = '''
email_to = st.text_input('email para')
email_msg = st.text_area('texto email')
email = st.button('enviar email')

if email:
    if not email_to or not email_msg:
        st.warning('destinatário e texto do email são obrigatórios')
    else:
        au.write_email('blockmonork', email_to, 'Teste email python', email_msg)
        st.empty()
        st.success('email enviado')
'''
