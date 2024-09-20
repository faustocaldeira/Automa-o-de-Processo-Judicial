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

O arquivo gerado terá um conteúdo semelhante ao seguinte:
```json
{
    "Tombo": "1027408-36.2018.4.01.3400 , 1027408-36.2018.4.01.3400, 1027408-36.2018.4.01.3400, 1027408-36.2018.4.01.3400, 1027408-36.2018.4.01.3400(TRF1/DF-1027408-36.2018.4.01.3400-AC)",
    "Autua\u00e7\u00e3o": "24/02/2021",
    "NUP": "1027408-36.2018.4.01.3400",
    "Classe": "APELA\u00c7\u00c3O C\u00cdVEL - AC",
    "Unidade": "PROCURADORIA REGIONAL DA REP\u00daBLICA DA 1\u00aa REGI\u00c3O",
    "Of\u00edcio": "SEM DISTRIBUI\u00c7\u00c3O ATIVA",
    "Membro": "SEM DISTRIBUI\u00c7\u00c3O ATIVA",
    "Autor": "FABRICIO GONCALVES DE SOUZA",
    "R\u00e9u": "); SECRET\u00c1RIO DE GEST\u00c3O DO TRABALHO E DA EDUCA\u00c7\u00c3O NA SA\u00daDE UNI\u00c3O FEDERAL",
    "Advogado": "PROCURADORIA-REGIONAL DA UNI\u00c3O DA 1\u00aa REGI\u00c3O THAIS THADEU FIRMINO",
    "Grupo Tem\u00e1tico": "5\u00aa C\u00c2MARA - COMBATE \u00c0 CORRUP\u00c7\u00c3O, 1\u00aa C\u00c2MARA - DIREITOS SOCIAIS E ATOS ADMINISTRATIVOS EM GERAL",
    "Assunto CNMP": "1\u00aa CCR - Inscri\u00e7\u00e3o / Documenta\u00e7\u00e3o, 5\u00aa CCR - Inscri\u00e7\u00e3o / Documenta\u00e7\u00e3o",
    "Localiza\u00e7\u00e3o Atual": "TRF1/DF - TRIBUNAL REGIONAL FEDERAL 1\u00aa REGI\u00c3O",
    "tramitacao": [
        {
            "Data/Hora": "08/05/2024   05:55:33",
            "Descri\u00e7\u00e3o": "Finaliza\u00e7\u00e3o Distribui\u00e7\u00e3o Titular - Autom\u00e1tica, conforme regras da unidade: PRR1 - 15\u00ba Of\u00edcio - Membro: LUIZ FRANCISCO FERNANDES DE SOUZA - Motivo: Finaliza\u00e7\u00e3o autom\u00e1tica por finaliza\u00e7\u00e3o da autua\u00e7\u00e3o"
        },
        {
            "Data/Hora": "14/11/2023   15:23:34",
            "Descri\u00e7\u00e3o": "Movimentado para TRF1/DF - TRIBUNAL REGIONAL FEDERAL 1\u00aa REGI\u00c3O"
        },
        {
            "Data/Hora": "13/11/2023   00:39:40",
            "Descri\u00e7\u00e3o": "Recebido pelo(a) GABINETE DE PROCURADOR REGIONAL DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "13/11/2023   00:07:45",
            "Descri\u00e7\u00e3o": "Movimentado para GABINETE DE PROCURADOR REGIONAL DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "13/11/2023   00:07:42",
            "Descri\u00e7\u00e3o": "Entrada no(a) DIVIS\u00c3O DE REGISTRO, DISTR. E INFORMA\u00c7\u00d5ES PROCESSUAIS-PRR/1\u00aa"
        },
        {
            "Data/Hora": "09/03/2021   13:48:40",
            "Descri\u00e7\u00e3o": "Movimentado para TRF1/DF - TRIBUNAL REGIONAL FEDERAL 1\u00aa REGI\u00c3O"
        },
        {
            "Data/Hora": "09/03/2021   13:47:09",
            "Descri\u00e7\u00e3o": "Parecer N\u00e3o Padronizado(Manifesta\u00e7\u00e3o em Segundo Grau/ATOS FINAL\u00cdSTICOS/Movimento) n\u00ba 19361/2021(PRR1\u00aa REGI\u00c3O-MANIFESTA\u00c7\u00c3O-19361/2021) - ADMINISTRATIVO. APELA\u00c7\u00c3O EM MANDADO DE SEGURAN\u00c7A. DIPLOMA ESTRANGEIRO. PROGRAMA MAIS M\u00c9DICO. PARECER PELO PROVIMENTO DA APELA\u00c7\u00c3O. (membro autor: LUIZ FRANCISCO FERNANDES DE SOUZA)."
        },
        {
            "Data/Hora": "05/03/2021   16:52:21",
            "Descri\u00e7\u00e3o": "Recebido pelo(a) GABINETE DE PROCURADOR REGIONAL DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "05/03/2021   16:35:58",
            "Descri\u00e7\u00e3o": "Movimentado para GABINETE DE PROCURADOR REGIONAL DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "05/03/2021   16:35:49",
            "Descri\u00e7\u00e3o": "Distribui\u00e7\u00e3o Titular - Autom\u00e1tica, conforme regras da unidade: PRR1 - 15\u00ba Of\u00edcio - Membro: LUIZ FRANCISCO FERNANDES DE SOUZA"
        },
        {
            "Data/Hora": "05/03/2021   16:35:45",
            "Descri\u00e7\u00e3o": "Entrada no(a) DIVIS\u00c3O DE REGISTRO, DISTR. E INFORMA\u00c7\u00d5ES PROCESSUAIS-PRR/1\u00aa"
        },
        {
            "Data/Hora": "05/03/2021   16:32:08",
            "Descri\u00e7\u00e3o": "Dependente - Secund\u00e1rio --> TRF1/DF-1036479-77.2018.4.01.0000-AI"
        },
        {
            "Data/Hora": "03/03/2020   16:10:57",
            "Descri\u00e7\u00e3o": "Movimentado para JF-DF - JUSTI\u00c7A FEDERAL - SE\u00c7\u00c3O JUDICI\u00c1RIA DO DISTRITO FEDERAL"
        },
        {
            "Data/Hora": "03/03/2020   13:15:06",
            "Descri\u00e7\u00e3o": "Recebido pelo(a) GABINETE DE PROCURADOR DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "03/03/2020   08:16:03",
            "Descri\u00e7\u00e3o": "Movimentado para GABINETE DE PROCURADOR DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "03/03/2020   01:24:25",
            "Descri\u00e7\u00e3o": "Entrada no(a) DIVIS\u00c3O C\u00cdVEL DA PR/DF"
        },
        {
            "Data/Hora": "22/08/2019   15:30:26",
            "Descri\u00e7\u00e3o": "Movimentado para JF-DF - JUSTI\u00c7A FEDERAL - SE\u00c7\u00c3O JUDICI\u00c1RIA DO DISTRITO FEDERAL"
        },
        {
            "Data/Hora": "22/08/2019   12:54:10",
            "Descri\u00e7\u00e3o": "Recebido pelo(a) GABINETE DE PROCURADOR DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "22/08/2019   12:03:14",
            "Descri\u00e7\u00e3o": "Movimentado para GABINETE DE PROCURADOR DA REP\u00daBLICA"
        },
        {
            "Data/Hora": "22/08/2019   12:02:33",
            "Descri\u00e7\u00e3o": "Entrada no(a) DIVIS\u00c3O C\u00cdVEL DA PR/DF"
        }
    ]
}
```
