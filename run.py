import datetime
import json
import logging
import os
import re
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Seta as configurações de log
log_level = os.getenv('log_level', 'info').lower().strip()
logger = logging.getLogger()
logging_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler para arquivo de log
file_handler = logging.FileHandler('run.log')
file_handler.setFormatter(logging_formatter)
logger.addHandler(file_handler)

# Handler para a saída padrão
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging_formatter)
logger.addHandler(stream_handler)

# Define o nível/severidade dos logs
log_levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
logger.setLevel(log_levels.get(log_level, logging.INFO))
logger.info(f'Severidade dos logs setado em "{log_level.upper()}".')


# Verifica se o "numero_do_processo" foi passado como argumento
try:
    numero_do_processo = sys.argv[1]
    logger.info(f'Iniciando script e buscando pelo número de processo: {numero_do_processo}')
except IndexError:
    logger.error('Número do processo precisar ser inserido como um argumento/paramento do comando .')
    logger.error('Ex.: python ./run.py <número do processo>')
    sys.exit()


# Seta URL de consulta
url = os.getenv('url', 'http://apps.mpf.mp.br/aptusmpf/portal')


# Obtém valor de timeout
try:
    tempo_espera = int(os.getenv('timeout', 10))
except ValueError:
    logger.warning('Valor de timeout inválido, usando valor padrão de 10 segundos.')
    tempo_espera = 10
logger.info(f'Timeout do WebDriver setado em: {tempo_espera} segundos')


def close(e=None):
    """Fecha o navegador e encerra o script."""
    if e: logger.error(f'Script encerrado pelo erro: {str(e)}')
    logger.info('Fechando o navegador.')
    driver.quit()
    logger.info('Encerrando o script.')
    sys.exit(1 if e else 0)


def write_output(output):
    """Salva a saída em um arquivo de texto."""
    # Formatar a data e hora
    data_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Criar o nome do arquivo
    numero_do_processo_sanitizado = re.sub(r'[<>:"/\\|?*~]', '_', numero_do_processo)
    nome_arquivo = f"{numero_do_processo_sanitizado}_{data_hora}.txt"

    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(output)
    logger.info(f'Conteúdo salvo em: {nome_arquivo}')


def verificar_checkbox(checkbox_id, estado_desejado=True):
    """Verifica e ajusta o estado de um checkbox."""
    checkbox = driver.find_element(By.ID, checkbox_id)
    if checkbox.is_selected() != estado_desejado:
        checkbox.click()
        estado = "marcado" if estado_desejado else "desmarcado"
        logger.info(f'O checkbox "{checkbox_id}" foi {estado}.')
    else:
        logger.info(f'O checkbox "{checkbox_id}" já está no estado desejado.')

# Iniciando WebDriver
logger.info(f'Iniciando o WebDriver.')
driver = webdriver.Chrome()
driver.get(url)


# Checa se o site carregou corretamente
try:
    string_check = 'MPF'
    assert string_check in driver.title, f'Título do site não contém a palavra {string_check}.'
    logger.info(f'URL: {url} carregada com sucesso.')
except AssertionError as e:
    logger.error(f'Erro ao carregar a URL: {url}')
    close(e)


# Aguarda o botão "Configurar Pesquisa" ser carregado e faz o clique
try:
    botao = WebDriverWait(driver, tempo_espera).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Configurar Pesquisa."]'))
    )
    logger.info('Clicando no botão "Configurar Pesquisa".')
    botao.click()
except TimeoutException as e:
    logger.error('Não foi possível clicar no botão "Configurar Pesquisa".')
    close(e)


# Aguarda a janela "Configurar Pesquisa" e ajusta checkboxes
try:
    checkbox = WebDriverWait(driver, tempo_espera).until(
        EC.element_to_be_clickable((By.ID, 'q-idx_numeracao'))
    )
    logger.info('Janela "Configurar Pesquisa" carregada com sucesso.')

    # Verifica e ajusta o estado dos checkboxes
    verificar_checkbox('q-idx_numeracao', True)           #Numeração
    verificar_checkbox('q-idx_numeracao2', False)         #Numeração Complementar
    verificar_checkbox('q-idx_partes', False)             #Partes
    verificar_checkbox('q-id_autuacao', False)            #ID Autuacao
    verificar_checkbox('q-id_documento', False)           #ID Documento
    verificar_checkbox('q-nm_membro_participacao', False) #Membro Participação
    verificar_checkbox('q-idx_integras', False)           #Íntegras(Votos;Decisões;Decisões Monocráticas)
    verificar_checkbox('q-idx_resumo', False)             #Resumo   

except TimeoutException as e:
    logger.error('Não foi possível carregar a janela "Configurar Pesquisa".')
    close(e)


# Clicando no botão "Aplicar"
logger.info('Clicando no botão "Aplicar".')
driver.find_element(By.CSS_SELECTOR, '#config_pesquisa .btn-primary').click()


# Preenche a caixa de buscas e pesquisa
try:
    element = WebDriverWait(driver, tempo_espera).until(
        EC.presence_of_element_located((By.ID, 'q'))
    )
    logger.info('Preenchendo a caixa de buscas com o número do processo.')
    element.clear()
    element.send_keys(numero_do_processo)
    logger.info('Clicando no icone lupa.')
    driver.find_element(By.ID, 'btnPesquisar').click()
except TimeoutException as e:
    logger.error('Erro ao preencher a caixa de buscas.')
    close(e)


# Aguarda a primeira linha da tabela da nova página ser carregar
try:
    primeira_linha_tabela = WebDriverWait(driver, tempo_espera).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="div_results"]/div/div/div/table/tbody/tr[1]'))
    )
    logger.info('Tabela da nova página carregada.')

    logger.info('Clicando no link da primeira linha da tabela.')
    primeira_linha_tabela.find_element(By.TAG_NAME, 'a').click()  
except TimeoutException:
    mensagem = 'Processo não encontrado.'
    logger.warning(mensagem)
    write_output(mensagem)
    close()


# Comuta o webdrive para a nova aba aberta
logger.info('Comuta o webdrive para a nova aba aberta.')
abas = driver.window_handles
driver.switch_to.window(abas[-1])


# Aguarda o conteudo ser carregado
logger.info('Aguardando o conteudo ser carregado.')
tabela_processo = WebDriverWait(driver, tempo_espera).until(
    EC.presence_of_element_located((By.ID, 'tab_proc'))
)


# Estrutura todas as informações em um dict/json
logger.info('Estruturando todas as informações em um json.')

# Tratando parte superior da pagina
logger.info('Obtendo o descritivo do processo.')
rows = tabela_processo.find_elements(By.TAG_NAME, 'tr')

dict_processo = {}
# Itera sobre as linhas
for row in rows:
    # Quebra os dados da linha em key e value
    cols = row.find_elements(By.TAG_NAME, 'td')
    key = cols[0].text.strip()[:-1]  # Primeira coluna (chave)

    match key:
        case 'Tombo':
            # Trata a primeira linha da tabela "Tombo"

            # Obtem valor da chave Tombo
            value_tombo = cols[2].find_element(By.XPATH, '//td[3]/div[1]').text # Terceira coluna (valor)
            dict_processo[key] = value_tombo       
            logger.info(f'Extraido os valores: {key} - {value_tombo}')

            # Obtem valor da chave Autuação
            key_autuacao = cols[2].find_element(By.XPATH, '//td[3]/div[5]/div[1]').text.strip()[:-1] # Quinta coluna (chave)
            value_autuacao = cols[2].find_element(By.XPATH, '//td[3]/div[5]/div[2]').text # Sexta coluna (valor)
            dict_processo[key_autuacao] = value_autuacao       
            logger.info(f'Extraido os valores: {key_autuacao} - {value_autuacao}')
            last_key = key

        case '':
            # Trata as linhas da tabela que não tem valor na primeira coluna
            # Complementa o valor da última chave (last_key)
            value = dict_processo[last_key] + ' ' + cols[1].text # Segunda coluna (valor)
            dict_processo[last_key] = value
            logger.info(f'Complementando os valores da {key}: {value}')

        case _:
            # Trata todas as outras demais linhas
            value = cols[1].text  # Segunda coluna (valor)
            dict_processo[key] = value
            logger.info(f'Extraido os valores: {key} - {value}')
            last_key = key


# Tratando parte inferior da página - Tramitação
logger.info('Obtendo todas as tramitações.')
tabela_tramitacao = driver.find_element(By.XPATH, '//*[@id="tab_mov"]/tbody')

lista_tramitacao = []
key_data_hora  = 'Data/Hora'
key_descricao  = 'Descrição'

rows = tabela_tramitacao.find_elements(By.TAG_NAME, 'tr')
# Itera sobre as linhas
for row in rows:
    # Separa os dados da linha entre as keys
    cols = row.find_elements(By.TAG_NAME, 'td')

    value_data_hora  = cols[0].text  # Primeira coluna (data/hora)
    value_descricao  = cols[2].text  # Terceira coluna (descricao)

    logger.info(f'Tramitação: {key_data_hora}: {value_data_hora} | {key_descricao}: {value_descricao}')
    lista_tramitacao.append({key_data_hora: value_data_hora, key_descricao: value_descricao})

dict_processo['tramitacao'] = lista_tramitacao  

# Salva o dicionário como JSON em um arquivo
logger.info('Transformando objeto dict python em JSON.')
dict_processo_json = json.dumps(dict_processo, indent=4)
logger.debug(f'Conteudo do JSON gerado: {dict_processo_json}')
write_output(dict_processo_json)

# Encerra o script
close()
