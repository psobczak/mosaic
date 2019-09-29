from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
from urllib.error import HTTPError
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


link = ['https://www.wykop.pl/hity/roku/2016/',
        'https://www.wykop.pl/hity/roku/2015/']


def get_links_dictionary(link):
    result = {}
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'html.parser')
    links_raw = soup.select('div > h2 > a')
    links = [link.get('href') for link in links_raw]
    for i, link in enumerate(links):
        try:
            new_page = requests.get(link).text
            soup = BeautifulSoup(new_page, 'html.parser')
            last_page = soup.find_all('a', class_="button")[-2].text
            result[link] = last_page
            print(f'{i+1}. {link} --> {last_page}')
        except Exception:
            # TODO: Refractor this!
            print(
                """General exception because i dont want to deal with it now.
                Change it later!""")
    return result


def download_wykop_images(link):
    j = 0
    err_404 = 0
    links = get_links_dictionary(link)
    for k, v in links.items():
        for x in range(1, int(v)):
            r = requests.get(f'{k}strona/{x}/')
            page = r.text
            soup = BeautifulSoup(page, 'html.parser')
            for img in soup.find_all('img'):
                link = img.get('data-original')
                if link is not None:
                    try:
                        start = time.time()
                        urlretrieve(link, 'images/' +
                                    str(time.time()).replace('.', '') + '.jpg')
                        end = time.time()
                        delta_time = end - start
                        time.sleep(delta_time)
                        j += 1
                    except HTTPError:
                        print("404 - not found!")
                        err_404 += 1

                    print(
                        f'{j}. Got {str(delta_time)[:5]} s. - -> {k} in {delta_time}')
    print(f'Ommited {err_404} because of 404!')


# download_wykop_images(link)

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.map(download_wykop_images, link)
