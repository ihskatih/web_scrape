from bs4 import BeautifulSoup
from urllib.request import urlopen
url = "https://food.list.co.uk/places/what:restaurants/location:New%20England%2852.0547%2C0.4853%29/distance:50/page:{}/#results"

from selenium import webdriver

DRIVER_PATH = 'C:/Users/Hitakshi/Desktop/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

base_url="https://food.list.co.uk"

final_result = []
for i in range(1,31):
    result = []
    html = urlopen(url.format(str(i)))
    print(url.format(str(i)))
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('div', attrs={'class':'placeSummary'}):
        result.append('/'+'/'.join(item.find('a')['href'].split('/')[-3:]))
    for link in result:
        try:
            samples = {'name': '', 'address': '', 'number': '', 'email': '', 'website': '', 'fb': '', 'insta': '',
                        'twitter': ''}
            driver.get(base_url+link)
            res = BeautifulSoup(driver.page_source)
            samples['name'] = res.find('div', attrs={'class':'placeHeading'}).find('h1').text
            samples['address']=res.find('span', attrs={'street-address'}).text+', '+ res.find('span', attrs={'locality'}).text+', '+ res.find('span', attrs={'postal-code'}).text.replace('\xa0',' ')
            for li in res.find('ul',  attrs={'contact'}).find_all('li'):
                if li.has_attr('class'):
                    samples['number']= li.find('span').text
                elif li.find('a', attrs={'class':'url'}) is not None:
                    samples['website']=li.find('a', attrs={'class':'url'})['href']
                else:
                    samples['email']=li.find('a').text
            for social in res.find_all('li', attrs={'class':'externalLink'}):
                if 'facebook' in social.find('a')['href']:
                    samples['fb']=social.find('a')['href']
                elif 'insta' in social.find('a')['href']:
                    samples['insta'] = social.find('a')['href']
                else:
                    samples['twitter'] = social.find('a')['href']
            final_result.append(samples.copy())
        except Exception as e:
            #print(str(e))
            #print('na')
            pass
print(final_result)


