-- Tabela Usuario com Data_create
CREATE TABLE Usuario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    CPF VARCHAR(11) UNIQUE NOT NULL,
    Celular VARCHAR(15),
    Email VARCHAR(255) UNIQUE,
    Senha VARCHAR(255) NOT NULL,
    CEP VARCHAR(8),
    Logradouro VARCHAR(255),
    Numero INT,
    Complemento VARCHAR(255),
    Cidade VARCHAR(100),
    Bairro VARCHAR(100),
    Estado VARCHAR(50),
    Data_nascimento DATE,
    Data_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Armazena a data de criação automaticamente
);
