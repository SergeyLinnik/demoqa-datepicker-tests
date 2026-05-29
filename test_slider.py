"""
Тест для горизонтального слайдера
Сайт: https://the-internet.herokuapp.com/horizontal_slider
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from slider_logic import HorizontalSliderLogic


def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def test_horizontal_slider():
    driver = None
    try:
        print("1. Запуск браузера")
        driver = setup_driver()

        print("2. Инициализация логики слайдера")
        slider_page = HorizontalSliderLogic(driver)

        print("3. Открытие страницы")
        slider_page.open_page()

        print("4. Ожидание загрузки слайдера")
        slider_page.wait_for_slider()

        initial_value = slider_page.get_displayed_value()
        print(f"   Начальное значение: {initial_value}")
        assert initial_value == 0.0, f"Начальное значение должно быть 0.0, получено {initial_value}"

        print("5. Перемещение слайдера на значение 2.5")
        slider_page.move_slider_with_arrow_keys(2.5)
        
        displayed_value = slider_page.get_displayed_value()
        print(f"   Отображаемое значение: {displayed_value}")
        
        assert abs(displayed_value - 2.5) < 0.1, \
            f"Ошибка: ожидалось 2.5, получено {displayed_value}"
        print("6. Значение 2.5 установлено корректно")

        print("7. Перемещение слайдера на значение 4.0")
        slider_page.move_slider_with_arrow_keys(4.0)
        
        displayed_value = slider_page.get_displayed_value()
        print(f"   Отображаемое значение: {displayed_value}")
        
        assert abs(displayed_value - 4.0) < 0.1, \
            f"Ошибка: ожидалось 4.0, получено {displayed_value}"
        print("8. Значение 4.0 установлено корректно")

        print("9. Перемещение слайдера на значение 1.0")
        slider_page.move_slider_with_arrow_keys(1.0)
        
        displayed_value = slider_page.get_displayed_value()
        print(f"   Отображаемое значение: {displayed_value}")
        
        assert abs(displayed_value - 1.0) < 0.1, \
            f"Ошибка: ожидалось 1.0, получено {displayed_value}"
        print("10. Значение 1.0 установлено корректно")

        print("\n" + "=" * 50)
        print("ТЕСТ ПРОЙДЕН УСПЕШНО")
        print("=" * 50)

    except AssertionError as e:
        print(f"\nОШИБКА ПРОВЕРКИ: {e}")
        raise
    except Exception as e:
        print(f"\nОШИБКА: {e}")
        raise
    finally:
        if driver:
            print("\nЗакрытие браузера...")
            driver.quit()


if __name__ == "__main__":
    test_horizontal_slider()