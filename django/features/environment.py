from splinter.browser import Browser

from selenium import webdriver


def before_all(context):
    # context.browser = Browser('firefox', headless=True)
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    
    context.browser = webdriver.Firefox(options=options)
    
def after_all(context):
    context.browser.quit()
    context.browser = None