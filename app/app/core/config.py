"""FrankieCMS Configuartion File"""
import os

APP_ENV = os.getenv('APP_ENV', 'development')

DATABASE_DRIVER = os.getenv('DB_DRIVER', 'postgresql')
DATABASE_USERNAME = os.getenv('DB_USER', 'postgres')
DATABASE_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DATABASE_HOST = os.getenv('DB_HOST', 'db')
DATABASE_NAME = os.getenv('DB_NAME', 'app')
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'app_test')
