-- =========================================
-- CRIAÇÃO DO BANCO
-- =========================================
CREATE DATABASE loja_db;
USE loja_db;

-- =========================================
-- TABELA: Perfis
-- =========================================
CREATE TABLE Perfis (
    ID_Perfil INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Perfil VARCHAR(50) NOT NULL
);

INSERT INTO Perfis (Nome_Perfil) VALUES 
('Desenvolvedor'),
('Caixa'),
('Repositor'),
('Gestor de Dados');

-- =========================================
-- TABELA: Funcionarios
-- =========================================
CREATE TABLE Funcionarios (
    ID_Funcionario INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Senha VARCHAR(100) NOT NULL,
    ID_Perfil INT,
    FOREIGN KEY (ID_Perfil) 
        REFERENCES Perfis(ID_Perfil)
        ON DELETE SET NULL
);

INSERT INTO Funcionarios (Nome, Login, Senha, ID_Perfil) VALUES
('Isaac Amaral', 'isaac.amaral', '123', 1),
('Romulo Silva', 'romulo.silva', '123', 1),
('Cauã Sérgio', 'caua.sergio', '123', 1);

-- =========================================
-- TABELA: Categorias (HIERÁRQUICA)
-- =========================================
CREATE TABLE Categorias (
    ID_Categoria INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(150) UNIQUE NOT NULL,
    Pai_ID INT DEFAULT NULL,
    FOREIGN KEY (Pai_ID) 
	REFERENCES Categorias(ID_Categoria)
	ON DELETE SET NULL
);

-- =========================================
-- TABELA: Produtos
-- =========================================

CREATE TABLE Produtos (
    ID_Produto INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL,
    Categoria_ID INT DEFAULT NULL,
    Img VARCHAR(255),
    FOREIGN KEY (Categoria_ID) 
        REFERENCES Categorias(ID_Categoria)
        ON DELETE SET NULL
);