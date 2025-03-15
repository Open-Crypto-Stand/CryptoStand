from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Строка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем базу данных и сессию
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Инициализируем хеширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модели данных для SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI()

# Модель данных для регистрации и авторизации
class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

# Хэшируем пароль с использованием passlib
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверяем правильность пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Получаем сессию для работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для регистрации
@app.post("/register")
async def register(user: UserIn, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Хешируем пароль
    hashed_password = hash_password(user.password)

    # Создаем нового пользователя
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error during user registration")
    return {"message": "User registered successfully"}

# Эндпоинт для авторизации
@app.post("/login")
async def login(user: UserIn, db: Session = Depends(get_db)):
    # Ищем пользователя в базе
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}