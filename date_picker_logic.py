"""
Модуль с бизнес-логикой для работы с date picker на demoqa.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time


class DatePickerLogic:
    """Класс для работы с полем выбора даты"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.date_input_locator = (By.ID, "datePickerMonthYearInput")
    
    def open_page(self) -> None:
        """Открывает страницу date-picker"""
        self.driver.get("https://demoqa.com/date-picker")
    
    def wait_for_page_load(self, timeout: int = 10) -> None:
        """Ожидает загрузки страницы"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.date_input_locator)
        )
    
    def get_date_input_field(self) -> WebElement:
        """Находит и возвращает поле ввода даты"""
        date_input = self.driver.find_element(*self.date_input_locator)
        assert date_input.is_displayed(), "Поле ввода даты не отображается"
        return date_input
    
    def get_field_value(self) -> str:
        """Возвращает текущее значение поля ввода"""
        return self.get_date_input_field().get_attribute("value")
    
    def clear_field_aggressive(self) -> None:
        """Агрессивная очистка поля ввода для React-полей"""
        date_input = self.get_date_input_field()
        
        date_input.click()
        time.sleep(0.1)
        date_input.send_keys(Keys.CONTROL + "a")
        time.sleep(0.1)
        date_input.send_keys(Keys.DELETE)
        time.sleep(0.1)
        
        self.driver.execute_script("arguments[0].value = '';", date_input)
        time.sleep(0.1)
        
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
            date_input
        )
        time.sleep(0.1)
        
        date_input.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)
    
    def set_date(self, date_value: str) -> None:
        """Устанавливает дату в поле ввода"""
        date_input = self.get_date_input_field()
        self.clear_field_aggressive()
        
        for char in date_value:
            date_input.send_keys(char)
            time.sleep(0.05)
        time.sleep(0.3)
    
    def confirm_date(self) -> None:
        """Подтверждает дату нажатием Enter"""
        self.get_date_input_field().send_keys(Keys.ENTER)
        time.sleep(0.3)
    
    def is_field_empty(self) -> bool:
        """Проверяет, пустое ли поле"""
        return self.get_field_value() == ""
    
    def is_date_correct(self, expected_date: str) -> tuple:
        """Проверяет соответствие значения поля ожидаемой дате"""
        actual_value = self.get_field_value()
        return (actual_value == expected_date, actual_value)
    
    def retry_set_date_if_needed(self, expected_date: str, max_retries: int = 2) -> None:
        """Устанавливает дату с повторной попыткой при склеивании"""
        for attempt in range(max_retries):
            self.set_date(expected_date)
            is_correct, actual_value = self.is_date_correct(expected_date)
            
            if is_correct:
                return
            
            if len(actual_value) > len(expected_date):
                print(f"  Попытка {attempt + 1}: обнаружено склеивание, повтор...")
        
        _, actual_value = self.is_date_correct(expected_date)
        raise AssertionError(
            f"Несовпадение даты после {max_retries} попыток!\n"
            f"  Ожидалось: '{expected_date}'\n"
            f"  Получено:  '{actual_value}'"
        )


def get_future_date(days_offset: int = 10) -> str:
    """Возвращает дату +N дней в формате MM/DD/YYYY"""
    future_date = datetime.now() + timedelta(days=days_offset)
    return future_date.strftime("%m/%d/%Y")


def validate_date_format(date_str: str) -> bool:
    """Проверяет формат даты MM/DD/YYYY"""
    if len(date_str) != 10:
        return False
    if date_str.count("/") != 2:
        return False
    return True