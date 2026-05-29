"""
Модуль с бизнес-логикой для работы с горизонтальным слайдером
Сайт: https://the-internet.herokuapp.com/horizontal_slider
Использует стрелки, так как они работают предсказуемо на этом сайте
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class HorizontalSliderLogic:
    """Класс для управления горизонтальным слайдером"""

    def __init__(self, driver):
        self.driver = driver
        self.slider_locator = (By.CSS_SELECTOR, "input[type='range']")
        self.value_locator = (By.ID, "range")

    def open_page(self) -> None:
        """Открывает страницу с горизонтальным слайдером"""
        self.driver.get("https://the-internet.herokuapp.com/horizontal_slider")

    def wait_for_slider(self, timeout: int = 10) -> None:
        """Ожидает появления ползунка на странице"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.slider_locator)
        )

    def get_slider(self) -> WebElement:
        """Возвращает элемент ползунка"""
        return self.driver.find_element(*self.slider_locator)

    def get_displayed_value(self) -> float:
        """Возвращает числовое значение, отображаемое на странице"""
        value_element = self.driver.find_element(*self.value_locator)
        return float(value_element.text)

    def move_slider_with_arrow_keys(self, target_value: float) -> None:
        """
        Перемещает ползунок стрелками до достижения целевого значения
        Один шаг стрелкой = 0.5
        """
        slider = self.get_slider()
        slider.click()
        
        current_value = self.get_displayed_value()
        
        # Определяем направление и количество шагов
        if target_value > current_value:
            steps = int((target_value - current_value) / 0.5)
            key = Keys.ARROW_RIGHT
        else:
            steps = int((current_value - target_value) / 0.5)
            key = Keys.ARROW_LEFT
        
        # Выполняем необходимое количество нажатий
        for _ in range(steps):
            slider.send_keys(key)
            time.sleep(0.05)
        
        time.sleep(0.3)