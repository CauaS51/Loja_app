-- =========================================
-- RECRIAR BANCO
-- =========================================
DROP DATABASE IF EXISTS loja_db;
CREATE DATABASE loja_db;
USE loja_db;

-- =========================================
-- TABELA: LOJAS
-- =========================================
CREATE TABLE Lojas (
    ID_Loja INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Loja VARCHAR(150) NOT NULL,
    Img VARCHAR(255)
);

-- =========================================
-- TABELA: TEMAS DAS LOJAS
-- =========================================
CREATE TABLE Temas_Lojas (
    ID_Loja INT PRIMARY KEY,
    Tema_JSON JSON NOT NULL,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE
);

-- =========================================
-- TABELA: PERFIS
-- =========================================
CREATE TABLE Perfis (
    ID_Perfil INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Perfil VARCHAR(50) NOT NULL
);

INSERT INTO Perfis (Nome_Perfil) VALUES
('Administrador'),
('Caixa'),
('Repositor'),
('Gestor de Dados');

-- =========================================
-- TABELA: CONTAS (LOGIN DO SISTEMA)
-- =========================================
CREATE TABLE Contas (
    ID_Conta INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL, -- espaço para hash
    Email VARCHAR(150) NOT NULL,
    Telefone VARCHAR(20),
    CPF VARCHAR(14) UNIQUE NOT NULL,
    Data_Cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- FUNCIONÁRIOS VINCULADOS À LOJA
-- =========================================
CREATE TABLE Funcionarios_Loja (
    ID_Funcionario INT AUTO_INCREMENT PRIMARY KEY,
    ID_Conta INT NOT NULL,
    ID_Loja INT NOT NULL,
    ID_Perfil INT NOT NULL,
    UNIQUE (ID_Conta, ID_Loja),
    FOREIGN KEY (ID_Conta) REFERENCES Contas(ID_Conta) ON DELETE CASCADE,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (ID_Perfil) REFERENCES Perfis(ID_Perfil)
);

-- =========================================
-- CATEGORIAS DE PRODUTOS
-- =========================================
CREATE TABLE Categorias (
    ID_Categoria INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    Nome VARCHAR(150) NOT NULL,
    Pai_ID INT DEFAULT NULL,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (Pai_ID) REFERENCES Categorias(ID_Categoria) ON DELETE SET NULL
);

-- =========================================
-- PRODUTOS
-- =========================================
CREATE TABLE Produtos (
    ID_Produto INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    Nome VARCHAR(255) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL,
    Categoria_ID INT DEFAULT NULL,
    Img VARCHAR(255),
    Ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (Categoria_ID) REFERENCES Categorias(ID_Categoria) ON DELETE SET NULL
);

-- =========================================
-- RELATÓRIOS
-- =========================================
CREATE TABLE Relatorios (
    ID_Relatorio INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    ID_Conta INT,
    Data_inicio DATETIME,
    Data_fim DATETIME,
    Tipo VARCHAR(50),
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (ID_Conta) REFERENCES Contas(ID_Conta) ON DELETE SET NULL
);
