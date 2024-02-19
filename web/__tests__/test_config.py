from ..config import data_dir, db_dir, cache_dir
import os


def test_data_dir():
    assert data_dir('') == '/data/docs'
    assert data_dir('my-collection') == '/data/docs-my-collection'


def test_data_dir_env():
    os.environ['DATA_DIR'] = '/custom-data'
    os.environ['DATA_DIR_MY-COLLECTION'] = '/custom-data-collection'
    assert data_dir('') == '/custom-data'
    assert data_dir('my-collection') == '/custom-data-collection'
    os.environ.pop('DATA_DIR')
    os.environ.pop('DATA_DIR_MY-COLLECTION')


def test_db_dir():
    assert db_dir('') == '/data/db'
    assert db_dir('my-collection') == '/data/db-my-collection'


def test_db_dir_env():
    os.environ['DB_DIR'] = '/custom-db'
    os.environ['DB_DIR_MY-COLLECTION'] = '/custom-db-collection'
    assert db_dir('') == '/custom-db'
    assert db_dir('my-collection') == '/custom-db-collection'
    os.environ.pop('DB_DIR')
    os.environ.pop('DB_DIR_MY-COLLECTION')


def test_cache_dir():
    assert cache_dir() == '/data/cache'


def test_cache_dir_env():
    os.environ['CACHE_DIR'] = '/custom-cache'
    assert cache_dir() == '/custom-cache'
    os.environ.pop('CACHE_DIR')
