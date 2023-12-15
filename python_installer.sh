#!/bin/bash
#
# instalador de libs do projeto python
#
#

# mesmo atualizando python pra 3.8 continua dando erro. na execucao do streamlit
# todas as libs estao com pau!
# TODO: rodar as libs em arquivos individuais pra ver
# fafm, 13/12/2023


# usar python3.8
# cd /usr/bin && find pytho*
# so:
# cd <novo_multi_teste>
# python3.8 -m venv .venv
# virtualenv --python="/usr/bin/python3.8" "<path/to/venv"
# se fizer isso acima, alterar no if abaixo
# bloco pro if acima ser executado soh uma vez

if [ ! -f ".python_installer_init0" ]; then 
    python3.8 -m venv .venv
    virtualenv --python="/usr/bin/python3.8" "/home/fafm/python/multi_testes/python_multi_testes/.venv"
    echo "DO NOT REMOVE THIS FILE!" > .python_installer_init0
fi 


source .venv/bin/activate

# https://stackoverflow.com/questions/49748063/pip-install-fails-for-every-package-could-not-find-a-version-that-satisfies
if [ ! -f ".python_installer_init1" ]; then
    # if python >=3.7
    curl https://bootstrap.pypa.io/get-pip.py | python
    # else
    # curl https://bootstrap.pypa.io/pip/3.6/get-pip.py | python 
    pip install --upgrade setuptools
    echo "DO NOT REMOVE THIS FILE!" > .python_installer_init1
fi 


pip install --upgrade pip
pip3 install --upgrade pip

modulos=(
'pandas' 'numpy' 'plotly' 'streamlit' 'mysql-connector-python' 'pyautogui' 'gTTS'
)

for m in "${modulos[@]}"; do
    pip3 install $m
done
