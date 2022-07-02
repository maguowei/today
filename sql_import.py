import os
import json
import sqlite3


JSON_DATA_PATH = 'data/feeds/json'


def sql_import():
    conn = sqlite3.connect('today.db')
    c = conn.cursor()

    table_create_sql = 'CREATE TABLE IF NOT EXISTS feed (id INTEGER PRIMARY KEY AUTOINCREMENT, data json)'
    c.execute(table_create_sql)

    sql = 'INSERT INTO feed (data) VALUES (?)'

    for file in os.listdir(JSON_DATA_PATH):
        filepath = f'{JSON_DATA_PATH}/{file}'
        with open(filepath) as f:
            print(f'process file: {filepath}')
            data = json.load(f)
            for feed in data:
                c.execute(sql, (json.dumps(feed, ensure_ascii=False),))

            conn.commit()


if __name__ == '__main__':
    sql_import()
