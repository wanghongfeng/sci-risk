import os
from pathlib import Path

ENV = os.environ.get('ENVIRONMENT', 'local')
ENV_FILE = Path(__file__).parent.parent / f'.env.{ENV}'

def load_env_file():
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env_file()


class Settings:
    BACKEND_URL: str = os.environ.get('BACKEND_URL', 'http://localhost:8080')
    ALGORITHM_PORT: int = int(os.environ.get('ALGORITHM_PORT', 5000))
    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT: str = os.environ.get('ENVIRONMENT', 'local')
    ALGORITHM_BASE_URL: str = os.environ.get('ALGORITHM_BASE_URL', f'http://localhost:{ALGORITHM_PORT}')

    CALLBACK_TIMEOUT: int = 5
    TASK_THREAD_DAEMON: bool = True


settings = Settings()