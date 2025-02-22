import os
import yaml
from dotenv import load_dotenv

class Config:
    def __init__(self, yaml_path="config.yaml", env_path=".env"):
        self.yaml_path = yaml_path
        self.env_path = env_path
        self.config = self.load_config()

    def load_config(self):
        config = {}

        if os.path.exists(self.yaml_path):
            with open(self.yaml_path, "r", encoding="utf-8") as file:
                try:
                    yaml_dict = yaml.safe_load(file)
                except Exception:
                    raise Exception('YAML 파일 문법이 옳지 않습니다.')
            config.update(yaml_dict)

        if os.path.exists(self.env_path):
            load_dotenv(self.env_path)

        for key, value in os.environ.items():
            config[key] = value

        return config

    def get(self, key, default=None):
        """중첩된 키 (예: "database.host")를 가져오기"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value or default
    
    def __call__(self, key, default=None):
        return self.get(key, default)
    
    def __contains__(self, key):
        return bool(self.get(key))

# 인스턴스 생성.
config = Config()


if __name__ == '__main__':
    # ✅ 사용 예제
    print(config("cors.allow_origins"))
    print(config("database.host"))
    print(config("database.password"))
