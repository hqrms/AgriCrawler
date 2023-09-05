import json
import requests
from bs4 import BeautifulSoup
import logging

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
        processed_response = self.get_quotation_data_from_html(response)
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
    

    def get_quotation_data_from_html(self, html_page):
        """
        Realiza a iteração entre os componentes HTML da página e coleta
        todas as informações das divs com a classe "cotacao"

        Args:
            html_page : Página HTML (https://www.noticiasagricolas.com.br/cotacoes/soja). 
        """
        quotation_data = []
        soup = BeautifulSoup(html_page.text, 'html.parser')
        quotation_tables = soup.find_all('div', class_='cotacao')

        index = 0
        try:
            for quotation_table in quotation_tables:
                soybean_info = []

                table_title = quotation_table.find('a').text
                table_title = table_title.strip().replace('\n', "")
                soybean_table = quotation_table.find('table', class_='cot-fisicas')
                table_head_text = soybean_table.find('thead').text
                table_body = soybean_table.find('tbody')
                table_rows = table_body.find('tr')
                quotation_table_text = table_rows.text     

                soybean_info.append(table_title)
                soybean_info.append(table_head_text.strip().replace('\n', " - "))
                soybean_info.append(quotation_table_text.strip().replace('\n', " - "))

                soybean_dictionary = {
                    "Titulo": soybean_info[0],
                    "Descrições" :soybean_info[1],
                    "Valores": soybean_info[2]
                }
                quotation_data.append(soybean_dictionary)

                index += 1

            print(quotation_data)
            return quotation_data
       
        except Exception as e:
            message = ("Falha na API [Erro: {status}]".format(status = e))
            logging.error(message)
            return ("Erro interno na API.", 500)

    

