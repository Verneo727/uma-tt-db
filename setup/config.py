#!/usr/bin/env python3

import configparser
from pathlib import Path

def create_config(app_path):
    try:
        file_path = Path(app_path)/"config.ini"
        if file_path.exists():
            return
        
        config = configparser.ConfigParser()
        config['APP'] = {
            'path': f'{app_path}',
            'database': '',
            'json': '',
            'lang': '',
        }

        try:
            with open(file_path, "w", encoding="utf-8") as configfile:
                config.write(configfile)
        except IOError as e:
            print(f"Erro while saving config file:\n{e}")
    except Exception as e:
        print(e)

def json_update(app_path, json_path):
    config_file = Path(app_path/"config.ini")
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    config['APP']['json'] = str(json_path)
    with open(config_file, "w", encoding="utf-8") as f:
        config.write(f)

def load_json(app_path):
    config_file = Path(app_path/"config.ini")
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding="utf-8")
        if config.has_option('APP', 'json'):
            json_path = config.get('APP', 'json')
            return json_path
    except Exception as e:
        print(e)

def lang_set(app_path):
    config_file = Path(app_path/"config.ini")
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding="utf-8")
        if config.has_option('APP', 'lang'):
            value = config.get('APP', 'lang')
            return bool(value)
        return False
    except Exception as e:
        print(e)
        return False

def lang_update(app_path, lang):
    config_file = Path(app_path)/"config.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    if 'APP' not in config:
        config['APP'] = {}

    config['APP']['lang'] = str(lang)
    with open(config_file, "w", encoding="utf-8") as f:
        config.write(f)

def lang_load(app_path):
    """Return the language code ('en') from the config file."""
    config_file = Path(app_path)/"config.ini"
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding="utf-8")
        if config.has_option('APP', 'lang'):
            lang = config.get('APP', 'lang')
            return lang
        return False
    except Exception as e:
        print(e)
        return False

def load_db_path(app_path):
    """Return the path to the uma.db database from the config file."""
    config_file = Path(app_path)/"config.ini"
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding="utf-8")
        if config.has_option('APP', 'database'):
            db_path = config.get('APP', 'database')
            return db_path
        return False
    except Exception as e:
        print(e)
        return False