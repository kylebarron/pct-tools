#! /usr/bin/env python3

import re
import click
import selenium.webdriver.support.expected_conditions as EC

from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


@click.command()
@click.argument(
    'gpx_paths',
    type=click.Path(exists=True, readable=True, resolve_path=True),
    nargs=-1)
@click.option(
    '-n',
    '--name',
    type=str,
    help=
    "Route name. Only supported with a single gpx_path as argument. Otherwise uses file path name."
)
@click.option(
    '-d',
    '--desc',
    type=str,
    help='Description for routes. Input is used for all uploads.')
@click.option(
    '--sync',
    default=False,
    is_flag=True,
    help='Set to push to watch on next sync.')
@click.option(
    '--public',
    default=False,
    is_flag=True,
    help='Whether route should be publicly visible.')
@click.option(
    '--website',
    type=str,
    help='Website for routes. Input is used for all uploads.')
@click.option(
    '--tags', type=str, help='Tags for routes. Input is used for all uploads.')
def import_routes(gpx_paths, name, sync, public, desc, website, tags):
    print('starting Chrome')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome()
    print('started Chrome')
    print('signing in')
    sign_in(driver)
    print('signed in')

    gpx_paths = [Path(gpx_path) for gpx_path in gpx_paths]
    if name is None or len(gpx_paths) > 1:
        names = [p.stem for p in gpx_paths]
    else:
        names = [name]

    names = [re.sub(r'[^a-zA-Z0-9]', ' ', name) for name in names]

    for gpx_path, route_name in zip(gpx_paths, names):
        import_route(
            driver,
            gpx_path=gpx_path,
            route_name=route_name,
            use_with_watch=sync,
            public=public,
            description=desc,
            website=website,
            tags=tags)


def sign_in(driver):
    url = 'https://www.movescount.com/auth?redirect_uri=%2fmap'
    driver.get(url)

    # Sign in
    # sign_in_button = driver.find_element_by_css_selector(
    #     '#nav-top .button--cancel')
    # sign_in_button.click()

    # Get credentials
    with Path('~/.credentials/movescount.txt').expanduser().open() as f:
        email, password = [x.strip() for x in f.readlines()]

    # enter credentials
    email_field = driver.find_element_by_css_selector('#splEmail')
    email_field.send_keys(email)
    pw_field = driver.find_element_by_css_selector('#splPassword')
    pw_field.send_keys(password)
    login_button = driver.find_element_by_css_selector('#splLoginButton')
    login_button.click()


def import_route(
        driver,
        gpx_path,
        route_name,
        use_with_watch=False,
        public=False,
        description=None,
        website=None,
        tags=None):

    import_route_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'fileImportInput')))
    import_route_button.send_keys(str(gpx_path))

    # Fill in route fields before saving
    route_name_field = driver.find_element_by_css_selector('#routeName')
    route_name_field.clear()
    route_name_field.send_keys(route_name)

    try:
        simplification_note = driver.find_element_by_css_selector(
            '#simplificationNote')
        print(simplification_note.text)
    except NoSuchElementException:
        pass

    if description is not None:
        driver.find_element_by_css_selector('#add-description-btn').click()
        route_description_field = driver.find_element_by_css_selector(
            '#route-description-text')
        route_description_field.send_keys(description)

    if website is not None:
        driver.find_element_by_css_selector('#add-website-btn').click()
        website_field = driver.find_element_by_css_selector(
            '#route-website-text')
        website_field.send_keys(website)

    if tags is not None:
        driver.find_element_by_css_selector('#add-tags-btn').click()
        tags_field = driver.find_element_by_css_selector('#route-tags-text')
        tags_field.send_keys(tags)

    private_checkbox = driver.find_element_by_css_selector('#private_checkbox')
    is_checked = private_checkbox.get_attribute('checked') == 'true'
    if is_checked == public:
        private_checkbox.click()

    if use_with_watch:
        try:
            devices = driver.find_element_by_css_selector('#routeDeviceList')
            for device_checkbox in devices.find_elements_by_tag_name('input'):
                is_checked = device_checkbox.get_attribute('checked') == 'true'
                if not is_checked:
                    actions = ActionChains(driver)
                    actions.move_to_element(device_checkbox).perform()
                    driver.execute_script(
                        "arguments[0].click();", device_checkbox)
        except Exception:
            print('Was not able to set "use with watch"')

    driver.find_element_by_css_selector('#saveRouteBtn').click()

    sleep(10)


if __name__ == '__main__':
    import_routes()
