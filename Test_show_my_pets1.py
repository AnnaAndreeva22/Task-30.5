import pytest
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://google.com')


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/seleniumdriver/chromedriver.exe')

    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('***')
    
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('***')

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()


    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').text == "Мои питомцы"

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))

    driver.implicitly_wait(10)

    # Проверяем, что присутствуют все питомцы
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    number_of_my_pets = 6

    if len(all_pets) == number_of_my_pets:
        print('Присутствуют все питомцы')
    else:
        print('Количество разное')

    print(len(all_pets))


    # Хотя бы у половины питомцев есть фото

    driver.implicitly_wait(10)

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//img[contains(@src, "data:image")]')))

    pets_images = pytest.driver.find_elements(By.XPATH, '//img[contains(@src, "data:image")]')

    print(len(pets_images))

    if len(pets_images) >= (number_of_my_pets/2):
        print('Хотя бы у половины питомцев есть фото')
    else:
        print('Фото меньше чем у половины питомцев')

    # У всех питомцев есть имя возраст и порода

    driver.implicitly_wait(10)

    pets_descr = pytest.driver.find_elements(By.XPATH, '//td[contains(text(), "")]')

    WebDriverWait(pytest.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[contains(@title, "Удалить питомца")]' )))

    pets_del_marks = pytest.driver.find_elements(By.XPATH, '//div[contains(@title, "Удалить питомца")]')

    descr = len(pets_descr)
    del_marks = len(pets_del_marks)

    print(descr)
    print(del_marks)

    number_of_descr = 3

    if number_of_my_pets*number_of_descr == descr - del_marks:
        print('У всех питомцев есть имя, возраст и порода')
    else:
        print('Описание есть не у всех животных')
