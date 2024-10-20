import psycopg2


class DBCreator:
    """Class to create DB"""

    def __init__(self, db_name: str, params: dict) -> None:
        """Initialisation"""

        self.__db_name = db_name
        self.__params = params

    def create_database(self) -> None:
        """Method to create DB"""

        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.__db_name}")
        cur.execute(f"CREATE DATABASE {self.__db_name}")

        conn.close()

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers(
                employer_id INT PRIMARY KEY,
                company_name VARCHAR,
                open_vacancies INT,
                accredited_it_employer BOOL,
                site_url VARCHAR,
                description TEXT
                )
                """
            )
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies(
                vacancy_id INT PRIMARY KEY,
                employer_id INT,
                vacancy_name VARCHAR,
                salary_from INT,
                salary_to INT,
                url VARCHAR,
                CONSTRAINT fk_vacancies_employer FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                )
                """
            )
        conn.commit()
        conn.close()

    def save_data_to_db(self, employers: list[dict], vacancies: list[dict]) -> None:
        """Saving data to employers table"""

        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        for employer in employers:
            cur.execute(
                """
                INSERT INTO employers (employer_id, company_name, open_vacancies,
                                        accredited_it_employer, site_url, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    employer.get("id"),
                    employer.get("name"),
                    employer.get("open_vacancies"),
                    employer.get("accredited_it_employer"),
                    employer.get("site_url"),
                    employer.get("description"),
                ),
            )

        for vacancy in vacancies:
            try:
                if not vacancy["salary"]:
                    salary_from = 0
                    salary_to = 0
                else:
                    salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                    salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0

                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary_from, salary_to, url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        int(vacancy["id"]),
                        vacancy["employer"]["id"],
                        vacancy["name"],
                        salary_from,
                        salary_to,
                        vacancy["alternate_url"],
                    ),
                )
            except psycopg2.errors.UniqueViolation:
                pass

        conn.close()
