from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://proxy6.net/"
LOGIN = 'tzpythondemo@domconnect.ru'
PASSWORD = 'rNCV14la'

# Запуск Chrome
driver = webdriver.Chrome()

try:
    # Открытие страницы
    driver.get(URL)

    # Ожидание появления кнопки "Войти" и её нажатие
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-role='login']"))
    )
    login_button.click()

    # Ожидание появления формы входа
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )

    # Заполнение полей логина и пароля
    email_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'password')
    email_input.send_keys(LOGIN)
    password_input.send_keys(PASSWORD)

    # Работа с reCAPTCHA
    try:
        # Ожидание появления iframe reCAPTCHA и переключение в него
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']"))
        )

        # Ожидание прохождения reCAPTCHA (aria-checked становится "true")
        WebDriverWait(driver, 300).until(
            EC.text_to_be_present_in_element_attribute(
                (By.ID, "recaptcha-anchor"), "aria-checked", "true"
            )
        )

        driver.switch_to.default_content()  # Возвращение в основной контекст страницы
    except Exception as e:
        print("Ошибка при работе с reCAPTCHA:", e)

    # Нажатие кнопки "Войти"
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@class='ndbox-inner' and @id='ndbox-1']//form[@id='form-login']//button[@type='submit']"
            ))
        )
        submit_button.click()

    except Exception as e:
        print("Ошибка при нажатии кнопки 'Войти':", e)

    # Ожидание загрузки страницы "Прокси"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'user_proxy_table'))
    )

    # Парсинг таблицы
    rows = driver.find_elements(
        By.XPATH, "//table[@class='table user_proxy_table']/tbody/tr[not(@class='active')]"
    )

    proxys = []

    for row in rows:
        try:
            # Проверка наличия прокси в строке
            proxy_elements = row.find_elements(By.XPATH, ".//div[contains(@class, 'right')][b]")
            if not proxy_elements:
                continue  # Пропуск строки без прокси

            # Извлечение прокси (IP:PORT)
            proxy = proxy_elements[0].text

            # Проверка наличия даты
            date_elements = row.find_elements(
                By.XPATH, ".//td[@class='mobile-hide']//div[contains(@class, 'right color-success')]"
            )
            # Извлечение даты окончания
            date = date_elements[0].text if date_elements else "Дата не указана"

            result = f"{proxy} - {date}"
            proxys.append(result)

            # Печать результата
            print(result)

        except Exception as e:
            print("Ошибка обработки строки:", e)

    if not proxys:
        print("Прокси не найдены")

except Exception as main_error:
    print("Произошла ошибка:", main_error)

finally:
    # Закрытие браузера
    driver.quit()
