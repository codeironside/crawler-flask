import os
import random
import requests
import pandas as pd
import time
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, send_file
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir, "database.sqlite")

db = SQLAlchemy(app)
class Scrapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name_location = db.Column(db.String)
    date_time = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())
    
    @property
    def cleaned_date_time(self):
        return f"{self.date_time.day}/{self.date_time.month}/{self.date_time.year}"

def scrape_api():
    url = "https://cate-search.hktvmall.com/query/products"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.hktvmall.com",
        "Referer": "https://www.hktvmall.com/",
        "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    }

    current_page = 0
    page_size = 60
    all_products = []

    while current_page<2:
        payload = {
            "query": ":relevance:zone:personalcarenhealth:street:main:",
            "currentPage": current_page,
            "pageSize": page_size,
            "pageType": "searchResult",
            "lang": "en",
            "CSRFToken": "fe21ee82-09e6-4b40-9ab1-c1875f151c07"
        }

        response = requests.post(url, headers=headers, data=payload)
        data = response.json()

        # Extract and process the data as needed
        product_list = data.get('products', [])
        if not product_list:
            break  # No more products, exit the loop

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Output the information
            print(f"{'-'*20}\n"
                  f"image_url: {image_url}\n"
                  f"brand_product_name: {brand_product_name}\n"
                  f"sales_number: {sales_number}\n"
                  f"review_number: {review_number}\n"
                  f"promotion_price: {promotion_price}\n"
                  f"original_price: {original_price}\n")

        all_products.extend(product_list)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-personal_health_care.xlsx"
    df.to_excel(file, index=False)
    return file


@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')


@app.route('/results/',methods=['GET'])
def display_results():
    results = Scrapper.query.all()
    
    context = {
        "results":results
    }
    
    return render_template("results.html",context=context)

@app.route('/scrape/', methods=['GET','POST'])
def scrapper():
    if request.method == "POST":
        print('scrapping___ _ _ _ _ please wait...')
        scrape_api()
        print('done_ _  _ _ scrapping ')

        file = scrape_api()
        new_scrapper = Scrapper(file_name_location=file)
        db.session.add(new_scrapper)
        db.session.commit()
        context = {
            "file_name": new_scrapper.file_name_location,
            "date_time": new_scrapper.cleaned_date_time
        }
        return render_template("scrapper_result.html",context=context, file=file)
    return render_template("scrapper.html")

@app.route("/download/<path:file>/", methods=["GET"])
def download(file):
    return send_file(file, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #DEBUG is SET to TRUE. CHANGE FOR PROD
        app.run(port=5000,debug=True)
    