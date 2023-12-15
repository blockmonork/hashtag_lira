import streamlit as st

# para a pagina ocupar toda a area central
st.set_page_config(page_title='home', layout='wide')

st.markdown('''
            # Multi testes
            streamlit com várias paginas.
            ''')


# teste pra classe mysql-database
comentario = '''
campos = []
valores = []
sql = ''
for i in range(1, 11):
    campos.append('campo' + str(i))
    valores.append(str(i))
def extract(val):
    r = '';
    for i in val:
        r += str(i) + ','
    return r[:len(r)-1]
sql = 'insert into porra ('+ extract(campos) +') values ( '+ extract(valores) +' ) '
print(sql)
'''
