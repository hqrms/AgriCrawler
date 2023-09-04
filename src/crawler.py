import json
import requests
from bs4 import BeautifulSoup
import logging
import crawler_test

logging.basicConfig(
    level=logging.INFO,
    filename='api_log.log',
    filemode='a', 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class AgriCrawler():
    """
    Classe responsável por realizar a coleta de dados de preços de soja do site Notícias Agricolas
    
    URL: https://www.noticiasagricolas.com.br/cotacoes/soja

    Esta classe implementa um crawler simples para coletar as informações de preço e variação

    Args:
        start_url (str): A URL para coleta de dados.

    """
    def __init__(self, url):
        self.url = url 
        self.final_json = []


    def run(self):
        """
        Orquestra o processo de coleta de dados.

        Os dados coletados retornam apenas com o valor do campo original.
        """
                
        response = self.request_url()
        processed_response = self.get_cotation_data_from_html(response)
        return processed_response
        
 
    def request_url(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            return response
        else:
            message = ('Falha na operação [Erro: {status}]: {url}'
                       .format(status = response.status_code, url=self.url))

            logging.error(message)
            return message
    

    def get_cotation_data_from_html(self, html_page):
        """
        Realiza a iteração entre os componentes HTML da página e coleta
        todas as informações das divs com a classe "cotacao"

        Args:
            html_page : Página HTML (https://www.noticiasagricolas.com.br/cotacoes/soja). 
        """
        cotation_data = []
        soup = BeautifulSoup(html_page.text, 'html.parser')
        cotations = soup.find_all('div', class_='cotacao')


        for cotation in cotations:
            cotation_tables_titles = []
            cotation_tables = cotation.find_all('table', class_='cot-fisicas')

            for table in cotation_tables:
                table_bodies = table.find_all('tbody')

                for table_body in table_bodies:
                    table_rows = table_body.find_all('tr')

                    for table_rows in table_rows:
                        cotation_table_text = table_rows.text
                        cotation_array = cotation_table_text.strip().split('\n')
                        cotation_data.append(cotation_array)

        return cotation_data
    




