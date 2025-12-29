import mysql.connector
from mysql.connector import Error

#--FUNÇÃO DE CONEXÃO COM O BANCO DE DADOS
def conexao():
    try:
        con = mysql.connector.connect(host='localhost', database='suporte', user='root', password='Htg.11202718')
        if con.is_connected():
            return con
    except Error as e:
        print("Erro ao conectar ao bando de dados;", e)

#--FUNÇÃO DE BUSCA NO BANCO DE DADOS
def funcao_select(consulta_sql,param):
    try:
        con = conexao()
        cursor = con.cursor()
        cursor.execute(consulta_sql, param)
        linhas = cursor.fetchall()
        print("numero de registros retornados", cursor.rowcount)

        print("\nMostrando os dados cadastrados")

        for linha in linhas:
            print("id: ", linha[0])
            print("nome:", linha[1])

        return linhas
    except Error as e:
        print("Erro ao acessar tabela", e)
        return []
    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()
            
            print("Conexão com o banco de dados encerrada")

#--FUNÇÃO DE INSERT BANCO DE DADOS
def funcao_insert(consulta_Sql,param):
    try:
        con = conexao()
        cursor = con.cursor()
        cursor.execute(consulta_Sql,param)
        con.commit()
    except Error as e:
        print("Erro ao acessar tabela", e)
    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()

#--FUNÇÃO LISTAR TICKETS
def funcao_listar(consulta_Sql):
    try:
        con = conexao()
        cursor = con.cursor()
        cursor.execute(consulta_Sql)
        linha = cursor.fetchall()
        return linha   
    except Error as e:
        print("Erro ao acessar tabela", e)
        return[]
    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()

            print("Conexão com o banco de dados encerrada.")

def funcao_update(consulta_sql,param):
    try:
        con = conexao()
        cursor = con.cursor()
        cursor.execute(consulta_sql,param)
        con.commit()
    except Error as e:
        print("Erro ao acessar tabela", e)
        return[]
    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()

            print("Conexão com o banco de dados encerrada.")
