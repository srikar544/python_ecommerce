"""
config.py
---------
Centralized configuration for the Flask application.

Why this file exists:
- Avoid hardcoding sensitive values
- Support multiple environments
- Make app production-ready

"""

import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    """
    Base configuration class.
    Shared settings across all environments.
    """

    # Secret key used for sessions, cookies, CSRF protection
    SECRET_KEY = os.getenv("SECRET_KEY")

    # SQLAlchemy database connection string
    SQLALCHEMY_DATABASE_URI =(
         f"mysql+pymysql://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/"
        f"{os.getenv('DB_NAME')}"
    )

    # Disable modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default cache timeout (seconds)
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 60))

class DevelopmentConfig(BaseConfig):

      """
    Development environment config.
    Used locally.
      """    
 
      DEBUG=False

class ProductionConfig(BaseConfig):
      """
      Production environment config.
      Used on live servers.
    """      

    # Map environment name to config class
config_map = {
         "development":DevelopmentConfig,
         "production":ProductionConfig,
    }  

