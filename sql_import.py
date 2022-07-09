#!/usr/bin/env python3

import os
import json
import sqlite3
from utils.logger import logger


JSON_DATA_PATH = 'data/feeds/json'


def sql_import():
    conn = sqlite3.connect('today.db')
    c = conn.cursor()

    table_create_sql = 'CREATE TABLE IF NOT EXISTS feed (id INTEGER PRIMARY KEY AUTOINCREMENT, data json, archive_date date)'
    c.execute(table_create_sql)

    sql = 'INSERT INTO feed (data, archive_date) VALUES (?, ?)'

    for file in sorted(os.listdir(JSON_DATA_PATH)):
        filepath = f'{JSON_DATA_PATH}/{file}'
        with open(filepath) as f:
            logger.info(f'process file: {filepath}')
            data = json.load(f)
            for feed in data:
                c.execute(sql, (json.dumps(feed, ensure_ascii=False), file.rstrip('.json')))

            conn.commit()


if __name__ == '__main__':
    sql_import()
