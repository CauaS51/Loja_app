-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS loja_db_test;
USE loja_db_test;

-- ========================
-- Tabela: Perfil
-- ========================
CREATE TABLE Perfis (
    ID_Perfil INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Perfil VARCHAR(50) NOT NULL
);

INSERT INTO Perfis (Nome_Perfil) VALUES 
('Desenvolvedor'),
('Caixa'),
('Repositor'),
('Gestor de Dados')
;

-- ========================
-- Tabela: Funcionario
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

