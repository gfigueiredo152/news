import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
import mysql.connector
from GoogleNews import GoogleNews
import pandas as pd
import validators
from datetime import datetime, timedelta
import logging
import cidades_PR
import os
import Google_BigQuery

def mysql_ent(title, link, source, Datas, snippet, valor, Vag_link, Regiao, Microregiao, Cidade):
    try:
        db_config = {
            'host': '35.239.141.124',
            'user': 'root',
            'password': "G|cP^D'Ej1<u;I<F",
            'database': 'twoMaths',
        }

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Assuming source is a date, convert it to the appropriate format
        #source = datetime.strptime(source, '%Y-%m-%d')
        #verifica se tem data 
        
        try:
            data_formatada_I = Datas.strftime("%Y-%m-%d %H:%M:%S")
        except:
            data_atual  = datetime.now()
            data_formatada_I = data_atual.strftime("%Y-%m-%d %H:%M:%S")
        
        # If valor and Vag_link are lists, process each element
        
        valor = [float(val.replace('[', '').replace(']', '').strip()) for val in valor]
        Vag_link = [float(link.replace('[', '').replace(']', '').strip()) for link in Vag_link]
        if valor:
            valor = valor[0]
        else:
            valor = 0
        
        if Vag_link:
            Vag_link = Vag_link[0]
        else:
            Vag_link = 0
        active = 1

        consulta = "SELECT Link FROM twoMaths.noticias WHERE Link = %s"
        parametro = (link)
        
        # Executar a consulta
        cursor.execute(consulta, parametro)
        
        # Recuperar os resultados da consulta

        resultados = cursor.fetchall()
        
        # Verificar se há resultados
        if len(resultados) == 0:
            
            if valor > 0 or Vag_link > 0:
                # Se não houver resultados, o link não existe, então podemos inseri-lo
                insert_query = "INSERT INTO twoMaths.noticias (Title, Source, link, Date_Posted, Snippet, investimento, Vagas, Regiao, Microregiao, Cidade, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                # Ajustar o número de espaços reservados para corresponder ao comprimento da tupla de dados
                data = (title, source, link, data_formatada_I, snippet, valor, Vag_link,Regiao, Microregiao, Cidade, active)

                cursor.execute(insert_query, data)
                conn.commit()
        
        # Fechar o cursor (não a conexão) após a execução das consultas
        cursor.close()

    except Exception as e:
        # Log the error
        logging.error(f'Ocorreu um erro: {str(e)}')
        logging.error("Data e hora do erro: %s", datetime.now())
        # Log the complete traceback
        logging.exception("Detalhes do erro:")
        logging.basicConfig(filename='Inf_log.log', level=logging.DEBUG)
       
# Função para realizar a consulta inicial e filtrar notícias relevantes
def perform_initial_Google(keywords,relevant_keywords ,num_results):
    googlenews = GoogleNews(lang='pt')
    news_data = []

    for keyword in keywords:
        googlenews.clear()
        googlenews.search(keyword)
        results = googlenews.results()

        for result in results[:num_results]:
            title = result['title']
            link = result['link']
            source = result['media']
            date_posted = result['date']
            snippet = result['desc']
            
            if any(keyword in title.lower() or keyword in snippet.lower() for keyword in relevant_keywords):
                news_data.append({
                    'Title': title,
                    'Source': source,
                    'Link': link,
                    'Date_Posted': date_posted,
                    'Snippet': snippet
                })

    return news_data

def perform_initial_query(urlsBing,relevant_keywords):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    data = []  # Lista para armazenar os resultados de todas as urlsBing

    for url in urlsBing:
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')

        for result in soup.select('.card-with-cluster'):
            title = result.select_one('.title').text
            link = result.select_one('.title')['href']
            snippet = result.select_one('.snippet').text
            try:
                source = result.select_one('.source a').text
            except:
                source = result.select_one('.title')['data-author']
            print(source)
            date_posted = result.select_one('#algocore span+ span').text

            is_relevant = any(keyword in title.lower() or keyword in snippet.lower() for keyword in relevant_keywords)

            if is_relevant:
                data.append([title, source,link, date_posted, snippet])
    
    return data
    
# Função para extrair informações específicas de uma página vinculada 
def extract_info_from_link(title, link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }
    # Procurar valores monetários na string 'title'
    valores_titulo = re.search(r'\b([0-9]+(?:\.[0-9]{3})*(?:,[0-9]{1,2})?|[0-9]+(?:,[0-9]{2})?)\s*(bilhões?|milhões?|trilhões|bilhão|milhão|trilhão|Bi|Mi)\b', title, re.IGNORECASE)
    
    if valores_titulo:
        # Extrair e retornar valores monetários formatados como uma única frase
        return extract_values(valores_titulo.group(0))

    try:
        # Fazer solicitação HTTP
        response = requests.get(link, headers=headers)
        response.raise_for_status()  # Verificar se houve um erro na solicitação
        soup = BeautifulSoup(response.text, 'html.parser')

        # Procurar valores monetários na resposta
        Valor_Inv = re.search(r'\b([0-9]+(?:\.[0-9]{3})*(?:,[0-9]{1,2})?|[0-9]+(?:,[0-9]{2})?)\s*(bilhões?|milhões?|trilhões|bilhão|milhão|trilhão|Bi|Mi)\b', response.text, re.IGNORECASE)

        if Valor_Inv:
            # Extrair e retornar valores monetários formatados como uma única frase
            return extract_values(Valor_Inv.group(0))
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação HTTP: {e}")

    return []

def extract_values(matched_string):
    # Extrair valores monetários e unidades e formatar como uma única frase
    valores = re.findall(r'\b([0-9]+(?:\.[0-9]{3})*(?:,[0-9]{1,2})?|[0-9]+(?:,[0-9]{2})?)\s*(bilhões?|milhões?|trilhões|bilhão|milhão|trilhão|Bi|Mi)\b', matched_string, re.IGNORECASE)
    
    resultado = []
    
    if valores:
        # A função findall retorna uma lista de tuplas
        # Cada tupla contém grupos de captura para uma correspondência
        for valor, unidade in valores:
            valor_numerico = float(valor.replace(',', ''))
            unidade = unidade.lower()
            
            if unidade == 'milhões' or unidade == 'milhão' or unidade == 'mi':
                valor_numerico *= 1000000
            elif unidade == 'bilhões' or unidade == 'bilhão' or unidade == 'bi':
                valor_numerico *= 1000000000
            elif unidade == 'trilhões' or unidade == 'trilhão' or unidade == 'tri':
               valor_numerico *= 1000000000000
            else:
                valor_numerico = 0
                    
            resultado.append(valor_numerico)
    
    return resultado

def remover_palavras_vagas(texto):
    palavras_a_remover = ['vagas', 'novas vagas', 'novos empregos', 'empregos', 'funcionários', 'novos funcionários'] 
    padrao = r'\b(?:' + '|'.join(map(re.escape, palavras_a_remover)) + r')\b'
    texto_sem_palavras = re.sub(padrao, '', texto, flags=re.IGNORECASE)
    return texto_sem_palavras

def extract_info_Vagas(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    
    response = requests.get(link, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        Valor_vaga = re.search(r'\b(\d+(?:\.\d+)?)\s+(vagas|novas vagas|novos empregos|empregos|funcionários|novos funcionários)\b', response.text, re.IGNORECASE)

        if Valor_vaga:
            # Correção: chamar a função com a string original, não o objeto de correspondência
            texto_sem_palavras = remover_palavras_vagas(Valor_vaga.group(0))
            return [texto_sem_palavras]
    return [0]

# Função para verificar se o conteúdo da página menciona Minas Gerais
def mentions_mg(content):
    
    keywords = ["Paraná","PR"]
    for keyword in keywords: 
        if keyword.lower() in content.lower():
            return True
    return False

# Validade dos links
def is_valid_url(url):
    return validators.url(url)

# Tratamento das datas
def convert_to_datetime(date_str):
    match = re.match(r'(\d+)([a-zA-Z]+)', date_str)

    if match:
        value, unit = int(match.group(1)), match.group(2).lower()
        unit_factors = {'m': 'minutes', 'h': 'hours', 'dia': 'days', 'mês': 'months'}
        new_date = (datetime.now() - timedelta(**{unit_factors.get(unit, 'minutes'): value})).date()
        
        return new_date
    
    return None

def dub_noticia(title):
    fila = []
    repete_palavra = 0
    eh_repetida = False
    palavras_noticia_da_vez = title.lower().split()
    if len(fila)>1:
        for palavras_noticia in fila:
            for palavra in palavras_noticia:
                if palavra in palavras_noticia_da_vez and len(palavra) >= 4:
                    repete_palavra += 1
    if repete_palavra >= 5:
        eh_repetida = True
    else:
        fila.append(palavras_noticia_da_vez)
    
    return eh_repetida

# Retorna região, microregião, cidade e contexto a qual foi achada no texto
def filtro_cidade(page_content):
    regioes = [cidades_PR.Noroeste_Parana, cidades_PR.Norte_Central_Parana, cidades_PR.Oeste_Parana, cidades_PR.Sudoeste_Parana, cidades_PR.Centro_Sul_Parana, cidades_PR.Campos_Gerais_Parana, cidades_PR.Metropolitana_Curitiba, cidades_PR.Litoral_Parana, cidades_PR.Norte_Pioneiro_Parana]
    palavras_chave = ['na','de','em', 'próximo']
    cidades_encontradas = []
    # Pega cidade uma por uma com sua respectiva regiao e microregiao   
    for regiao in regioes:
        microregioes = regiao()
        nome_regiao = microregioes[0] 
        for microregiao in microregioes[1:]:
            for cidade in microregiao["Cidade"]:
                #padrao_cidade = r'(?:' + '|'.join(map(re.escpea, palavras_chave)) + r')\s*' + re.escape(cidade) + r'\b'
                padrao_cidade = r'(?:' + '|'.join(map(re.escape, palavras_chave)) + r')\s*' + re.escape(cidade) + r'\b'
                resultado = re.search(padrao_cidade, page_content)
                if resultado:
                    # Contexto para entender se faz sentido o investimento com a cidade
                    inicio = resultado.start()
                    fim = resultado.end()
                    contexto = resultado.group(0)
                    cidades_encontradas.append([nome_regiao, microregiao.Name, cidade, contexto, inicio, fim])
                    cidades_encontradas.sort(key=lambda x: x[4])

                    return cidades_encontradas[:1]      
    if not resultado:
        nome_regiao = '-'; microregiao = '-';cidade = '-';contexto='-';inicio='-';fim='-'
        cidades_encontradas.append([nome_regiao, microregiao, cidade, contexto, inicio, fim])
        cidades_encontradas.sort(key=lambda x: x[4])
        
        return cidades_encontradas[:1]
def main():  
    try:    
        #Info pesquisa realizadas pelo Bing
        urlsBing = [
            'https://www.bing.com/news/search?q=investimento+de+empresas+na+regiao+de+%22PR%22&go=Pesquisar&qs=ds&form=QBNT',
            'https://www.bing.com/news/search?q=investimento+de+empresas+em+%22PR%22&go=Pesquisar&qs=ds&form=QBNT',
            'https://www.bing.com/news/search?q=aporte+de+empresas+EM+%22PR%22&go=Pesquisar&qs=ds&form=QBNT',
            'https://www.bing.com/news/search?q=expan%C3%A7%C3%A3o+de+empresas+em+%22PR%22+&go=Pesquisar&qs=ds&form=QBNT',
        ]
        #pesquisa realizada pelo google
        keywords  = ['investimento de empresas na regiao de "PR"',
                       'investimento de empresas em "PR"',
                       'aporte de empresas EM "PR"',
                       'expanção de empresas em "PR" '] 

        # Obter resultados do Bing e Google
        relevant_keywords = ["investimentos", "investe", "economia", "investimento", "expansão", "gerar", "nova unidade" ]

        bing_results = perform_initial_query(urlsBing,relevant_keywords)
        google_results = perform_initial_Google(keywords,relevant_keywords, num_results=5)
        
        if bing_results or google_results:
            combined_data = []
            results = []
            # a==========
            # Lista para dataFrama cidades
            results_cidades = []
            # b=========

            # Combinar os resultados do Bing e do Google
            combined_data.extend(bing_results)
            for google_result in google_results:
                title = google_result.get('Title', '')
                source = google_result.get('Source', '')
                link = google_result.get('Link', '')
                date_posted = google_result.get('Date_Posted', '')
                snippet = google_result.get('Snippet', '')

                combined_data.append([title,  source, link, date_posted, snippet])

        for item in combined_data:
            title, source, link, date_posted, snippet = item

            if is_valid_url(link) and not dub_noticia(title):
                
                # Fazendo o download do conteudo da pagina
               
                try:
                    if '&' in link:
                        link = link.split('&')[0]
                    response = requests.get(link) 
                    response.raise_for_status()
                    if response.status_code == 200:
                        page_content = response.text

                        #Verificar se o contéudo da pagina menciona Minas Gerais
                        if mentions_mg(page_content):
                            Investimento = extract_info_from_link(title, link)
                            Vagas = extract_info_Vagas(link)
                            Datas = convert_to_datetime(date_posted)

                            valor = ""
                            Vag_link = ""

                            if Investimento:
                                valor = list(map(str, Investimento))
                            if Vagas:
                                Vag_link = list(map(str, Vagas))
                            
                            # a==================================================================
                            try:
                                # Cria um soup do html
                                soup = BeautifulSoup(response.text, 'html.parser')
                                # Retira apenas as tags <p> que estão os textos das noticias
                                conteudo = soup.find_all('p')
                                # Tranforma em uma string separadas por //
                                conteudo_string = '//'.join(paragraph.text for paragraph in conteudo)
                                # Chama a função dando o a string acima como parametro
                                info_geografica = filtro_cidade(conteudo_string)
                                # b==================================================================
                            except:
                                print("cidade não encontrada link:",link)
                            
                            palavras_desejadas = ['Diário', 'globo', 'G1', 'Uol', 'exame', 'revistaoe','Mercado&Consumo', 'Record News', 'Diario Regional','Hoje em dia']

                            # Verificar se pelo menos uma palavra desejada está presente na fonte
                            if any(palavra in source or link for palavra in palavras_desejadas):

                                # a===========================================================================================
                                if info_geografica != []:
                                    for info in info_geografica:
                                            results_cidades.append([title,  source, link, Datas, snippet, valor, Vag_link, info[0], info[1], info[2]])
                                            print("\n")
                                            print(results_cidades)
                                # b============================================================================================

                                   
                
                except requests.exceptions.RequestException as e:
                    print("\n")
                    print(f"Erro ao fazer a solicitação para {link}: {e}")


                           
        # Colunas do DataFrame de cidades
        headers_df_cidades = ['Title', 'Source','Link', 'Date_Posted', 'Snippet', 'Investimento', 'Vagas' ,'Regiao', 'Microregiao', 'Cidade',]
        #print(headers_df_cidades)
        # DataFrame que correlaciona cidades com as noticias
        df_cidades = pd.DataFrame(results_cidades, columns=headers_df_cidades)
        
        #df_sem_diario_do_comercio = df_cidades[~df_cidades['Contexto'].str.contains("© Diário do Comércio.")]
        df_sem_linhas_em_branco = df_cidades.dropna(subset='Title')
        
        df_sem_duplicatas = df_sem_linhas_em_branco.drop_duplicates(subset='Title')

        # Iterar sobre as linhas do DataFrame e chamar a função mysql_ent para cada linha
        print(df_sem_duplicatas)
        
        file_ex = "Parana.xlsx"

        df_sem_duplicatas.to_excel(file_ex, index=False)



        #Google_BigQuery.main(df_sem_duplicatas)
        
    except ZeroDivisionError as e:
        # Log de erro
        logging.error(f'Tentativa de divisão por zero: {e}')
        logging.error(f"Ocorreu um erro: {str(e)}")
        logging.error("Data e hora do erro: %s", datetime.now())
        # Pode ser útil também registrar a traceback completa
        logging.exception("Detalhes do erro:")
    logging.basicConfig(filename='Inf_log.log', level=logging.DEBUG)
if __name__ == "__main__":
    main()