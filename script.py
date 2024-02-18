from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Specify the path to the Chrome profile directory
chrome_profile_directory = "C:\\Users\\max\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5"

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=" + chrome_profile_directory)

# Initialize Chrome WebDriver with the custom options
driver = webdriver.Chrome(options=chrome_options)

# Open the Infinite Craft game
driver.get("https://neal.fun/infinite-craft/")

def spawn_item(item_div):
    item_div.click()

def combine_instances(instance1, instance2):
    # Find the instance-emoji element inside each instance and get its text
    emoji_one = driver.execute_script("return arguments[0].querySelector('.instance-emoji').textContent;", instance1)
    emoji_two = driver.execute_script("return arguments[0].querySelector('.instance-emoji').textContent;", instance2)
    
    # Get the text content of the instance, excluding the span's contents
    text_one = driver.execute_script("""
        var spanContent = arguments[0].querySelector('.instance-emoji').textContent;
        var instanceContent = arguments[0].textContent;
        return instanceContent.replace(spanContent, '').trim();
    """, instance1)
    
    text_two = driver.execute_script("""
        var spanContent = arguments[0].querySelector('.instance-emoji').textContent;
        var instanceContent = arguments[0].textContent;
        return instanceContent.replace(spanContent, '').trim();
    """, instance2)
    
    # Simulate drag and drop
    ActionChains(driver).drag_and_drop(instance1, instance2).perform()
    
    # Add a small delay to allow time for the combination animation to finish
    time.sleep(0.1)

    # Find the newest instance
    all_instances = driver.find_elements(By.CLASS_NAME, "instance")
    newest_instance = all_instances[-1]
    
    # Get the text of the newest instance, excluding the span's contents
    newest_text = driver.execute_script("""
        var spanContent = arguments[0].querySelector('.instance-emoji').textContent;
        var instanceContent = arguments[0].textContent;
        return instanceContent.replace(spanContent, '').trim();
    """, newest_instance)
    
    # Get the newest emoji
    newest_emoji = driver.execute_script("return arguments[0].querySelector('.instance-emoji').textContent;", newest_instance)
    
    # Print the combination
    print(emoji_one + text_one, "+", emoji_two + text_two, "=", newest_emoji + newest_text)


items_div = driver.find_element(By.CLASS_NAME, "items")
item_divs = items_div.find_elements(By.CLASS_NAME, "item")
current_item = item_divs[0]
    
# Find the "instances" container div
instances = driver.find_element(By.CLASS_NAME, "instances")

# Recursive function to explore recipes
def explore_recipes():
    # Loop through each item in item_divs
    for item_div in item_divs:

        select_one = current_item
        select_two = item_div

        # Spawn an instance of each item
        spawn_item(select_one)
        spawn_item(select_two)
        

        # Wait for the new instances to appear
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@class='instances']//div[@class='instance']"))
        # )
        
        # Find all instances in the "instances" container
        all_instances = driver.find_elements(By.CLASS_NAME, "instance")

        instance_one = all_instances[len(all_instances) - 2]
        instance_two = all_instances[len(all_instances) - 1]

        # Combine instance one and two
        # print("Combining", instance_one.text, "+", instance_two.text)
        combine_instances(instance_one,instance_two)

        # Call the recursive function to explore recipes further
        # explore_recipes()

# Call the recursive function to start exploring recipes
explore_recipes()

# Once all recipes have been explored, you can print or save them as needed

input("Press enter to continue...")