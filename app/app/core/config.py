"""FrankieCMS Configuartion File"""
import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'db')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'app')
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'app_test')
