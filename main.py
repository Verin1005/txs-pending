import pandas as pd
import concurrent.futures
import collections
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import FastAPI

app = FastAPI()


class Scraper():
    def __init__(self):
        self._driver = self._init_driver()
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        return driver

    def _get_paged_url(self, page):
        return f'https://etherscan.io/txsPending?a={self._address}&ps=100&p={page}'

    def _get_all_paged_urls(self, total_pages):
        return [self._get_paged_url(page) for page in range(0, total_pages)]

    def set_query(self, address, page=-1):
        self._address = address
        self._total_pages = None
        self._page = page
        self._table_list = []

    def load_page(self, page):
        url = self._get_paged_url(page)
        self._driver.get(url)
        total_pages = int(self._driver.find_element(By.CSS_SELECTOR, 'span.page-link.text-nowrap').text.split(' ')[-1])
        table = pd.read_html(self._driver.find_element(By.TAG_NAME, 'table').get_attribute('outerHTML'))[0]
        return table, total_pages

    def load_first_page(self):
        return self.load_page(0)

    def try_load_page(self, page):
        try:
            return self.load_page(page)
        except Exception as e:
            print(e)
            return pd.DataFrame([]), -1

    def try_load_all_pages(self):
        try:
            return self.load_all_pages()
        except Exception as e:
            print(e)
            return pd.DataFrame([]), -1

    def load_all_pages(self):
        table_dict = {}
        table, total_pages = self.load_first_page()
        table_dict[self._get_paged_url(0)] = table
        urls = self._get_all_paged_urls(total_pages)[1:]
        future_to_url = {self._executor.submit(self.load_page, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                table, _ = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                table_dict[url] = table

        od = collections.OrderedDict(sorted(table_dict.items()))
        return pd.concat(list(od.values())), total_pages

    def response(self, df):
        return list(df.T.to_dict().values())


scraper = Scraper()


@app.get("/txn-pending")
async def root(address: str, page: int = -1):
    scraper.set_query(address, page)
    if page == -1:
        table, total_pages = scraper.try_load_all_pages()
    else:
        table, total_pages = scraper.try_load_page(page)

    return {
        'address': address,
        'txn_pending': scraper.response(table),
        'total_pages': total_pages,
    }
