#!/usr/bin/env python3

import os
import json
import sqlite3
from utils.logger import logger
from utils.time import get_beijing_time

JSON_DATA_PATH = 'data/feeds/json'

conn = sqlite3.connect('today.db')

def history_data_import():
    c = conn.cursor()

    table_create_sql = '''
    CREATE TABLE IF NOT EXISTS feed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        source_name TEXT NOT NULL, 
        source_desc TEXT NOT NULL,
        source_icon TEXT NOT NULL,
        archive_date DATE
        );
    '''
    table_index_create_sql = '''
    CREATE UNIQUE INDEX IF NOT EXISTS idx_feed_unique ON feed (
        title,
        url,
        source_name,
        archive_date
    );
    '''
    c.execute(table_create_sql)
    c.execute(table_index_create_sql)

    for file in sorted(os.listdir(JSON_DATA_PATH)):
        filepath = f'{JSON_DATA_PATH}/{file}'
        date_str = file.rstrip('.json')
        with open(filepath) as f:
            logger.info(f'process file: {filepath}')
            data = json.load(f)
            insert_feeds(data, date_str)

def insert_feeds(data, date_str=get_beijing_time().date()):
    c = conn.cursor()
    insert_sql = 'INSERT INTO feed (title, url, source_name, source_desc, source_icon, archive_date) VALUES (?, ?, ?, ?, ?, ?)'

    for feed in data:
        print(feed)
        try:
            c.execute(insert_sql, (
            feed['title'], feed['url'], feed['source']['name'], feed['source']['desc'], feed['source']['icon'],
            date_str))
        except sqlite3.IntegrityError as e:
            pass
    conn.commit()

def _row_to_feed(row):
    return {
        'title': row[1],
        'url': row[2],
        'source': {
            'name': row[3],
            'desc': row[4],
            'icon': row[5]
        }
    }

def get_today_feed():
    c = conn.cursor()
    today = get_beijing_time().date()
    select_sql = f'SELECT * FROM feed WHERE archive_date = "{today}" ORDER BY id DESC'
    data = c.execute(select_sql).fetchall()
    feeds = [_row_to_feed(row) for row in data]
    return feeds

def get_today_feed_by_source(source_name):
    c = conn.cursor()
    today = get_beijing_time().date()
    select_sql = f'SELECT * FROM feed WHERE source_name = "{source_name}" AND archive_date = "{today}" ORDER BY id DESC'
    data = c.execute(select_sql).fetchall()
    feeds = [_row_to_feed(row) for row in data]
    return feeds


if __name__ == '__main__':
    history_data_import()