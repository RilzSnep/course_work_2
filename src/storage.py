from abc import ABC, abstractmethod
from src.models import Vacancy
import json


def get_top_n_vacancies(file_path, n):
    try:
        n = int(n)  # Преобразуем n в целое число
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Сортируем вакансии по максимальной зарплате (salary_to)
        top_vacancies = sorted(
            data,
            key=lambda x: (x['salary_to'] if isinstance(x['salary_to'], (int, float)) else 0),
            reverse=True
        )[:n]

        # Перезаписываем файл только с топ N вакансиями
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(top_vacancies, file, ensure_ascii=False, indent=4)
    except ValueError:
        print("Ошибка: n должно быть числом.")
    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy):
        pass

    @abstractmethod
    def filter_by_salary(self, min_salary):
        pass

    @abstractmethod
    def save_to_file(self, filename):
        pass

    @abstractmethod
    def load_from_file(self, filename):
        pass


# Допустим, что ваш конструктор Vacancy выглядит так:
# Vacancy(self, name, area, salary_from, salary_to, currency, description)

class JSONVacancyStorage:
    def __init__(self):
        # Инициализируем список вакансий
        self.vacancies = []

    def load_from_file(self, filename):
        # Проверка на существование файла и загрузка данных
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Добавляем вакансии в список
        self.vacancies = []
        for v in data['items']:
            salary = {
                'from': v['salary']['from'] if v.get('salary') else None,
                'to': v['salary']['to'] if v.get('salary') else None
            }
            currency = v['salary']['currency'] if v.get('salary') else 'Не указано'
            area = v['area']['name'] if v.get('area') else 'Не указано'
            description = v['snippet'].get('responsibility') if v.get('snippet') and v['snippet'].get(
                'responsibility') else 'Нет описания'

            vacancy = Vacancy(v['name'], area, salary['from'], salary['to'], currency, description)
            self.vacancies.append(vacancy)

    def add_vacancy(self, vacancy):
        self.vacancies.append(vacancy)

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([vacancy.__dict__ for vacancy in self.vacancies], file, ensure_ascii=False, indent=4)
