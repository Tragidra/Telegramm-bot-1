from bs4 import BeautifulSoup
import requests


def parser(url):
    html = requests.get(url=url).text
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ''.join(chunk for chunk in chunks if chunk)
    return text

print(parser('http://127.0.0.1:8000/'))