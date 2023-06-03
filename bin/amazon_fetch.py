
import requests
from bs4 import BeautifulSoup
import yaml
import sys
import openai

asin = sys.argv[1]
if not asin:
    print("Please provide the ASIN as an argument.")
    sys.exit(1)
url = f"https://www.amazon.com/dp/{asin}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Accept-Language': 'en-US,en;q=0.9',
}


response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting high-res image URL
    img_tag = soup.find('img', {'id': 'landingImage'})
    high_res_img_url = img_tag['data-old-hires']

    # Extracting product title
    product_title = soup.find('span', {'id': 'productTitle'}).text.strip()

    # Extracting rating and number of reviews
    rating_tag = soup.find('span', {'class': 'a-icon-alt'})
    rating = rating_tag.text.strip().split()[0]
    num_reviews = soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip().split()[0]

    # Extracting product price
    price_whole_tag = soup.find('span', {'class': 'a-price-whole'})
    price_whole = price_whole_tag.text.strip('.')

    price_fraction_tag = soup.find('span', {'class': 'a-price-fraction'})
    price_fraction = price_fraction_tag.text.strip()
    # Extracting asin
    asin = soup.find('input', {'id': 'ASIN'})['value']
    description = soup.find('div', {'id': 'feature-bullets'}).get_text()

    openai_result = []
    with open('.openai_key', 'r') as openai_key_file:
        openai.api_key = openai_key_file.readline().strip()
        openai_result = openai.ChatCompletion.create(
            model="gpt-4", messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"""
                    i have the following product description, i need you to summarize it into no more than 25 words:
                    ---
                    {description}
                    """}
            ]
        )
    if 'choices' not in openai_result:
        print("Problem getting GPT4 response!")
        sys.exit(1)

    p = {
        "img_url": high_res_img_url,
        "title": product_title,
        "rating": rating,
        "num_reviews": num_reviews.replace(",",""),
        "price": f"{price_whole}.{price_fraction}",
        "url": f"https://www.amazon.com/dp/{asin}",
        "description": openai_result['choices'][0]['message']['content']
    }
    # Downloading the high-res image
    #img_response = requests.get(high_res_img_url, stream=True)

#    with open('product_image.jpg', 'wb') as img_file:
#        img_response.raw.decode_content = True
#        shutil.copyfileobj(img_response.raw, img_file)
#        print("\nImage successfully downloaded as 'product_image.jpg'")

    with open("products.yaml", "r+") as file:
        data = yaml.safe_load(file)

    # Check if 'products' key exists and create one if not
    if not data:
        data = {"products": []}
    elif "products" not in data:
        data["products"] = []
    data["products"].append(p)
    with open("products.yaml", "w") as file:
        yaml.safe_dump(data, file)
else:
    print("Couldn't fetch the product page. Check the URL and try again.")
