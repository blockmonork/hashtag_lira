import plotly.express as px
import datetime
import pandas as pd
import streamlit as st
from fafm.database import Database
db = Database()


st.title('My classe MySQL')

st.markdown(f'database: **{db.database}**. A tabela *teste* \
    tem *{db.select("count(*) as x", "teste")[0][0]}* registros')

st.markdown(f'primeiro registro: \
    {db.select("nome", "teste", "id > 0 order by id asc limit 1")[0][0]} ')

st.markdown(f'último registro: \
    {db.select("nome", "teste", "id > 0 order by id desc limit 1")[0][0]} ')

st.divider()

st.subheader('MySQL com pandas')
# create cache
if not 'data' in st.session_state:
    tabela = pd.read_sql_query("SELECT * FROM teste", db.db, index_col='id')
    st.session_state['data'] = tabela


tabela = st.session_state['data']

exp = st.expander('Tabela', expanded=True)
exp.write(tabela)

# cadastrar/editar
# calc_idade


def get_min_date(anos=30):
    anoEmDia = anos * 365
    x = anoEmDia
    return datetime.datetime.today() - datetime.timedelta(days=x)


def get_max_date():
    return datetime.datetime.today()


def calc_idade(data_nascimento):
    str_ano = str(data_nascimento).split('-')[0]
    return int(datetime.datetime.now().year - int(str_ano))

# nome, data nascimento, vivo


def load_by_id(id):
    item = tabela.query(f'id=={id}')
    if len(item) == 0 :
        return {}
    else:
        return {
            'nome': item['nome'],
            'data_nascimento': item['data_nascimento'],
            'vivo': item['vivo']
        }



def cadastrar(nome, data_nascimento, vivo):
    # st.markdown(f'nome: {nome}, data nascimento {data_nascimento}, vivo {vivo}, idade: {calc_idade(data_nascimento)} ')
    db.insert('teste', [
        {'nome': nome},
        {'data_nascimento': str(data_nascimento)},
        {'vivo': 1 if vivo == True else 0},
        {'idade': calc_idade(data_nascimento)}
    ])
    st.success('Registro gravado!')


def editar():
    pass


st.divider()
st.subheader('Cadastrar novo')
c1, c2, c3 = st.columns(3)
with st.form(key='form_cadastrar', clear_on_submit=True):
    nome = c1.text_input('nome', max_chars=50)
    vivo = c2.checkbox('vivo')
    data_nascimento = c3.date_input(
        'data_nascimento',
        min_value=get_min_date(),
        max_value=get_max_date()
    )
    submit_btn = st.form_submit_button('salvar')
    if submit_btn:
        cadastrar(nome, data_nascimento, vivo)



st.divider()
st.subheader('Editar')
ec1, ec2, ec3, ec4 = st.columns(4)
with st.form(key='form_editar', clear_on_submit=True):
    
    reg_id = ec1.text_input('ID Registro')

    v_nome = ''
    v_vivo = ''
    v_data = get_min_date()
    go_to_editar = False
    
    if reg_id:
        x = load_by_id(reg_id)
        v_nome = x['nome']
        st.write(f'nome = { str(v_nome) }  ')
        cu = '''
        if len(x) == 0:
            st.error('registro não encontrado')
        else:
            v_nome = x['nome']
            v_vivo = x['vivo']
            v_data = x['data_nascimento']
            go_to_editar = True
        '''

        

    nome2 = ec2.text_input('nome2', max_chars=50, value=v_nome)
    vivo2 = ec3.checkbox('vivo2', value=v_vivo)
    data_nascimento2 = ec4.date_input(
        'data_nascimento2',
        min_value=get_min_date(),
        max_value=get_max_date(),
        value = v_data
    )
        
    submit_btn2 = st.form_submit_button('alterar')
    if submit_btn2 and go_to_editar:
        editar(nome2, data_nascimento2, vivo2)



st.subheader('Estatísticas')
vivos = len(tabela[tabela['vivo'] == 1])
mortos = len(tabela[tabela['vivo'] == 0])
total = len(tabela)
total2 = vivos+mortos

c1, c2 = st.columns(2)

c1.metric('vivos', vivos)
c2.metric('mortos', mortos)


c1, c2 = st.columns(2)
pct1 = tabela[tabela['vivo'] == 1]
pct2 = tabela[tabela['vivo'] == 0]
pct_vivo = round((len(pct1)/total)*100, 2)
pct_morto = round((len(pct2)/total)*100, 2)
c1.metric('pct vivos', f'{pct_vivo}%')
c2.metric('pct mortos', f'{pct_morto}%')

c1, c2 = st.columns(2)
menos_46 = tabela[tabela['idade'] < 46]
pct_menos_46 = round((len(menos_46)/total)*100, 2)

mais_46 = tabela[tabela['idade'] >= 46]
pct_mais_46 = round((len(mais_46)/total)*100, 2)

c1.metric('pct menos de 46 anos', f'{pct_menos_46}%')
c2.metric('pct 46 anos ou mais', f'{pct_mais_46}%')


pct_menos_46_vivos = round(
    (len(menos_46[menos_46['vivo'] == 1])/len(menos_46))*100, 2)
pct_menos_46_mortos = round(
    (len(menos_46[menos_46['vivo'] == 0])/len(menos_46))*100, 2)

pct_mais_46_vivos = round(
    (len(mais_46[mais_46['vivo'] == 1]) / len(mais_46))*100, 2)
pct_mais_46_mortos = round(
    (len(mais_46[mais_46['vivo'] == 0]) / len(mais_46))*100, 2)

c1, c2 = st.columns(2)
c1.metric('pct menos de 46 vivos', f'{pct_menos_46_vivos}%')
c2.metric('pct menos de 46 mortos', f'{pct_menos_46_mortos}%')

c1, c2 = st.columns(2)
c1.metric('pct 46 anos ou mais vivos', f'{pct_mais_46_vivos}%')
c2.metric('pct 46 anos ou mais mortos', f'{pct_mais_46_mortos}%')

st.divider()

dado = tabela[['idade', 'vivo']]

st.subheader('adicionando gráficos (streamlit.bat_chart)')
st.bar_chart(
    data=dado,
    x='idade'
)


st.subheader('adicionando gráficos (plotly)')

st.write(px.histogram(dado))
