-- =========================================
-- RECRIAR BANCO
-- =========================================
DROP DATABASE IF EXISTS loja_db;
CREATE DATABASE loja_db;
USE loja_db;

-- =========================================
-- TABELA: LOJAS
-- =========================================
DROP TABLE IF EXISTS Lojas;
CREATE TABLE Lojas (
    ID_Loja INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Loja VARCHAR(150) NOT NULL,
    Img VARCHAR(255) NULL
);

-- =========================================
-- TABELA: PERFIS
-- =========================================
DROP TABLE IF EXISTS Perfis;
CREATE TABLE Perfis (
    ID_Perfil INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Perfil VARCHAR(50) NOT NULL
);

-- Inserir Perfis
INSERT INTO Perfis (Nome_Perfil) VALUES
('Administrador'),
('Caixa'),
('Repositor'),
('Gestor de Dados');

-- =========================================
-- TABELA: CONTAS
-- =========================================
DROP TABLE IF EXISTS Contas;
CREATE TABLE Contas (
    ID_Conta INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Senha VARCHAR(100) NOT NULL
);

-- Inserir Contas
INSERT INTO Contas (Nome, Login, Senha) VALUES
('Isaac Amaral', 'isaac.amaral', '123'),
('Romulo Silva', 'romulo.silva', '123'), 
('Cauã Sérgio', 'caua.sergio', '123'); 

-- =========================================
-- TABELA: FUNCIONARIOS_LOJA
-- =========================================
DROP TABLE IF EXISTS Funcionarios_Loja;
CREATE TABLE Funcionarios_Loja (
    ID_Funcionario INT AUTO_INCREMENT PRIMARY KEY,
    ID_Conta INT NOT NULL,
    ID_Loja INT NOT NULL,
    ID_Perfil INT NOT NULL,
    UNIQUE (ID_Conta, ID_Loja), -- evita duplicar funcionário na mesma loja
    FOREIGN KEY (ID_Conta) REFERENCES Contas(ID_Conta),
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja),
    FOREIGN KEY (ID_Perfil) REFERENCES Perfis(ID_Perfil)
);




-- =========================================
-- TABELA: CATEGORIAS
-- =========================================
DROP TABLE IF EXISTS Categorias;
CREATE TABLE Categorias (
    ID_Categoria INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    Nome VARCHAR(150) NOT NULL,
    Pai_ID INT DEFAULT NULL,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja),
    FOREIGN KEY (Pai_ID) REFERENCES Categorias(ID_Categoria)
);

-- =========================================
-- TABELA: PRODUTOS
-- =========================================
DROP TABLE IF EXISTS Produtos;
CREATE TABLE Produtos (
    ID_Produto INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    Nome VARCHAR(255) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL,
    Categoria_ID INT DEFAULT NULL,
    Img VARCHAR(255),
    Ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja),
    FOREIGN KEY (Categoria_ID) REFERENCES Categorias(ID_Categoria)
);

-- =========================================
-- TABELA: RELATORIOS
-- =========================================
DROP TABLE IF EXISTS Relatorios;
CREATE TABLE Relatorios (
    ID_Relatorio INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    ID_Funcionario INT,
    Data_inicio DATETIME,
    Data_fim DATETIME,
    Tipo VARCHAR(50),
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja),
    FOREIGN KEY (ID_Funcionario) REFERENCES Contas(ID_Conta)
);
