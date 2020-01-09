import argparse
import os
from pathlib import Path
from urllib import request
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options

# Collects the links of every post in every page of selected pedal
def get_post_links(browser, pedal_page_url):
    browser.get(pedal_page_url)
    link_list = []
    
    try:    
        page_end_number = int(browser.find_elements_by_css_selector('div.PageNav:nth-child(2) > span:nth-child(1)')[0].text.split('of ')[1])
    except:
        page_end_number = 1

    for i in range(1, page_end_number+1):
        print("Getting download links. Page " + str(i) + " of " + str(page_end_number))
        title_list = browser.find_element_by_css_selector('ol.discussionListItems')
        
        for li in title_list.find_elements_by_css_selector('li.discussionListItem'):
            link_list.append(li.find_element_by_css_selector('a.PreviewTooltip').get_attribute('href'))
        if(i != page_end_number):
            browser.find_element_by_xpath('//a[text()="Next >"]').click()

    return link_list

def download_patches(browser, link_list):
    print("\nStarting download...\n")
    
    for link in link_list:
        browser.get(link)
        try:
            browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/form/ol/li/div[2]/div[2]/div[1]/div/ul/li/div/div[2]/h6/a').click()
            print("Downloading: " + link)
        except:
            pass
    
    print("Download finished.")
    browser.close()

def login(browser, username, password):
    login_page_url = "https://tonelib.net/forums/login"
    
    browser.get(login_page_url)

    browser.find_element_by_id('ctrl_pageLogin_login').send_keys(username)
    browser.find_element_by_id('ctrl_pageLogin_password').send_keys(password)
    browser.find_element_by_id('ctrl_pageLogin_remember').click()
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div/form/dl[3]/dd/input').click()

    try:
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/header/div/div[3]/div[2]/div/nav/div[1]/div/div/ul[2]/li[3]/a/i')
    except:
        return False
    return True
    

def main():
    desc="A tool for downloading guitar patches from ToneLib Forums"
    argparser = argparse.ArgumentParser(description=desc)
    
    argparser.add_argument("-u", "--user", help='Enter your ToneLib login name', dest='user', required=True)
    argparser.add_argument("-p", "--password", help='Enter your ToneLib password', dest='password', required=True)
    argparser.add_argument("-e", "--effects", help='Enter a effects pedal model. Valid options are: "tonelib", "ms50g", "ms60b", "ms70cdr", "g3n", "g1on", "b1on", "b3n", "g1", "b1".', dest='effects', required=True)
    
    args = argparser.parse_args()
    username = str(args.user)
    password = str(args.password)
    pedal = str(args.effects)

    pedal_folder_name = pedal.upper() + ' Effects'

    pedal_page_urls = {
        "tonelib" : "https://tonelib.net/forums/forums/tonelib-gfx-presets.27/",
        "ms50g" : "https://tonelib.net/forums/forums/zoom-ms-50g.10/",
        "ms60b" : "https://tonelib.net/forums/forums/zoom-ms-60b.11/",
        "ms70cdr" : "https://tonelib.net/forums/forums/zoom-ms-70cdr.12/",
        "g3n" : "https://tonelib.net/forums/forums/zoom-g3n-g3xn-g5n.15/",
        "g1on" : "https://tonelib.net/forums/forums/zoom-g1on-g1xon.13/",
        "b1on" : "https://tonelib.net/forums/forums/zoom-b1on-b1xon.14/",
        "b3n" : "https://tonelib.net/forums/forums/zoom-b3n.16/",
        "g1" : "https://tonelib.net/forums/forums/zoom-g1-g1x-four.30/",
        "b1" : "https://tonelib.net/forums/forums/zoom-b1-b1x-four.31/"
    }

    
    if not pedal in pedal_page_urls:
        print("Invalid effects pedal argument. Exiting...")
        exit(0)

    if not os.path.exists(pedal_folder_name):
        os.makedirs(pedal_folder_name)


    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), pedal_folder_name))
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/g1xon, application/g1on, application/octet-stream, application/binary")
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False) 
    options = Options()
    options.headless = True


    try:
        browser = webdriver.Firefox(executable_path=os.getcwd()+'/geckodriver', firefox_profile=profile, options=options)
    except:
        print("Could not start web driver. Make sure that webdriver and script are in the same directory")

    
    pedal_page_url = pedal_page_urls[pedal]

    is_login_success = login(browser, username, password)

    if is_login_success:
        print("Login is successful.")
        download_patches(browser, get_post_links(browser, pedal_page_url))
    else:
        print("Could not login. Make sure that login credentials are valid.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
            print('\nKeypress Detected.')
            print('\nExiting...')
            exit(0)