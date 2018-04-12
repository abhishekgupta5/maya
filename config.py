# config.py

class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    CSRF_ENABLED = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_ECHO = True
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """
    Testing configurations
    """
    DEBUG = True
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
    }

