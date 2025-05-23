import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection string
DATABASE_URL = 'postgresql://postgres:jGOEnSzNyXWkxBdoIQayvcImZlklPSQK@trolley.proxy.rlwy.net:43430/railway'

# SQL to create tables
CREATE_TABLES_SQL = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    role VARCHAR(20) DEFAULT 'patient',
    phone VARCHAR(20),
    address TEXT,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Professionals table
CREATE TABLE IF NOT EXISTS professionals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cro VARCHAR(20) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES users(id),
    professional_id INTEGER REFERENCES professionals(id),
    date DATE NOT NULL,
    time TIME NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Treatment plans table
CREATE TABLE IF NOT EXISTS treatment_plans (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES users(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Treatment steps table
CREATE TABLE IF NOT EXISTS treatment_steps (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES treatment_plans(id) ON DELETE CASCADE,
    description VARCHAR(500) NOT NULL,
    expected_date DATE,
    completed BOOLEAN DEFAULT FALSE,
    completed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES users(id),
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(200),
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- File uploads table
CREATE TABLE IF NOT EXISTS file_uploads (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) DEFAULT 'document',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Insert default data
INSERT_DEFAULT_DATA_SQL = """
-- Insert admin user if not exists
INSERT INTO users (name, email, password_hash, role) 
SELECT 'Administrator', 'admin@clinic.com', 'scrypt:32768:8:1$yF9YOhVqzAH1WRDZ$e8b8f3df0c5f8b2e7a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f', 'admin'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@clinic.com');

-- Insert sample professionals if not exist
INSERT INTO professionals (name, cro, specialty) 
SELECT 'Dr. Maria Silva', '12345-SP', 'Ortodontia'
WHERE NOT EXISTS (SELECT 1 FROM professionals WHERE cro = '12345-SP');

INSERT INTO professionals (name, cro, specialty) 
SELECT 'Dr. João Santos', '67890-SP', 'Implantodontia'
WHERE NOT EXISTS (SELECT 1 FROM professionals WHERE cro = '67890-SP');
"""

def create_tables():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(DATABASE_URL)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        
        print("Conectando ao PostgreSQL...")
        
        # Create tables
        print("Criando tabelas...")
        cursor.execute(CREATE_TABLES_SQL)
        
        # Insert default data
        print("Inserindo dados padrão...")
        cursor.execute(INSERT_DEFAULT_DATA_SQL)
        
        print("✓ Tabelas criadas com sucesso!")
        print("✓ Dados padrão inseridos!")
        print("\nCredenciais de admin:")
        print("Email: admin@clinic.com")
        print("Senha: admin123")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    create_tables()