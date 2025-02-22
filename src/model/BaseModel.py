from sqlalchemy import Column, DateTime, BigInteger
from sqlalchemy.orm import declared_attr, declarative_base
from sqlalchemy.sql import func


# 기본적인 Base 클래스 생성
class BaseModel():
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()  # 테이블 이름을 모델 이름 소문자로 설정
    
    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.timezone("Asia/Seoul", func.now()), nullable=False)
    
    
    @classmethod
    def add_sort(cls, query, column_name, is_asc):
        if column_name == 'created_at':
            new_order = cls.created_at.asc() if is_asc else cls.created_at.desc()
            return cls.add_order_by(query, new_order)
        elif column_name == 'id':
            new_order = cls.id.asc() if is_asc else cls.id.desc()
            return cls.add_order_by(query, new_order)
        else:
            return query


# Base 클래스 재정의
BaseModel = declarative_base(cls=BaseModel)
