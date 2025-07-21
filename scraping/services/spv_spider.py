import time
import datetime
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from tqdm import tqdm

from core.models import Pesquisa, PesquisaSPV, Website, Funcionario

NADA_CONSTA = "Não existem informações disponíveis para os parâmetros informados."
CONSTA01 = "Processos encontrados"
CONSTA02 = "Audiências"
EXECUTAVEL = "/code/msedgedriver"  # Caminho para o driver do Selenium


class SPVAutomatico:
    def __init__(self, filtro: int = 0):
        self.filtro = filtro

    def pesquisar(self):
        pesquisas = Pesquisa.objects.filter(
            data_conclusao__isnull=True, tipo=0, cpf__isnull=False
        ).exclude(spv__filtro=self.filtro)[:200]

        for p in tqdm(pesquisas, desc=f"Executando filtro {self.filtro}"):
            self.executa_pesquisa(p)

    def executa_pesquisa(self, pesquisa: Pesquisa):
        documento = (
            pesquisa.cpf
            if self.filtro == 0
            else pesquisa.rg if self.filtro in [1, 3] else pesquisa.nome
        )

        html = self.carrega_site(documento)
        resultado = self.checa_resultado(html)

        PesquisaSPV.objects.create(
            cod_pesquisa=pesquisa,
            cod_funcionario=Funcionario.objects.get_or_create(nome="Bot")[0],
            website=Website.objects.get_or_create(url="https://esaj.tjsp.jus.br")[0],
            cod_spv=1,
            cod_spv_computador=36,
            cod_spv_tipo=1,
            filtro=self.filtro,
            resultado=resultado,
        )

    def checa_resultado(self, html):
        if NADA_CONSTA in html:
            return 1
        if CONSTA01 in html or CONSTA02 in html:
            if "criminal" in html.lower():
                return 2
            return 5
        return 7

    def carrega_site(self, documento, url="https://esaj.tjsp.jus.br/cpopg/open.do"):
        service = Service(executable_path="/usr/bin/chromedriver")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        browser = webdriver.Chrome(service=service, options=options)
        browser.get(url)

        try:
            select_el = browser.find_element("xpath", '//*[@id="cbPesquisa"]')
            select_obj = Select(select_el)
            if self.filtro in [0, 1, 3]:
                select_obj.select_by_value("DOCPARTE")
                browser.find_element("xpath", '//*[@id="campo_DOCPARTE"]').send_keys(
                    documento
                )
            elif self.filtro == 2:
                select_obj.select_by_value("NMPARTE")
                browser.find_element(
                    "xpath", '//*[@id="pesquisarPorNomeCompleto"]'
                ).click()
                browser.find_element("xpath", '//*[@id="campo_NMPARTE"]').send_keys(
                    documento
                )
            browser.find_element("xpath", '//*[@id="botaoConsultarProcessos"]').click()
            time.sleep(2)
        except Exception as e:
            print("Erro no carregamento:", e)
            browser.quit()
            return ""
        html = browser.page_source
        browser.quit()
        return html
