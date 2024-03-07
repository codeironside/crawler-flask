import os
import random
import requests
import pandas as pd
import time
from datetime import datetime
from flask import Blueprint, Flask, redirect, url_for, render_template, request, send_file
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


home_bp = Blueprint('home',__name__) 
app=Flask(__name__,static_folder='static')
app.register_blueprint(home_bp)
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-personal_health_care.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_2():
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

    while current_page < 2:
        payload = {
            "query": ":relevance:zone:gadgetsandelectronics:street:main:",
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
        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-gadgetsnelectronics.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_3():
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
            "query": ":relevance:zone:beautynhealth:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-beautynhealth.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_4():
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
            "query": ":relevance:zone:mothernbaby:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-mothernbaby.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_5():
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
            "query": ":relevance:zone:finance:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-finance.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_6():
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
            "query": ":relevance:zone:homenfamily:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-homenfamily.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_7():
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
            "query": ":relevance:zone:sportsntravel:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-sportsntravel.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_8():
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
            "query": ":relevance:zone:toysnbooks:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-toysnbooks.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_9():
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
            "query": ":relevance:zone:supermarket:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-supermarket.xlsx"
    df.to_excel(file, index=False)
    return file

def scrape_10():
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
            "query": ":relevance:zone:thirteenlandmarks:street:main:",
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

        product_data = []

        for product in product_list:
            # Extract relevant information
            image_url = product.get('images', [{}])[0].get('url', '')
            brand_product_name = product.get('brand', '') + ' ' + product.get('name', '')
            sales_number = product.get('salesVolume', 0)
            review_number = product.get('numberOfReviews', 0)
            promotion_price = product.get('price', {}).get('formattedValue', '')
            original_price = product.get('price', {}).get('value', 0)

            # Create a dictionary for the product
            product_dict = {
                "image_url": image_url,
                "brand_product_name": brand_product_name,
                "sales_number": sales_number,
                "review_number": review_number,
                "promotion_price": promotion_price,
                "original_price": original_price
            }

            # Append the dictionary to the list
            product_data.append(product_dict)
            # Output the information
            print(f"{'-'*20}\n"
                f"image_url: {image_url}\n"
                f"brand_product_name: {brand_product_name}\n"
                f"sales_number: {sales_number}\n"
                f"review_number: {review_number}\n"
                f"promotion_price: {promotion_price}\n"
                f"original_price: {original_price}\n")
            
        # Convert the list of dictionaries to a DataFrame
        # df = pd.DataFrame(product_data)

        # # Save the DataFrame to an Excel file
        # df.to_excel("product_data.xlsx", index=False)

        all_products.extend(product_data)
        current_page += 1

        # time.sleep(2)

    # Save data to a DataFrame and Excel file
    data_dict = {"data": all_products}
    df = pd.DataFrame.from_dict(data_dict['data'])
    file = f"./results/{int(time.time())}-thirteenlandmarks.xlsx"
    df.to_excel(file, index=False)
    return file
# @app.route('/',methods=['GET','POST'])
@home_bp.route('/')
def home():
    if request.method == 'POST':
        # Handle POST Request here
        return render_template('index.html')
    
    # Read data from the Excel file
    excel_data = pd.read_excel("homedata/1709218950-personal_health_care.xlsx")  # Adjust path as needed

    # Convert DataFrame to JSON format and pass it to the template
    return render_template('index.html', excel_data=excel_data.to_json(orient='records'))
@app.route('/results/',methods=['GET'])
def display_results():
    results = Scrapper.query.all()
    return render_template("results.html", results=results)

@app.route('/scrape/', methods=['POST'])
def scrapper():
    print('Scraping... please wait...')
    file = scrape_api()  # Assuming this function returns the file path
    file2 = scrape_2()
    file3 = scrape_3()
    file4 = scrape_4()
    file5 = scrape_5()
    file6 = scrape_6()
    file7 = scrape_7()
    file8 = scrape_8()
    file9 = scrape_9()
    file10 = scrape_10()
    print('Scraping done')

    new_scrapper = Scrapper(file_name_location=file)
    new_scrapper2 = Scrapper(file_name_location=file2)
    new_scrapper3 = Scrapper(file_name_location=file3)
    new_scrapper4 = Scrapper(file_name_location=file4)
    new_scrapper5 = Scrapper(file_name_location=file5)
    new_scrapper6 = Scrapper(file_name_location=file6)
    new_scrapper7 = Scrapper(file_name_location=file7)
    new_scrapper8 = Scrapper(file_name_location=file8)
    new_scrapper9 = Scrapper(file_name_location=file9)
    new_scrapper10 = Scrapper(file_name_location=file10)
    db.session.add(new_scrapper)
    db.session.add(new_scrapper2)
    db.session.add(new_scrapper3)
    db.session.add(new_scrapper4)
    db.session.add(new_scrapper5)
    db.session.add(new_scrapper6)
    db.session.add(new_scrapper7)
    db.session.add(new_scrapper8)
    db.session.add(new_scrapper9)
    db.session.add(new_scrapper10)
    db.session.commit()
    return redirect(url_for('display_results'))

@app.route("/download/<path:file>/", methods=["GET"])
def download(file):
    return send_file(file, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #DEBUG is SET to TRUE. CHANGE FOR PROD
        app.run(port=5000,debug=True)
    
