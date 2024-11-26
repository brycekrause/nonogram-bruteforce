from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert 
import time
import os

print("Nonogram.org Bruteforce")
id = input("Nonogram.org id number: ")
width = int(input("Nonogram width: "))
height = int(input("Nonogram height: "))
print("Loading... Please wait...")

driver = webdriver.Edge()
driver.get("https://www.nonograms.org/nonograms/i/" + id)

# Fill boxes
for y in range(height):
    for x in range(width):
        print(x, y)
        box = driver.find_element(By.ID, f"nmf{x}_{y}")
        box.click()
        box_styles = box.get_attribute('style')
        box_styles = box_styles.split(";")
        time.sleep(0.1)

# Find and click check button
time.sleep(1)
check_button = driver.find_element(By.ID, "innc").click()
time.sleep(1)

# Find bad squares
for y in range(height):
    for x in range(width):
        print(x, y)
        incorrect = driver.find_element(By.ID, f"nmf{x}_{y}")
        if incorrect.value_of_css_property("background-image") == 'url("https://www.nonograms.org/i/cutoutbad3w.gif")':
            incorrect.click()

# Dismiss solved alert
time.sleep(2)
Alert(driver).dismiss()
time.sleep(2)

if not os.path.exists('solved'):
    os.makedirs("solved")

# Save a screenshot
container = driver.find_element(By.CLASS_NAME, "content")
container.screenshot(f"solved/{id}.png")
print(f"Done!\nSaved nonogram to solved/{id}.png")