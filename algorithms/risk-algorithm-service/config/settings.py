import os


class Settings:
    BACKEND_URL: str = os.environ.get('BACKEND_URL', 'http://localhost:8080')
    ALGORITHM_PORT: int = int(os.environ.get('ALGORITHM_PORT', 5000))
    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'

    CALLBACK_TIMEOUT: int = 5
    TASK_THREAD_DAEMON: bool = True


settings = Settings()