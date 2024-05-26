from scraper import Scraper
from converter import Converter

def main():
    url = "https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html"
    navigation_path = "Acesso_a_internet_e_posse_celular – 2015 – Tabelas_de_Resultados – xlsx – 01_Pessoas_de_10_Anos_ou_Mais_de_Idade"
    navigation_path = navigation_path.split(" – ") 

    files = [
        "01_Utilizacao_da_Internet.xlsx",
        "02_Equipamento_Utlizado_para_Acessar_a_Internet.xlsx",
        "03_Posse_de_Telefone_Movel_Celular.xlsx"
    ]

    download_dir = "xslx_files"
    csv_dir = "csv_files"

    scraper = Scraper(url, navigation_path, download_dir, files)
    try:
        scraper.navigate_to_target_page()
        scraper.download_files()
    finally:
        scraper.close()

    converter = Converter(download_dir, csv_dir)
    converter.csv_converter()


if __name__ == "__main__":
    main()
