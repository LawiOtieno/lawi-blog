import os
from dotenv import load_dotenv
load_dotenv()

class Config:
  SQLALCHEMY_TRACK_MODIFICATIONS=True
  SECRET_KEY = os.environ.get('SECRET_KEY')

  #Simplemde cofigurations
  SIMPLEMDE_JS_IIFE = True
  SIMPLEMDE_USE_CDN = True

  #Email configurations
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
  MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
  
  #PHOTOS UPLOAD CONFIGURATION
  UPLOADED_PHOTOS_DEST = 'app/static/photos'

class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
  if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",1)

class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://access:lawioti@localhost/blogging'
  DEBUG = True

class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:nick101010@localhost/blog_test'

config_options = {
  'production':ProdConfig,
  'development':DevConfig,
  'test':TestConfig
}
