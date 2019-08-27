from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import json


class Scrapper():

    def test(self):
        driver = webdriver.Firefox(executable_path=r"./Selenium/geckodriver")
        driver.get(
            "https://stackoverflow.com/questions/11750447/performing-a-copy-and-paste-with-selenium-2")
        time.sleep(5)
        driver.close()
        return 200

    def get_elementos(self, driver):
        # obtengo todos los elementos a completar
        # cualquiera de estas palabras
        ors = driver.find_element_by_name("ors")
        # todas estas palabras
        ands = driver.find_element_by_name("ands")
        # Frase exacta por ej: del potro
        phrase = driver.find_element_by_name("phrase")
        # hashtags
        tags = driver.find_element_by_name("tag")
        # ninguna de estas
        nots = driver.find_element_by_name("nots")
        # desde estas cuentas
        from_ = driver.find_element_by_name("from")
        # respondiendo a
        respondiendo = driver.find_element_by_name("to")
        # mencionando a
        mencionando = driver.find_element_by_name("ref")
        # idioma espaniol
        driver.find_element_by_xpath(
            "//*[@id=\"lang\"]/option[text()=\'español (español)\']").click()
        # fecha desde
        fecha_desde = driver.find_element_by_xpath("//*[@id=\"since\"]")
        # fecha hasta
        fecha_hasta = driver.find_element_by_xpath("//*[@id=\"until\"]")
        return ors, ands, phrase, tags, nots, respondiendo, mencionando, fecha_desde, fecha_hasta, from_

    def colocar_fecha(self, driver, ands, elemento_fecha, kwargs_fecha):
        # Coloca las fechas cortando y pegando
        try:
            ands.click()
        except e:
            print(e)
        ands.send_keys(kwargs_fecha)
        time.sleep(2)
        ands.send_keys(Keys.CONTROL, 'a')  # selecciono todo
        ands.send_keys(Keys.CONTROL, 'x')  # corto
        elemento_fecha.click()
        delay = 2
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'datepicker-days')))
        time.sleep(3)
        elemento_fecha.send_keys(Keys.CONTROL, 'v')  # paste
        time.sleep(3)

    def colocar_busqueda(self, lista_elementos, **kwargs):
        elem_ands, elem_ors, elem_phrase, elem_tags, elem_nots, elem_respondiendo, \
            elem_mencionando, elem_from = lista_elementos[0], lista_elementos[1], \
                lista_elementos[2], lista_elementos[3], lista_elementos[4], \
                    lista_elementos[5], lista_elementos[6], lista_elementos[7]

        ands = kwargs['ands']
        ors = kwargs['ors']
        phrase = kwargs['phrase']
        tags = kwargs['tags']
        nots = kwargs['nots']
        from_ = kwargs['From']
        respondiendo = kwargs['respondiendo']
        mencionando = kwargs['mencionando']

        elem_ands.send_keys(ands)
        time.sleep(0.5)
        elem_ors.send_keys(ors)
        time.sleep(0.5)
        elem_phrase.send_keys(phrase)
        time.sleep(0.5)
        elem_tags.send_keys(tags)
        time.sleep(0.5)
        elem_nots.send_keys(nots)
        time.sleep(0.5)
        elem_from.send_keys(from_)
        time.sleep(0.5)
        elem_respondiendo.send_keys(respondiendo)
        time.sleep(0.5)
        elem_mencionando.send_keys(mencionando)
        time.sleep(0.5)

    def buscar_ir_a_recientes(self, driver):

        driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div/div[1]/form/button").click()
        delay = 3  # seconds
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                           'AdaptiveFiltersBar-nav')))
        # ir a recientes
        btn_recientes = driver.find_element_by_xpath(
            "//a[@data-nav=\'search_filter_tweets\']")
        time.sleep(1)
        btn_recientes.click()

    def scrollear(self, driver):
        # scrollear en pagina con driver
        SCROLL_PAUSE_TIME = 3.5
        # Get scroll height
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        #i = 0
        band = True
        while band:
            # Scroll down to bottom
            #i = i +1
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Esperar que cargue la pag
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                band = False
            else:
                last_height = new_height

    def get_html(self, driver):
        # obtengo y devuelvo html con beautiful soup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #print("imprimiendo soup en el metodo get html")
        # print(soup)
        return soup

    def get_action_number(self, tweet, clase):
        # obtiene numero de rts y favs dependiendo el elemento que le pases en clase
        # action = retweet o fav
        action_button = tweet.find('button', class_=clase)
        action_text = action_button.find(
            'span', class_='ProfileTweet-actionCountForPresentation').text
        if action_text == '':
            # no tiene likes ni/o rts
            action = 0
        elif 'K' in action_text or 'M' in action_text:
            # cuando esta abreviada la cantidad saco asi
            integ = action_button.find(
                'span', class_='ProfileTweet-actionCount')['data-tweet-stat-count']
            action = int(integ)
        else:
            # no esta abreviada la cantidad
            action = int(action_text)
        return action

    def get_tweets_soup(self, soup):
        # Devuelve un pandas de tweets
        # primero sacamos el contenedor de tweets
        tweets_container = soup.find_all(
            'li', class_='js-stream-item stream-item stream-item')
        tweets = []
        # tweets = [['Username', 'Text', 'Fecha', 'Favs', 'Rts', 'Link']]
        for tweet in tweets_container:
            username = tweet.find(
                'span', class_='username u-dir u-textTruncate').text
            tw_text = tweet.find(
                'div', class_='js-tweet-text-container').p.text.replace(";", ",")
            tw_link = 'https://twitter.com' + tweet\
                .find('a', class_='tweet-timestamp js-permalink js-nav js-tooltip')['href']
            fecha_ms = tweet.find('a', class_='tweet-timestamp js-permalink js-nav js-tooltip')\
                .span['data-time-ms']
            rts = int(self.get_action_number(
                tweet, 'ProfileTweet-actionButton js-actionButton js-actionRetweet'))
            favs = int(self.get_action_number(
                tweet, 'ProfileTweet-actionButton js-actionButton js-actionFavorite'))

            tweets.append([username, tw_text, fecha_ms, favs, rts, tw_link])

        df = pd.DataFrame(
            tweets, columns=['username', 'text', 'fecha', 'favs', 'rts', 'link'])

        df['fecha'] = pd.to_datetime(df['fecha'], unit='ms')

        return df

    def selenium_get_tweets(self, **kwargs):
        # option headless
        options = Options()
        options.headless = True

        #driver = webdriver.Firefox(options=options, executable_path=r"./Selenium/geckodriver")
        driver = webdriver.Firefox(executable_path=r"./Selenium/geckodriver")

        driver.get("https://twitter.com/search-advanced?lang=es")

        # obtengo todos los elementos a completar
        ors, ands, phrase, tags, nots, respondiendo, mencionando, fecha_desde, fecha_hasta, \
            from_ = self.get_elementos(driver)
        
        time.sleep(3)
        # pongo en espaniol
        driver.find_element_by_xpath(
            "//*[@id=\"lang\"]/option[text()=\'español (español)\']").click()

        # fecha desde es un mes atras en esta prueba
        k_fecha_desde = kwargs['fecha_desde']
        k_fecha_hasta = kwargs['fecha_hasta']
        # mandamos las fechas
        self.colocar_fecha(driver, ands, fecha_desde, k_fecha_desde)
        self.colocar_fecha(driver, ands, fecha_hasta, k_fecha_hasta)

        lista_elementos = ands, ors, phrase, tags, nots, respondiendo, mencionando, from_
        self.colocar_busqueda(lista_elementos, **kwargs)
        self.buscar_ir_a_recientes(driver)
        self.scrollear(driver)
        time.sleep(2)
        soup = self.get_html(driver)
        driver.quit()
        
        tweets = self.get_tweets_soup(soup)
        tweets_json = json.loads(tweets.to_json(orient='records'))
        
        return tweets_json
