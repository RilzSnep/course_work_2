from abc import ABC, abstractmethod
import requests


# src/models.py

class Vacancy:
    def __init__(self, name, area, salary_from, salary_to, currency, description):
        self.name = name
        self.area = area
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.description = description

    def __lt__(self, other):
        # Сравнение по максимальной зарплате (salary_to), если она есть, иначе по минимальной (salary_from)
        self_salary = self.salary_to if self.salary_to else self.salary_from
        other_salary = other.salary_to if other.salary_to else other.salary_from

        if self_salary is None:
            return True
        if other_salary is None:
            return False

        return self_salary < other_salary

    def __str__(self):
        salary_range = f"{self.salary_from} - {self.salary_to} {self.currency}" if self.salary_from and self.salary_to else "Зарплата не указана"
        return f"Вакансия: {self.name}, Зарплата: {salary_range}, Город: {self.area}, Описание: {self.description}"


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, params=None):
        pass


class HHAPI(VacancyAPI):
    BASE_URL = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, params=None):
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            raise Exception(f'Error fetching vacancies: {response.status_code}')
