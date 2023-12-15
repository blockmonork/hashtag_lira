import streamlit as st
from PIL import Image
from fafm.file import File

st.title('PIL - Python Image Library')

img_upload = st.file_uploader('Enviar imagem', type=['jpg', 'png'])

st.divider()

col_1, col_w, col_h = st.columns(3)

redimensionar = col_1.checkbox('Redimensionar imagem')

img_w = col_w.slider(
    'largura', min_value=320, max_value=800, step=1, disabled=not redimensionar)
img_h = col_h.slider('altura',
                     min_value=240, max_value=600, step=1, disabled=not redimensionar)


st.divider()

marcadagua = st.checkbox('Adicionar marca d\'agua ')

c1, c2, c3 = st.columns(3)

marca_txt = c1.text_input(
    'texto marca dagua', disabled=not marcadagua, max_chars=50)

marca_cor = c2.color_picker('cor', disabled=not marcadagua)

marca_tam = c3.number_input(
    'tamanho da fonte', min_value=13, max_value=50, disabled=not marcadagua)


st.divider()

enviar = st.button('Processar')
temp_file = 'temp.png'
new_name = 'arquivo.png'
file = File(new_name)
md_txt = ''

if enviar and img_upload:
    original = Image.open(img_upload)
    original.save(temp_file)
    img = Image.open(temp_file)

    if redimensionar:
        w = img_w
        h = img_h
        alt_img = img.resize((w, h))
    else:
        original_dim = img.size
        w = original_dim[0]
        h = original_dim[1]
        alt_img = img

    alt_img.save(new_name)
    file.delete(temp_file)
    md_txt = ''

    if marcadagua:
        md_txt = 'TODO: marca d\'agua aplicada!'

    st.markdown(
        f'Arquivo **{new_name}** salvo! dimensoes ({w} x {h}) {md_txt} ')
    st.image(image=new_name, caption=new_name)
else:
    if file.exists():
        st.markdown('Arquivo salvo:')
        st.image(image=new_name, caption=new_name)
