import sys
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
g = Service()
driver = webdriver.Chrome(options=options, service=g)
base_url = 'https://www.saucedemo.com/'
driver.get(base_url)
driver.maximize_window()
# Data for autorization
user_name_password = "standard_user"
password_main = "secret_sauce"
# Installed expectation
driver.implicitly_wait(5)
# User authorization
user_name = driver.find_element(By.XPATH, "//input[@id='user-name']")
password = driver.find_element(By.XPATH, "//input[@id='password']")
button_login = driver.find_element(By.XPATH, "//input[@id='login-button']")
user_name.send_keys(user_name_password)
password.send_keys(password_main)
button_login.click()
# Create a product list
array_products = []
name_products = driver.find_elements(By.XPATH, "//div[@class='inventory_item_name']")
button_products = driver.find_elements(By.XPATH, "//button[@class='btn btn_primary btn_small btn_inventory']")
price_products = driver.find_elements(By.XPATH, "//div[@class='inventory_item_price']")
text_messeg = ""
for i in range(len(name_products)):
    array_products.append({
        "button": button_products[i].get_attribute("id"),
        "name": name_products[i].text,
        "price": price_products[i].text.replace("$", "")
    })
    text_messeg = text_messeg + str(i + 1) + ". " + name_products[i].text + " "
print(array_products)

print("Выберите товар " + text_messeg)
select_product = input("Выбирите варианты, указав номера через ',': ")
arr_select_product = select_product.split(",")
# Add products in the cart
try:
    for f in arr_select_product:
        button = driver.find_element(By.XPATH, "//button[@id='" + array_products[int(f) - 1]["button"] + "']")
        button.click()
    cart = driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']")
    cart.click()
except NoSuchElementException:
    print("Не найден выбранный товар" + array_products[int(f) - 1]["name"])
else:
    print("Выбранный товар успешно добавлен в корзину, переход к оформлению заказа")


driver.find_element(By.XPATH, "//button[@id='checkout']").click()
driver.find_element(By.XPATH, "//input[@id='first-name']").send_keys("Ivan")
driver.find_element(By.XPATH, "//input[@id='last-name']").send_keys("Ivanov")
driver.find_element(By.XPATH, "//input[@id='postal-code']").send_keys("123456")
driver.find_element(By.XPATH, "//input[@id='continue']").click()
print("Данные покупателя заполнены")
# Сравнение выбранных товаров с оформляймыми
total_price = 0
try:
    for elem in arr_select_product:
        assert driver.find_element(By.XPATH, "//div[text()='" + array_products[int(elem) - 1]["name"] + "']").text == array_products[int(elem) - 1]["name"]
        assert driver.find_element(By.XPATH, "//div[text()='" + array_products[int(elem) - 1]["price"] + "']").text.replace("$","") == array_products[int(elem) - 1]["price"]
        total_price += float(array_products[int(elem) - 1]["price"])
        print(total_price)
except NoSuchElementException:
    print("Несоответствие выбранного товара с оформляемым товаром")
    sys.exit()
try:
    total = driver.find_element(By.XPATH, "//*[@id='checkout_summary_container']/div/div[2]/div[6]").text.replace("Item total: $", "")
    assert total_price == float(total)
except:
    print("Общяя сумма товара не соответсвует ожиданиям")
driver.find_element(By.XPATH, "//button[@id='finish']").click()

try:
    assert driver.find_element(By.XPATH, "//h2[text()='Thank you for your order!']").text == "Thank you for your order!"
    print("Заказ оформлен успешно")
except AssertionError:
    print("Заказ не оформлен")
