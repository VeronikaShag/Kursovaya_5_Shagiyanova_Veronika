import psycopg2

from utils.config import config


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query) -> list:
        """Возвращает результат запроса"""
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()

        return result

    def all_data(self):
        """Вывод данных из таблицы"""
        result = self.execute_query('SELECT * FROM employers')
        return result

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        result = self.execute_query('SELECT employers.name, COUNT(*) FROM vacancies '
                                    'INNER JOIN employers ON vacancies.employer = employers.id '
                                    'GROUP BY employers.name')
        return result

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию"""
        result = self.execute_query('SELECT vacancies.name, employers.name, salary_from, salary_to, url FROM vacancies '
                                    'INNER JOIN employers ON vacancies.employer = employers.id')
        return result

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        result = self.execute_query('SELECT AVG((salary_from + salary_to)/2) FROM vacancies')
        return int(result[0][0])

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        result = self.execute_query('SELECT name, ((salary_from + salary_to)/2) FROM vacancies '
                                    'WHERE ((salary_from + salary_to)/2) >= (SELECT AVG((salary_from + salary_to)/2) '
                                    'FROM vacancies)')
        return result

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT name, salary_from, salary_to, url FROM vacancies 
        WHERE name LIKE  (%s)""", (f'%{keyword}%'))
                result = cur.fetchall()
        conn.close()

        return result

        # result = self.execute_query(f"""SELECT name, salary_from, salary_to, url FROM vacancies
        # WHERE name LIKE  (%s)""", (f'%{keyword}%'))
        # return result


# db = DBManager('lk')
# print(db.get_vacancies_with_keyword('Ozon'))
