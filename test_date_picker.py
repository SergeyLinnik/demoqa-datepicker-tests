"""
Тесты для страницы https://demoqa.com/date-picker
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from date_picker_logic import DatePickerLogic, get_future_date, validate_date_format


def setup_driver() -> webdriver.Chrome:
    """Настройка и запуск драйвера Chrome"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def test_date_picker_plus10() -> None:
    """Основной тест: ввести дату +10 дней"""
    driver = None
    
    try:
        print("Шаг 1: Запуск браузера")
        driver = setup_driver()
        print("Браузер запущен")
        
        print("Шаг 2: Инициализация DatePickerLogic")
        date_picker = DatePickerLogic(driver)
        
        print("Шаг 3: Открытие страницы")
        date_picker.open_page()
        
        print("Шаг 4: Ожидание загрузки")
        try:
            date_picker.wait_for_page_load()
        except TimeoutException:
            raise AssertionError("Страница не загрузилась")
        print("Страница загружена")
        
        print("Шаг 5: Расчёт даты +10 дней")
        future_date = get_future_date(10)
        assert validate_date_format(future_date), "Неверный формат даты"
        print(f"Дата +10 дней: {future_date}")
        
        print("Шаг 6: Установка даты")
        date_picker.retry_set_date_if_needed(future_date)
        print(f"Дата '{future_date}' установлена")
        
        print("Шаг 7: Проверка даты")
        is_correct, actual_value = date_picker.is_date_correct(future_date)
        print(f"  Ожидалось: '{future_date}'")
        print(f"  Получено:  '{actual_value}'")
        assert is_correct, f"Несовпадение даты! Получено: '{actual_value}'"
        print("Дата совпадает")
        
        print("Шаг 8: Фиксация даты")
        date_picker.confirm_date()
        
        print("\n" + "="*50)
        print("ТЕСТ ПРОЙДЕН УСПЕШНО")
        print("="*50)
        
    except AssertionError as e:
        print(f"\nОШИБКА: {e}")
        raise
    except Exception as e:
        print(f"\nОШИБКА: {e}")
        raise
    finally:
        if driver:
            print("\nЗакрытие браузера...")
            driver.quit()


if __name__ == "__main__":
    test_date_picker_plus10()