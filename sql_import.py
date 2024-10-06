#!/usr/bin/env python3

import os
import json
import sqlite3
from utils.logger import logger


JSON_DATA_PATH = 'data/feeds/json'


def sql_import():
    conn = sqlite3.connect('today.db')
    c = conn.cursor()

    table_create_sql = '''
    CREATE TABLE IF NOT EXISTS feed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        source json, 
        archive_date date);
    '''
    table_index_create_sql = '''
    CREATE UNIQUE INDEX IF NOT EXISTS idx_feed_unique ON feed (
        title,
        url,
        json_extract(source, '$.name')
    );
    '''
    c.execute(table_create_sql)
    c.execute(table_index_create_sql)

    sql = 'INSERT INTO feed (title, url, source, archive_date) VALUES (?, ?, ?, ?)'

    for file in sorted(os.listdir(JSON_DATA_PATH)):
        filepath = f'{JSON_DATA_PATH}/{file}'
        date_str = file.rstrip('.json')
        with open(filepath) as f:
            logger.info(f'process file: {filepath}')
            data = json.load(f)
            for feed in data:
                print(feed)
                try:
                    c.execute(sql, (feed['title'], feed['url'], json.dumps(feed['source'], ensure_ascii=False), date_str))
                except sqlite3.IntegrityError as e:
                    pass

            conn.commit()


if __name__ == '__main__':
    sql_import()
