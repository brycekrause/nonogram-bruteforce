from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.edge.options import Options
import time
import os
from PIL import Image

print("Nonogram.org Bruteforce")
id = input("Nonogram.org id number: ")

options = Options()
options.add_argument('--headless')

driver = webdriver.Edge(options=options)
driver.get("https://www.nonograms.org/nonograms/i/" + id)

print("Loading")

time.sleep(5)

size = driver.find_element(By.XPATH, "//td[contains(text(), 'Size: ')]").text
size_value = size.split(': ')[1]
width, height = size_value.split('x')
width = int(width)
height = int(height)

driver.execute_script("document.body.style.zoom = '30%';")

# Fill boxes
for y in range(height):
    for x in range(width):
        box = driver.find_element(By.ID, f"nmf{x}_{y}")
        time.sleep(0.01)
        box.click()

        box_styles = box.get_attribute('style')
        box_styles = box_styles.split(";")

        width_percent = (x / width)
        height_percent = (y / height) * 100 + width_percent
        print(f'Part 1/2: {round(height_percent, 2)}%')

# Find and click check button
time.sleep(1)
check_button = driver.find_element(By.ID, "innc").click()
time.sleep(1)

# Find bad squares
for y in range(height):
    for x in range(width):
        incorrect = driver.find_element(By.ID, f"nmf{x}_{y}")
        if incorrect.value_of_css_property("background-image") == 'url("https://www.nonograms.org/i/cutoutbad3w.gif")':
            time.sleep(0.01)
            incorrect.click()

        width_percent = (x / width)
        height_percent = (y / height) * 100 + width_percent
        print(f'Part 2/2: {round(height_percent, 2)}%')

# Dismiss solved alert
time.sleep(2)
Alert(driver).dismiss()
time.sleep(2)

if not os.path.exists('solved'):
    os.makedirs("solved")

# Save a screenshot
container = driver.find_element(By.CLASS_NAME, "nonogram_table")
driver.save_screenshot(f"solved/{id}.png")

table = container.location
size = container.size

image = Image.open(f"solved/{id}.png")

left = table['x']
top = table['y']
right = left + size['width']
bottom = top + size['height']

final_image = image.crop((left, top, right, bottom))
print(f"Done!\nSaved nonogram to solved/{id}.png")