from typing import Any

import psycopg2

from src.config import config


class DBManager:
    """Class to get vacancies data from database"""

    def __init__(self, db_name: str, params: dict) -> None:
        """Initialisation"""

        self.__db_name = db_name
        self.__params = params

    def __query_execute(self, query: str) -> list[dict | Any]:
        """Private method to get a query"""

        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                columns = [column[0] for column in cur.description]
                result = cur.fetchall()
                result_in_dict = [dict(zip(columns, i)) for i in result]

        conn.close()

        return result_in_dict

    def get_employers(self) -> Any:
        """Method to get employers data from DB"""

        return self.__query_execute("SELECT * FROM employers")

    def get_companies_and_vacancies_count(self) -> Any:
        """Method to get list of all the companies and the employers from BD"""

        query = """
            SELECT employers.company_name, COUNT(*) AS vacancies_count
            FROM vacancies
            JOIN employers USING(employer_id)
            GROUP BY employers.company_name
            """

        return self.__query_execute(query)

    def get_all_vacancies(self) -> Any:
        """Method to get list of all vacancies with company name, vacancy name, salary and link to vacancy"""

        query = """
            SELECT employers.company_name, vacancy_name, salary_from, salary_to, url
            FROM vacancies
            JOIN employers USING(employer_id)
            """

        return self.__query_execute(query)

    def get_avg_salary(self) -> Any:
        """Method to get average salary"""

        query = """
            SELECT AVG (salary_to)
            FROM vacancies
            WHERE salary_to > 0
            """

        return round(self.__query_execute(query)[0]["avg"], 2)

    def get_vacancies_with_higher_salary(self) -> Any:
        """Method to get vacancy with the highest salary"""

        query = """
            SELECT employers.company_name, vacancy_name, salary_from, salary_to, url
            FROM vacancies
            JOIN employers USING(employer_id)
            WHERE salary_from > (
            SELECT AVG (salary_from)
            FROM vacancies
            WHERE salary_to > 0
            )
            """

        return self.__query_execute(query)

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Method to get list of vacancies by keyword"""

        query = f"""
            SELECT employers.company_name, vacancy_name, salary_from, salary_to, url
            FROM vacancies
            JOIN employers USING(employer_id)
            WHERE vacancy_name LIKE '%{keyword}%'
            """

        return self.__query_execute(query)
