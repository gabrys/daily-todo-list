#!/usr/bin/env python

import locale
from config import config
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fx = None


def wait_for_sync():
    locator = By.CSS_SELECTOR, '*[aria-label="Every change you make is automatically saved"]'
    WebDriverWait(fx, 10).until(EC.text_to_be_present_in_element(locator, "All notes saved"))


def log_in():
    fx.get('https://accounts.google.com/')
    fx.find_element_by_css_selector('#Email').send_keys(config['email'])
    fx.find_element_by_css_selector('#Passwd').send_keys(config['password'])
    fx.find_element_by_css_selector('form').submit()


def get_note(label, title):
    fx.get('https://keep.google.com/#label/' + config['label'])
    fx.implicitly_wait(10)
    xpath = '//div[contains(text(), "' + title + '")]/following-sibling::div'
    notes = fx.find_elements_by_xpath(xpath)
    if len(notes):
        return notes[0]
    return None


def copy_note(label, template_title, new_title):
    # Get the note
    get_note(label, template_title).click()

    # Copy the note
    more_btns = fx.find_elements_by_css_selector('div[role="toolbar"] div[aria-label="More"]')
    more_btns[-1].click()
    copy_btn = fx.find_element_by_xpath('//div[contains(text(), "Make a copy")]')
    copy_btn.click()

    # Update the title
    xpath = '//div[contains(text(), "' + template_title + '")]'
    title = fx.find_elements_by_xpath(xpath)[-1]
    title.click()
    title.clear()
    title.send_keys(new_title.decode('utf-8'))

    # Save/close
    xpath = '//div[contains(text(), "Done")]'
    fx.find_elements_by_xpath(xpath)[-1].click()


if __name__ == '__main__':
    fx = webdriver.Firefox()
    log_in()
    locale.setlocale(locale.LC_ALL, config['lang'])
    today_title = datetime.now().strftime(config['today_title_format'])
    if get_note(config['label'], today_title) is None:
        copy_note(config['label'], config['template_title'], today_title)
        wait_for_sync()
        print 'Note ' + today_title + ' added'
    else:
        print 'Note ' + today_title + ' already in place'
    fx.quit()

