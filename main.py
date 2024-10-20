from src.api import Parser
from src.config import config
from src.creator_db import DBCreator
from src.manager_db import DBManager
from src.ui import ui
from src.utils import read_json

if __name__ == '__main__':
    print("Вас приветствует программа для поиска вакансий с сайта hh.ru")

    params = config()
    db_name = "vacancies_hh"
    db = DBCreator(db_name, params)
    db.create_database()
    file_with_companies = "data/companies_data.json"
    companies = read_json(file_with_companies)

    employers = []
    vacancies = []

    for company in companies:
        print(f"Загрузка данных о вакансиях для компании: {company["name"]}")
        employers.append(Parser.load_employer_data(company.get("id")))

        vacancies.extend(Parser.load_vacancies(company.get("id")))

    db.save_data_to_db(employers, vacancies)

    print("Данные успешно записаны в БД")

    print('*' * 10)

    db = DBManager(db_name, params)
    companies = db.get_companies_and_vacancies_count()
    print()
    print("Название компании       Количество вакансий в БД")
    for company in companies:
        print(f"{company["company_name"]:<23}", company["vacancies_count"])
    print()

    ui(db_name, params)
