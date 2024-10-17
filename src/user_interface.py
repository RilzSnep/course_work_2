import os
import json
from src.api import HHAPI  # Импорт класса HHAPI
from src.models import Vacancy
from src.storage import JSONVacancyStorage, get_top_n_vacancies


def user_interaction():
    # Очищаем файл, чтобы сохранить только актуальные данные при новом запуске
    open("src/for_vacancies.json", "w").close()
    hh_api = HHAPI()
    vacancy_storage = JSONVacancyStorage()

    # Имя файла: for_vacancies.json
    filename = "src/for_vacancies.json"

    # Если файл еще не был создан, создаем пустой файл
    if not os.path.exists(filename):
        open(filename, "w").write('[]')

    # 1. Получаем вакансии по запросу и сохраняем в src/for_vacancies.json
    query = input("Введите поисковый запрос: ")
    try:
        # Получаем данные вакансий по запросу
        vacancies_data = hh_api.get_vacancies({'text': query})

        for item in vacancies_data:
            title = item['name']
            area = item['area']['name'] if 'area' in item else "Город не указан"
            salary_info = item.get('salary')
            salary_from = salary_info['from'] if salary_info and salary_info['from'] is not None else 'Не указана'
            salary_to = salary_info['to'] if salary_info and salary_info['to'] is not None else 'Не указана'
            currency = salary_info['currency'] if salary_info and 'currency' in salary_info else 'Не указана'
            snippet_info = item.get('snippet')
            description = snippet_info[
                'responsibility'] if snippet_info and 'responsibility' in snippet_info else 'Нет описания'

            vacancy = Vacancy(title, area, salary_from, salary_to, currency, description)
            vacancy_storage.add_vacancy(vacancy)

        # Сохраняем вакансии в файл
        vacancy_storage.save_to_file(filename)
        print(f"Добавлено {len(vacancies_data)} вакансий и сохранено в файл: {filename}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # 2. Получаем топ N вакансий по зарплате
    n = input("Введите количество вакансий для отображения в топе по зарплате (или нажмите Enter, чтобы пропустить): ")
    get_top_n_vacancies("src/for_vacancies.json", n)

    # 3. Найти вакансии по ключевому слову в описании
    keyword = input("Введите ключевое слово для поиска в описании (или нажмите Enter, чтобы пропустить): ")
    if keyword:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            vacancy_storage.vacancies = [Vacancy(**v) for v in data]
            filtered_vacancies = [v for v in vacancy_storage.vacancies if
                                  v.description and keyword.lower() in v.description.lower()]
            if filtered_vacancies:
                print(f"Найдено {len(filtered_vacancies)} вакансий с ключевым словом '{keyword}':")
                for v in filtered_vacancies:
                    print(v)
            else:
                print(f"Не найдено вакансий с ключевым словом '{keyword}'.")
        except Exception as e:
            print(f"Произошла ошибка при загрузке файла: {e}")
