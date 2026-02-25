from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Database connection
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

# User schema
class UserCreate(BaseModel):
    tenant_id: int
    email: str
    phone: str
    password: str

# Home endpoint
@app.get("/")
def home():
    return {"message": "API is working"}

# Create User endpoint
@app.post("/api/users")
def create_user(user: UserCreate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Check if email exists
        cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
        if cur.fetchone():
            raise HTTPException(status_code=409, detail="Email already exists")

        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Add 6 zeros at start
        final_password_hash = "000000" + hashed_password

        # Insert into DB
        cur.execute("""
            INSERT INTO users
            (tenant_id, email, phone, password_hash, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, tenant_id, email, phone, is_active
        """, (
            user.tenant_id,
            user.email,
            user.phone,
            final_password_hash,
            True,
            datetime.now(),
            datetime.now()
        ))

        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "User created successfully",
            "user": {
                "id": new_user[0],
                "tenant_id": new_user[1],
                "email": new_user[2],
                "phone": new_user[3],
                "is_active": new_user[4]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
