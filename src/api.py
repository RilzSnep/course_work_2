from abc import ABC, abstractmethod
import requests


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
