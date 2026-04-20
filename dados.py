import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.supermonas.pt/catalog"

data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

for page in range(1, 27):  # 26 páginas
    offset = (page - 1) * 12

    if offset == 0:
        url = base_url
    else:
        url = f"{base_url}/{offset}"

    print(f"A processar página {page} -> {url}")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("article", class_="product-box")

    if not products:
        print("Sem produtos, parar.")
        break

    for p in products:
        name = p.find("h3").get_text(strip=True)
        price = p.find("span", class_="product-price").get_text(strip=True)
        link = p.find("a")["href"]

        # imagem
        img_tag = p.find("img", class_="primary-img")
        if img_tag and "data-src" in img_tag.attrs:
            image = img_tag["data-src"]
        else:
            image = ""

        data.append([name, price, link, image])

print(f"Total produtos: {len(data)}")

# guardar CSV
with open("produtos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Nome", "Preço", "Link", "Imagem"])
    writer.writerows(data)