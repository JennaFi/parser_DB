from src.manager_db import DBManager


def ui(db_name, params) -> None:
    """User interaction form"""

    db_manager = DBManager(db_name, params)

    print("Выберите действие: ")
    print("1. Получить список всех вакансий")
    print("2. Получить среднюю зарплату по вакансиям")
    print("3. Получить список всех вакансий, у которых зарплата выше средней")
    print("4. Получить список всех вакансий по ключевому слову")

    choice = input("Введите номер требуемого действия от 1 до 4: ")

    match choice:
        case "1":
            vacancies = db_manager.get_all_vacancies()
            print_vacancies(vacancies)

        case "2":
            print(db_manager.get_avg_salary())

        case "3":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print_vacancies(vacancies)

        case "4":
            keyword = input("Введите слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print_vacancies(vacancies)


def print_vacancies(vacancies: list) -> None:
    """Printing out vacancies data"""

    print("Название компании  Название вакансии", " " * 35, "Зарплата ОТ   Зарплата ДО   Ссылка на вакансию")
    for i in range(len(vacancies)):
        vacancy = vacancies[i]
        company = vacancy["company_name"]
        name = vacancy["vacancy_name"]
        salary_from = "Не указана" if vacancy["salary_from"] == 0 else vacancy["salary_from"]
        salary_to = "Не указана" if vacancy["salary_to"] == 0 else vacancy["salary_to"]
        url = vacancy["url"]
        print(
            f"{company:<15}", "  ", f"{name[0:50]:<50}", "  ", f"{str(salary_from):<13}", f"{str(salary_to):<13}", url
        )
