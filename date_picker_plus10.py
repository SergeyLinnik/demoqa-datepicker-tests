"""
Тест для https://demoqa.com/date-picker
Вычисляет дату +10 дней от текущей и вводит её в поле выбора даты.
Исправлена проблема с очисткой поля через комбинацию методов.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time


def get_future_date(days_offset: int = 10) -> str:
    """
    Возвращает дату в формате MM/DD/YYYY, которая на days_offset дней позже текущей.
    
    :param days_offset: количество дней для добавления (по умолчанию 10)
    :return: строка с датой в формате MM/DD/YYYY
    """
    today: datetime = datetime.now()
    future_date: datetime = today + timedelta(days=days_offset)
    return future_date.strftime("%m/%d/%Y")


def force_clear_input_field(element: WebElement) -> None:
    """
    Принудительно очищает поле ввода несколькими способами.
    Комбинация методов для обхода React-обработчиков.
    
    :param element: поле ввода для очистки
    """
    # Способ 1: Клик в поле для фокуса
    element.click()
    time.sleep(0.1)
    
    # Способ 2: Выделить весь текст (Ctrl+A)
    element.send_keys(Keys.CONTROL + "a")
    time.sleep(0.1)
    
    # Способ 3: Удалить выделенное (Delete)
    element.send_keys(Keys.DELETE)
    time.sleep(0.1)
    
    # Способ 4: Дополнительная очистка через Backspace
    element.send_keys(Keys.BACKSPACE)
    time.sleep(0.1)


def clear_with_js_and_backspace(driver: webdriver.Chrome, element: WebElement) -> None:
    """
    Очистка через комбинацию JavaScript и клавиш.
    Самый надёжный метод для React-полей.
    
    :param driver: экземпляр WebDriver
    :param element: поле ввода для очистки
    """
    # Сначала кликаем для фокуса
    element.click()
    time.sleep(0.1)
    
    # Очищаем через JavaScript
    driver.execute_script("arguments[0].value = '';", element)
    time.sleep(0.1)
    
    # Триггерим событие input, чтобы React понял, что значение изменилось
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
    time.sleep(0.1)
    
    # Дополнительно отправляем Backspace на всякий случай
    element.send_keys(Keys.BACKSPACE)
    time.sleep(0.1)


def test_date_picker_plus10() -> None:
    """
    Основной тест: открыть страницу, ввести дату +10 дней, проверить ввод.
    Каждый шаг имеет осмысленное assert сообщение.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    
    try:
        # ШАГ 1: ОТКРЫТИЕ СТРАНИЦЫ
        print("Шаг 1: Открытие страницы https://demoqa.com/date-picker")
        driver.get("https://demoqa.com/date-picker")
        
        # Проверка: страница загрузилась (ждём появления поля ввода)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "datePickerMonthYearInput"))
            )
        except TimeoutException:
            raise AssertionError(
                "Страница не загрузилась корректно. Поле ввода с ID 'datePickerMonthYearInput' не найдено."
            )
        print("Страница успешно загружена")
        
        # ШАГ 2: ПОИСК ПОЛЯ ВВОДА
        print("Шаг 2: Поиск поля ввода даты (ID = 'datePickerMonthYearInput')")
        date_input: WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "datePickerMonthYearInput"))
        )
        
        assert date_input.is_displayed(), \
            "Поле ввода даты с ID 'datePickerMonthYearInput' найдено, но не отображается на странице"
        print("Поле ввода даты найдено и отображается")
        
        # ШАГ 3: ОЧИСТКА ПОЛЯ (комбинированным методом)
        print("Шаг 3: Очистка поля ввода перед вводом новой даты")
        
        old_value_before_clear = date_input.get_attribute("value")
        print(f"  Значение до очистки: '{old_value_before_clear}'")
        
        # Используем самый надёжный метод очистки
        clear_with_js_and_backspace(driver, date_input)
        
        # Проверка: поле успешно очистилось
        value_after_clear = date_input.get_attribute("value")
        assert value_after_clear == "", \
            f"Поле ввода не очистилось. После очистки содержит: '{value_after_clear}'. Было: '{old_value_before_clear}'"
        print("Поле успешно очищено")
        
        # ШАГ 4: РАСЧЁТ БУДУЩЕЙ ДАТЫ
        print("Шаг 4: Расчёт даты +10 дней от текущей")
        future_date: str = get_future_date(10)
        
        assert len(future_date) == 10, \
            f"Некорректный формат даты: '{future_date}'. Ожидается формат MM/DD/YYYY (10 символов)"
        assert future_date.count("/") == 2, \
            f"Некорректный формат даты: '{future_date}'. Ожидается разделитель '/'"
        print(f"Рассчитана дата +10 дней: {future_date}")
        
        # ШАГ 5: ВВОД НОВОЙ ДАТЫ
        print("Шаг 5: Ввод рассчитанной даты в поле")
        
        # Вводим дату посимвольно для надёжности
        for char in future_date:
            date_input.send_keys(char)
            time.sleep(0.05)
        
        time.sleep(0.3)
        
        # Проверка: дата введена
        value_after_input = date_input.get_attribute("value")
        assert value_after_input != "", \
            f"После ввода даты поле осталось пустым. Ожидалось: '{future_date}'"
        print(f"Дата '{future_date}' введена в поле")
        
        # ШАГ 6: ПРОВЕРКА ПРАВИЛЬНОСТИ ВВОДА
        print("Шаг 6: Проверка, что введена правильная дата")
        
        entered_value: str = date_input.get_attribute("value")
        
        print(f"  Ожидалось: '{future_date}'")
        print(f"  Получено:  '{entered_value}'")
        
        # Если значение содержит старую дату (склеилось), пробуем очистить ещё раз
        if len(entered_value) > len(future_date):
            print("  Обнаружено склеивание дат, повторная очистка...")
            
            # Более агрессивная очистка
            date_input.click()
            date_input.clear()
            driver.execute_script("arguments[0].value = '';", date_input)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", date_input)
            time.sleep(0.3)
            
            # Проверяем, что очистилось
            value_after_second_clear = date_input.get_attribute("value")
            print(f"  После повторной очистки: '{value_after_second_clear}'")
            
            # Вводим дату заново
            date_input.send_keys(future_date)
            time.sleep(0.3)
            entered_value = date_input.get_attribute("value")
            print(f"  После повторного ввода: '{entered_value}'")
        
        assert entered_value == future_date, \
            f"Несовпадение даты!\n" \
            f"  Ожидалось: '{future_date}'\n" \
            f"  Получено:  '{entered_value}'"
        
        print("Дата в поле полностью совпадает с ожидаемой")
        
        # ШАГ 7: ФИКСАЦИЯ ДАТЫ
        print("Шаг 7: Фиксация даты (нажатие Enter)")
        date_input.send_keys(Keys.ENTER)
        time.sleep(0.3)
        
        final_value = date_input.get_attribute("value")
        assert final_value == future_date, \
            f"После нажатия Enter значение изменилось! Было: '{entered_value}', стало: '{final_value}'"
        print("Дата зафиксирована")
        
        # ВСЕ ТЕСТЫ ПРОЙДЕНЫ
        print("\n" + "="*50)
        print("ТЕСТ ПРОЙДЕН УСПЕШНО")
        print("Дата +10 дней (" + future_date + ") успешно установлена в поле")
        print("="*50)
        
    except AssertionError as e:
        print("\nОШИБКА ПРОВЕРКИ: " + str(e))
        print("\nДетали для отладки:")
        print("  URL: " + driver.current_url)
        print("  Заголовок страницы: " + driver.title)
        raise
        
    except WebDriverException as e:
        print("\nОШИБКА ДРАЙВЕРА: " + str(e))
        raise
        
    except Exception as e:
        print("\nНЕПРЕДВИДЕННАЯ ОШИБКА: " + str(e))
        raise
        
    finally:
        print("\nЗакрытие браузера...")
        driver.quit()
        print("Браузер закрыт")


if __name__ == "__main__":
    test_date_picker_plus10()