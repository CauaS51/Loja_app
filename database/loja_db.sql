-- =========================================
-- RECRIAR BANCO
-- =========================================
DROP DATABASE IF EXISTS loja_db;
CREATE DATABASE loja_db;
USE loja_db;

-- =========================================
-- LOJAS
-- =========================================
CREATE TABLE Lojas (
    ID_Loja INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Loja VARCHAR(150) NOT NULL,
    Img VARCHAR(255)
);

-- =========================================
-- TEMAS DAS LOJAS
-- =========================================
CREATE TABLE Temas_Lojas (
    ID_Loja INT PRIMARY KEY,
    Tema_JSON JSON NOT NULL,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE
);

-- =========================================
-- PERFIS
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
-- CONTAS
-- =========================================
CREATE TABLE Contas (
    ID_Conta INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    Email VARCHAR(150) NOT NULL,
    Telefone VARCHAR(20),
    CPF VARCHAR(14) UNIQUE NOT NULL,
    Data_Cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- FUNCIONÁRIOS NA LOJA
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
-- CATEGORIAS
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
-- PRODUTOS (MODELO PROFISSIONAL)
-- =========================================
CREATE TABLE Produtos (
    ID_Produto INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    Nome VARCHAR(255) NOT NULL,
    Codigo_Barras VARCHAR(50) UNIQUE,
    Preco DECIMAL(10,2) NOT NULL,
    Custo DECIMAL(10,2),
    Margem_Lucro DECIMAL(5,2),
    Estoque INT DEFAULT 0,
    Estoque_Minimo INT DEFAULT 0,
    Unidade VARCHAR(10) DEFAULT 'UN',
    Categoria_ID INT DEFAULT NULL,
    Img VARCHAR(255),
    Ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (Categoria_ID) REFERENCES Categorias(ID_Categoria) ON DELETE SET NULL
);

-- =========================================
-- MOVIMENTAÇÃO DE ESTOQUE
-- =========================================
CREATE TABLE Movimentacoes_Estoque (
    ID_Mov INT AUTO_INCREMENT PRIMARY KEY,
    ID_Produto INT NOT NULL,
    ID_Loja INT NOT NULL,
    Tipo ENUM('ENTRADA','SAIDA','AJUSTE') NOT NULL,
    Quantidade INT NOT NULL,
    Motivo VARCHAR(100),
    Data_Mov DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Produto) REFERENCES Produtos(ID_Produto) ON DELETE CASCADE,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE
);

-- =========================================
-- VENDAS
-- =========================================
CREATE TABLE Vendas (
    ID_Venda INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    ID_Funcionario INT,
    Data_Venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    Total DECIMAL(10,2),
    Forma_Pagamento VARCHAR(50),
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (ID_Funcionario) REFERENCES Funcionarios_Loja(ID_Funcionario) ON DELETE SET NULL
);

-- =========================================
-- ITENS DA VENDA
-- =========================================
CREATE TABLE Itens_Venda (
    ID_Item INT AUTO_INCREMENT PRIMARY KEY,
    ID_Venda INT NOT NULL,
    ID_Produto INT NOT NULL,
    Quantidade INT NOT NULL,
    Preco_Unitario DECIMAL(10,2),
    Subtotal DECIMAL(10,2),
    FOREIGN KEY (ID_Venda) REFERENCES Vendas(ID_Venda) ON DELETE CASCADE,
    FOREIGN KEY (ID_Produto) REFERENCES Produtos(ID_Produto) ON DELETE CASCADE
);

-- =========================================
-- CONTROLE DE CAIXA
-- =========================================
CREATE TABLE Caixas (
    ID_Caixa INT AUTO_INCREMENT PRIMARY KEY,
    ID_Loja INT NOT NULL,
    ID_Funcionario INT,
    Data_Abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    Data_Fechamento DATETIME NULL,
    Valor_Inicial DECIMAL(10,2),
    Valor_Final DECIMAL(10,2),
    Status ENUM('ABERTO','FECHADO') DEFAULT 'ABERTO',
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE,
    FOREIGN KEY (ID_Funcionario) REFERENCES Funcionarios_Loja(ID_Funcionario) ON DELETE SET NULL
);

-- =========================================
-- MOVIMENTAÇÕES DE CAIXA
-- =========================================
CREATE TABLE Movimentacoes_Caixa (
    ID_Mov INT AUTO_INCREMENT PRIMARY KEY,
    ID_Caixa INT NOT NULL,
    Tipo ENUM('SANGRIA','SUPRIMENTO') NOT NULL,
    Valor DECIMAL(10,2),
    Motivo VARCHAR(100),
    Data_Mov DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Caixa) REFERENCES Caixas(ID_Caixa) ON DELETE CASCADE
);

-- =========================================
-- FORNECEDORES
-- =========================================
CREATE TABLE Fornecedores (
    ID_Fornecedor INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(150),
    CNPJ VARCHAR(20),
    Telefone VARCHAR(20),
    Email VARCHAR(150)
);

-- =========================================
-- COMPRAS
-- =========================================
CREATE TABLE Compras (
    ID_Compra INT AUTO_INCREMENT PRIMARY KEY,
    ID_Fornecedor INT,
    ID_Loja INT,
    Data_Compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    Total DECIMAL(10,2),
    FOREIGN KEY (ID_Fornecedor) REFERENCES Fornecedores(ID_Fornecedor) ON DELETE SET NULL,
    FOREIGN KEY (ID_Loja) REFERENCES Lojas(ID_Loja) ON DELETE CASCADE
);

-- =========================================
-- ITENS DA COMPRA
-- =========================================
CREATE TABLE Itens_Compra (
    ID_Item INT AUTO_INCREMENT PRIMARY KEY,
    ID_Compra INT,
    ID_Produto INT,
    Quantidade INT,
    Custo_Unitario DECIMAL(10,2),
    Subtotal DECIMAL(10,2),
    FOREIGN KEY (ID_Compra) REFERENCES Compras(ID_Compra) ON DELETE CASCADE,
    FOREIGN KEY (ID_Produto) REFERENCES Produtos(ID_Produto) ON DELETE CASCADE
);

-- =========================================
-- RELATÓRIOS GERADOS
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
