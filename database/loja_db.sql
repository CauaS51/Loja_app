-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS loja_db;
USE loja_db;

-- ========================
-- Tabela: Perfis
-- ========================
CREATE TABLE Perfis (
    ID_Perfil INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Perfil VARCHAR(50) NOT NULL
);

INSERT INTO Perfis (Nome_Perfil) VALUES 
('Desenvolvedor'),
('Caixa'),
('Repositor'),
('Gestor de Dados');

-- ========================
-- Tabela: Funcionarios
-- ========================
CREATE TABLE Funcionarios (
    ID_Funcionario INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Senha VARCHAR(100) NOT NULL,
    ID_Perfil INT,
    FOREIGN KEY (ID_Perfil) REFERENCES Perfis(ID_Perfil)
);

INSERT INTO Funcionarios (Nome, Login, Senha, ID_Perfil) VALUES
('Isaac Amaral', 'isaac.amaral', '123', 1),
('Romulo Silva', 'romulo.silva', '123', 1),
('Cauã Sérgio', 'caua.sergio', '123', 1);

-- ========================
-- Tabela: Produtos
-- ========================
CREATE TABLE Produtos (
    ID_Produto INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL,
    Categoria VARCHAR(255) NOT NULL,
    Img VARCHAR(255)
);

-- Inserir produtos de exemplo (corrigido: Categoria no lugar certo)
INSERT INTO Produtos (Nome, Preco, Categoria, Img) VALUES
('Salgadinho Doritos 28g', 4.50, 'Salgados', 'images/produtos/1.png'),
('Refrigerante Lata', 5.00, 'Bebidas', 'images/produtos/2.png'),
('Água Mineral 500ml', 2.00, 'Bebidas', 'images/produtos/3.png');
