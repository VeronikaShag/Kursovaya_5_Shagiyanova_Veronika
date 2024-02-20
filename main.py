from classes.db_manager import DBManager
from utils.utils import create_database, create_tables, insert_data_info_tables


if __name__ == '__main__':
    print('Выберите действие:\n'
          '1 - вывести список всех компаний и количество вакансий у каждой компании\n'
          '2 - вывести список всех вакансий с указанием названия компании, названия вакансии и зарплаты '
          'и ссылки на вакансию\n'
          '3 - вывести среднюю зарплату по вакансиям\n'
          '4 - вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
          '5 - список всех вакансий, в названии которых содержатся переданные в метод слова, например python\n')

    # работа с БД
    create_database('hh')
    create_tables('hh')
    insert_data_info_tables('hh')
    db = DBManager('hh')

    answer = int(input('Выбор: '))

    if answer == 1:
        for i in db.get_companies_and_vacancies_count():
            print(f'{i[0]} - {i[1]}')

    elif answer == 2:
        for i in db.get_all_vacancies():
            print(f'{i[0]} - {i[1]} - ЗП от {i[2]} до {i[3]} - {i[4]}')

    elif answer == 3:
        print(db.get_avg_salary())

    elif answer == 4:
        for i in db.get_vacancies_with_higher_salary():
            print(f'{i[0]} - ЗП {i[1]}')

    elif answer == 5:
        keyword = input('Введите слово для поиска: ')
        print(db.get_vacancies_with_keyword(keyword))


