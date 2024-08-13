-- Criação da Tabela Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    celular VARCHAR(17),
    email VARCHAR(100) NOT NULL,
    cpf VARCHAR(20) UNIQUE NOT NULL
);




















-- Criação da Tabela Categoria
CREATE TABLE Categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Criação da Tabela Tipo
CREATE TABLE Tipo (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    id_categoria INT,
    nome VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);

-- Criação da Tabela Documentos
CREATE TABLE Documentos (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_categoria INT,
    id_tipo INT,
    valor DECIMAL(10, 2),
    data DATE,
    imagem VARCHAR(255),
    codigo_NFE VARCHAR(50),
    informacao TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
    FOREIGN KEY (id_tipo) REFERENCES Tipo(id_tipo)
);