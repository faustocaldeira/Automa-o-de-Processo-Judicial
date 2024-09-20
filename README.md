# Automação de Processo Judicial

Este script automatiza a extração de dados de processos judiciais de um portal público utilizando Selenium.
Este script foi testado em uma máquina Windows e é fortemente recomendado criar um ambiente virtual (virtual environment) para sua execução.

## Requisitos

- **Python 3.10** ou superior.
- Todos os módulos necessários estão listados no arquivo `requirements.txt`. Para instalá-los, utilize o seguinte comando:

```bash
pip install -r requirements.txt
```

## Execução do Script

Para executar o script, utilize a seguinte sintaxe:

```bash
python3 run.py <numero_de_processo>
```

### Exemplo:

```bash
python3 run.py 10274083620184013400
```

## Variáveis de Ambiente

Você pode configurar algumas variáveis de ambiente para personalizar o comportamento do script:

- `URL`  
  Define a URL da aplicação de consulta.  
  **Padrão:** `http://apps.mpf.mp.br/aptusmpf/portal`

- `log_level`  
  Nível de log utilizado durante a execução.  
  **Padrão:** `INFO`  
  **Opções:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

- `webdrive_timeout`  
  Define o tempo de espera para o WebDriver, em segundos.  
  **Padrão:** `10` segundos  
  **Tipo:** Qualquer valor inteiro

## Logs

Os logs serão gerados na saída padrão e também serão gravados no arquivo `run.log`.

## Saída dos Dados

Os dados do processo serão gravados em um arquivo com a seguinte formação de nome:  
`<numero_do_processo_sanitizado>_<data_hora>.txt`
