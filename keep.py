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


def get_note_text(label, title):
    fx.get('https://keep.google.com/#label/' + config['label'])
    xpath = '//div[contains(text(), "' + title + '")]/following-sibling::div'
    notes = fx.find_elements_by_xpath(xpath)
    if len(notes):
        return notes[0].text.encode('utf-8')
    return None


def add_note(label, title, text, todo_list=False):
    fx.get('https://keep.google.com/#label/' + config['label'])

    # Open add note form
    fx.find_element_by_xpath('//div[contains(text(), "Add note")]').click()

    # Fill the note contents
    fx.find_element_by_xpath('//div[contains(text(), "Add note")]').click()
    fx.find_element_by_css_selector('*:focus').send_keys(text.decode('utf-8'))

    # Fill the note title
    fx.find_element_by_xpath('//div[contains(text(), "Title")]').click()
    fx.find_element_by_css_selector('*:focus').send_keys(title.decode('utf-8'))

    if todo_list:
        # Convert to list
        fx.find_element_by_css_selector('*[role="toolbar"] *[aria-label="New list"][aria-disabled="false"]').click()

    # Save
    fx.find_element_by_xpath('//div[@role="button"][contains(text(), "Done")]').click()


if __name__ == '__main__':
    fx = webdriver.Firefox()
    log_in()
    locale.setlocale(locale.LC_ALL, config['lang'])
    today_title = datetime.now().strftime(config['today_title_format'])
    if get_note_text(config['label'], today_title) is None:
        template = get_note_text(config['label'], config['template_title'])
        add_note(config['label'], today_title, template, todo_list=True)
        wait_for_sync()
        print 'Note ' + today_title + ' added'
    else:
        print 'Note ' + today_title + ' already in place'
    fx.quit()

