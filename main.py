from datetime import datetime
from banco import funcao_select
from banco import funcao_insert
from banco import funcao_listar
from banco import funcao_update
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from atualiza import atualiza_menu_clientes, atualiza_menu_tecnicos
from centraliza import centraliza_janela

id_ticket_selecionado = ""
status = ["ABERTO", "FECHADO", "TICKET BLIP", "AGUARDANDO CLIENTE"]

if __name__ == "__main__":
    def mascara_data(event):
        entry = event.widget

        texto = entry.get().replace("/","") #remove barras se forem colocadas
        novo = ""

        if not texto.isdigit():
            entry.delete(0, "end")
            entry.insert(0, "")
            return

        #dia
        if len(texto) >=2:
            novo += texto[:2] + "/"
        else:
            novo += texto
            entry.delete(0, "end")
            entry.insert(0, novo)
            return 
            
        #mês
        if len(texto) >= 4:
            novo += texto[2:4] + "/"
        else:
            novo +=texto[2:]
            entry.delete(0, "end")
            entry.insert(0, novo)
            return
            
        #ano
        if len(texto) > 4:
            novo += texto[4:8]

        entry.delete(0, "end")
        entry.insert(0, novo)

    def mascara_hora(event):
        entry =event.widget
        nova_hora = ""

        hora = entry.get().replace(":","")

        if not hora.isdigit():
            entry.delete(0,"end")
            return

        
        if len(hora) >= 2:
            nova_hora += hora[:2] + ":"
            
            #MINUTOS
            if len(hora) > 2:
                nova_hora += hora[2:]
        else:
            nova_hora += hora
        
        entry.delete(0, "end")
        entry.insert(0, nova_hora)

    def pesquisa():
        def executar_pesquisa():
            nome = campo_nome_pesquisa.get()

            sql = f"SELECT * FROM clientes WHERE nome_cliente LIKE %s"
            param = (f"%{nome}%", )
            resultados = funcao_select(sql, param)

            if not resultados:
                label = ctk.CTkLabel(janela_pesquisa, text="Nenhum resultado encontrado.")
                label.pack(pady=20)
                return
        
            clientes = []
            for linha in resultados:

                id_cliente = linha[0]
                nome_cliente = linha[1]

                clientes.append(f"{id_cliente} - {nome_cliente}")

            lista = ctk.CTkComboBox(janela_pesquisa, values=clientes, width=400)
            lista.grid(row=5, column=1, padx=10, pady=10, stick="ew")

        janela_pesquisa =  ctk.CTkToplevel(app)
        janela_pesquisa.attributes('-topmost', True)
        janela_pesquisa.title("Pesquisa por nome")
        centraliza_janela(janela_pesquisa)

        label_nome_pesquisa = ctk.CTkLabel(janela_pesquisa, text="Nome do cliente: ")
        label_nome_pesquisa.grid(row=1, column=0, padx=10, pady=10,sticky="e")

        campo_nome_pesquisa = ctk.CTkEntry(janela_pesquisa, width=600)
        campo_nome_pesquisa.grid(row=1,column=1, padx=10, pady=10,stick="w")
  
        botao_pesquisar = ctk.CTkButton(janela_pesquisa, text="PESQUISAR", command=executar_pesquisa, width = 500, height=50, fg_color="white", text_color="black")
        botao_pesquisar.grid(row=3, column=1, padx=10, pady=10, stick="ew")

    def pesquisa_atendente():
        sql = f"SELECT * FROM tecnicos WHERE status = 1"
        resultados = funcao_listar(sql)

        janela_pesquisa_atendente = ctk.CTkToplevel(app)
        janela_pesquisa_atendente.attributes("-topmost", True)
        janela_pesquisa_atendente.title("Tickets Cadastrados")
        centraliza_janela(janela_pesquisa_atendente)

        if not resultados:
            label = ctk.CTkLabel(janela_pesquisa_atendente, text="Nenhum resultado encontrado!")
            label.grid(row=4, column=0, columnspan=3, pady=20)
            return

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="#ffffff",
                        fieldbackground="#2b2b2b",
                        rowheight=25)
        style.map("Treeview", background=[('selected', "#1f538d")])

        colunas = ("ID", "Técnico")
        tabela = ttk.Treeview(janela_pesquisa_atendente, columns=colunas, show="headings")

        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=120, anchor="center")

        tabela.column("Técnico", width=250, anchor="w")

        scrollbar = ctk.CTkScrollbar(janela_pesquisa_atendente, orientation="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        tabela.pack(side="left", fill="both", expand=True, padx=(20,0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0,20), pady=20)

        for linha in resultados:
            tabela.insert("", "end", values=(linha[0], linha[1]))

    def cadastro_atendente():
        def realiza_cadastro():
            nome_digitado = campo_nome_atendente.get()
            nome_atendente = nome_digitado.upper()

            sql = f"INSERT INTO tecnicos (nome) VALUES (%s)"
            param = (nome_atendente,)
            funcao_insert(sql,param)

            campo_nome_atendente.delete(0,"end")
            messagebox.showinfo("Tecnico cadastrado com sucesso!")

            tecnicos_novos = atualiza_menu_tecnicos()
            campo_tecnico.configure(values=tecnicos_novos)
       
        janela_cadastro_atendente = ctk.CTkToplevel(app)
        janela_cadastro_atendente.attributes("-topmost", True)
        janela_cadastro_atendente.title("CADASTRO DE ATENDENTE")
        centraliza_janela(janela_cadastro_atendente)

        label_nome_atendente = ctk.CTkLabel(janela_cadastro_atendente, text="Nome do Tecnico")
        label_nome_atendente.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        campo_nome_atendente = ctk.CTkEntry(janela_cadastro_atendente, width=400)
        campo_nome_atendente.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        botao_cadastrar_atendente = ctk.CTkButton(janela_cadastro_atendente, text="CADASTRAR", command=realiza_cadastro, width=150, height=22)
        botao_cadastrar_atendente.grid(row=2, column=1, padx=10, pady=20, sticky="e")

        botao_pesquisar_atendente = ctk.CTkButton(janela_cadastro_atendente, text="PESQUISAR", command=pesquisa_atendente, width=150, height=22)
        botao_pesquisar_atendente.grid(row=2, column=1, padx=10, pady=20, sticky="w")
        
        tecnicos_novos = atualiza_menu_tecnicos()
        campo_tecnico.configure(values=tecnicos_novos)

    def cadastro_ticket(): 
        nome_cliente_selecionado = campo_cliente.get()
        id_cliente = nome_cliente_selecionado.split(" - ")[0]

        data_abertura = campo_data_abertura.get()
        data_abertura_tratada = datetime.strptime(data_abertura,"%d/%m/%Y").strftime("%Y-%m-%d")
      
        hora_abertura = campo_hora_abertura.get()
        descricao = campo_descricao.get()
        hora_primeiro_retorno = campo_hora_primeiro_retorno.get()
        data_retorno_final = campo_data_retorno_final.get()
        data_retorno_final_tratada = datetime.strptime(data_retorno_final,"%d/%m/%Y").strftime("%Y-%m-%d")
        hora_retorno_final =campo_hora_retorno_final.get()
        tecnico = campo_tecnico.get()
        status = campo_status.get()

        if data_retorno_final < data_abertura:
            messagebox.showinfo("Data de retorno final inválida!!!")
        elif hora_abertura > hora_primeiro_retorno:
            messagebox.showinfo("Hora de Primeiro retorno inválida!!!")
        elif nome_cliente_selecionado == "Selecione":
            messagebox.showinfo("Selecione o nome do cliente!!!")
        else:
            sql = f"INSERT INTO tickets (id_cliente,data_abertura,hora_abertura,descricao,hora_primeiro_retorno,data_retorno_final,hora_retorno_final,tecnico,status_ticket) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
            param = (
                id_cliente,
                data_abertura_tratada,
                hora_abertura,
                descricao,
                hora_primeiro_retorno,
                data_retorno_final_tratada,
                hora_retorno_final,
                tecnico,
                status
            )
                
            funcao_insert(sql,param)
            
            messagebox.showinfo("Ticket cadastrado com sucesso!")

            # -- LIMPA OS CAMPOS DO FORMULÁRIO
            campo_cliente.set("selecione")
            campo_data_abertura.delete(0,"end")
            campo_hora_abertura.delete(0,"end")
            campo_descricao.delete(0,"end")
            campo_hora_primeiro_retorno.delete(0,"end")
            campo_data_retorno_final.delete(0,"end")
            campo_hora_retorno_final.delete(0,"end")
            campo_tecnico.delete(0,"end")
            campo_status.delete(0,"end")

    def cadastro_cliente():
        def realiza_cadastro():
            nome_digitado = campo_nome_cliente.get()
            nome = nome_digitado.upper()

            sql = f"INSERT INTO clientes (nome_cliente) VALUES (%s)"
            param = (nome,)
            funcao_insert(sql,param)

            campo_nome_cliente.delete(0,"end")
           
            messagebox.showinfo("Cliente cadastrado com sucesso!")
        
            clientes_novos = atualiza_menu_clientes()
            campo_cliente.configure(values=clientes_novos)

        janela_cadastro_clientes = ctk.CTkToplevel(app)
        janela_cadastro_clientes.attributes("-topmost",True)
        janela_cadastro_clientes.title("CADASTRO DE CLIENTES")
        centraliza_janela(janela_cadastro_clientes)

        label_nome_cliente = ctk.CTkLabel(janela_cadastro_clientes, text="Nome do cliente")
        label_nome_cliente.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        campo_nome_cliente = ctk.CTkEntry(janela_cadastro_clientes, width=400)
        campo_nome_cliente.grid(row=1,column=1, padx=10, pady=10, sticky="w")

        botao_cadastrar_cliente = ctk.CTkButton(janela_cadastro_clientes, text="CADASTRAR", command=realiza_cadastro, width=150, height=22)
        botao_cadastrar_cliente.grid(row=2, column=1, padx=10, pady=20, sticky="w")

    def lista_tickets():
        sql = f"SELECT * FROM tickets"
        resultados = funcao_listar(sql)

        janela = ctk.CTkToplevel(app)
        janela.attributes("-topmost", True)
        janela.title("Tickets Cadastrados")
        centraliza_janela(janela)

        def obter_id(event):
            item_selecionado = tabela.selection()

            if item_selecionado:
                valores = tabela.item(item_selecionado, "values")

                id_ticket_selecionado = valores[0]
            
            janela_editar_ticket = ctk.CTkToplevel(app)
            janela_editar_ticket.attributes("-topmost",True)
            janela_editar_ticket.title("Editar Tickets")
            centraliza_janela(janela_editar_ticket)

            janela_editar_ticket.grid_columnconfigure(0, weight=0)
            janela_editar_ticket.grid_columnconfigure(1, weight=1)

            sql = "SELECT * FROM tickets T JOIN clientes C ON T.id_cliente = C.id WHERE T.id=%s"
            param = id_ticket_selecionado,
            retorno = funcao_select(sql,param)

            #TRATANDO DATA DE RETORNO
            data_banco = retorno[0][5]
            if isinstance(data_banco,str):
                data_tratada = datetime.strptime(data_banco, "%Y-%m-%d").strftime("%d/%m/%Y")
            else:
                data_tratada = data_banco.strftime("%d/%m/%Y")

            #RECUPERANDO STATUS
            status_retorno = retorno[0][8]

            def atualiza_tickets():
                nome_cliente = botao_nome_cliente.get()
                data_solicitacao = botao_data_solicitacao.get()
                descricao = botao_descricao.get()
                tecnico = botao_tecnico.get()
                status = select_status.get()

                sql = "UPDATE tickets SET id_cliente = %s, data_abertura = %s, descricao = %s, tecnico = %s, status_ticket=%s WHERE id=%s"
                params = (retorno[0][1], data_solicitacao,descricao,tecnico,status,id_ticket_selecionado)

                funcao_update(sql, params)

            label_titulo = ctk.CTkLabel(janela_editar_ticket, text="EDITAR DADOS DO CLIENTE", font=("Arial", 24, "bold"), anchor="center",)
            label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0), sticky="ew")
            
            frame_dados = ctk.CTkFrame(janela_editar_ticket)
            frame_dados.grid(row=1, column=0, columnspan=2, pady=10)

            label_nome_cliente = ctk.CTkLabel(frame_dados, text="Nome do cliente", width=100)
            label_nome_cliente.grid(row=1, column=0, padx=10, pady=10, sticky="e")

            botao_nome_cliente = ctk.CTkEntry(frame_dados, width=600)
            botao_nome_cliente.grid(row=1, column=1, padx=10, pady=10, sticky="w")
            botao_nome_cliente.insert(0, retorno[0][11])

            label_data_solicitacao = ctk.CTkLabel(frame_dados, text="Data da Solicitação", width=100)
            label_data_solicitacao.grid(row=2, column=0, padx=10, pady=10, sticky="e")

            botao_data_solicitacao = ctk.CTkEntry(frame_dados, width=600)
            botao_data_solicitacao.grid(row=2, column=1, padx=10, pady=10, sticky="w")
            botao_data_solicitacao.insert(0, data_tratada,)

            label_descricao = ctk.CTkLabel(frame_dados, text="Descrição", width=100)
            label_descricao.grid(row=3, column=0, padx=10, pady=10, sticky="e")

            botao_descricao = ctk.CTkEntry(frame_dados, width=600)
            botao_descricao.grid(row=3, column=1, padx=10, pady=10, sticky="w")
            botao_descricao.insert(0, retorno[0][9])

            label_tecnico = ctk.CTkLabel(frame_dados, text="Técnico", width=100)
            label_tecnico.grid(row=4, column=0, padx=10, pady=10, sticky="e")

            botao_tecnico = ctk.CTkEntry(frame_dados, placeholder_text=retorno[0][7], width=600)
            botao_tecnico.grid(row=4, column=1, padx=10, pady=10, sticky="w")
            botao_tecnico.insert(0, retorno[0][7])

            label_status = ctk.CTkLabel(frame_dados, text= "Status", width=100)
            label_status.grid(row=5, column=0, padx=10, pady=10, sticky = "e")

            select_status = ctk.CTkOptionMenu(frame_dados, values = status, width=600)
            select_status.grid(row=5, column=1, padx=10, pady=10, sticky="w")
            select_status.set(status_retorno)

            botao_atualizar = ctk.CTkButton(frame_dados, text="EDITAR TICKET", command=atualiza_tickets, width=150, height=22, fg_color="white", text_color="black")
            botao_atualizar.grid(row=6,column=0, columnspan=2, padx=10, pady=10, sticky="ew")


        if not resultados:
            label = ctk.CTkLabel(janela, text="Nenhum resultado encontrado!")
            label.grid(row=4, column=0, columnspan=3, pady=20)
            return

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="#ffffff",
                        fieldbackground="#2b2b2b",
                        rowheight=25)
        style.map("Treeview", background=[('selected', "#1f538d")])

        colunas = ("ID do Ticket", "Cliente", "Técnico", "Descrição")
        tabela = ttk.Treeview(janela, columns=colunas, show="headings")
        tabela.bind("<<TreeviewSelect>>",obter_id)

        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=120, anchor="center")

        tabela.column("Descrição", width=250, anchor="w")

        scrollbar = ctk.CTkScrollbar(janela, orientation="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        tabela.pack(side="left", fill="both", expand=True, padx=(20,0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0,20), pady=20)

        for linha in resultados:
            tabela.insert("", "end", values=(linha[0], linha[1], linha[7], linha[9]))
       
    # -- CONFIGURANDO A APARÊNCIA DO APP
    ctk.set_appearance_mode('dark')

    # -- CRIA A JANELA PRINCIPAL
    app = ctk.CTk()
    app.title('INSERE CLIENTES')

    centraliza_janela(app)

    def novajanela():
        nova_janela = ctk.CTk()
        nova_janela.title("JANELA 2")

    # Grid responsivo
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)
    
    # -- LABEL TÍTULO
    label_titulo = ctk.CTkLabel(app, text="CADASTRO DE TICKETS", font=("Arial", 24, "bold"), anchor="center", )
    label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    #FRAME CENTRALIZADO PARA OS BOTÕES
    frame_botoes = ctk.CTkFrame(app)
    frame_botoes.grid(row=1, column=0, columnspan=3, pady=(5,10))

    botao_pesquisar = ctk.CTkButton(frame_botoes,text="PESQUISAR", command=pesquisa, width=150, height=22, fg_color="white", text_color="black")
    botao_pesquisar.grid(row=1, column=0, padx=10, pady=20, sticky="e")

    botao_cadastrar_atendente = ctk.CTkButton(frame_botoes, text="CADASTRAR ATENDENTE", command=cadastro_atendente, width=150, height=22, fg_color="white", text_color="black")
    botao_cadastrar_atendente.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    
    botao_cadastrar_cliente = ctk.CTkButton(frame_botoes,text="CADASTRAR CLIENTE", command=cadastro_cliente, width=150, height=22,fg_color="white", text_color="black")
    botao_cadastrar_cliente.grid(row=1, column=2, padx=10, pady=20, sticky="w")

    botao_listar_tickets = ctk.CTkButton(frame_botoes, text="LISTAR TICKETS", command=lista_tickets, width = 150, height=22, fg_color="white", text_color="black")
    botao_listar_tickets.grid(row=1, column=3, padx=10, pady=20, sticky="w")

    #FRAME CENTRALIZADO PARA OS ENTRYS
    frame_campos = ctk.CTkFrame(app)
    frame_campos.grid(row=3, column=0, columnspan=2, pady=20)

     #--NOME CLIENTE
    clientes = []
    param = []

    sql = 'SELECT * FROM CLIENTES'
    resultados = funcao_select(sql,param)

    for linha in resultados:
        id_cliente = linha[0]
        nome_cliente = linha[1]

        clientes.append(f"{id_cliente} - {nome_cliente}")

    label_cliente = ctk.CTkLabel(frame_campos, text="Cliente", width=100)
    label_cliente.grid(row=2, column=0, padx=10,pady=10,sticky="e")

    campo_cliente = ctk.CTkOptionMenu(frame_campos, values=clientes,width=600)
    campo_cliente.grid(row=2, column=1, padx=55,pady=10,sticky="w")
    campo_cliente.set('Selecione')

    label_data_abertura = ctk.CTkLabel(frame_campos,text='Data da Solicitação', width=100)
    label_data_abertura.grid(row=3, column=0, padx=10,pady=10,sticky="e")

    campo_data_abertura = ctk.CTkEntry(frame_campos, placeholder_text='Digite a data', width=600)
    campo_data_abertura.grid(row=3, column=1, padx=55,pady=10,sticky="w")
    campo_data_abertura.bind("<KeyRelease>", mascara_data)

    #--HORA
    label_hora_abertura = ctk.CTkLabel(frame_campos,text="Hora da solicitação",width=100)
    label_hora_abertura.grid(row=4,column=0,padx=10,pady=10,sticky="e")

    campo_hora_abertura = ctk.CTkEntry(frame_campos,placeholder_text="Digite a hora",width=600)
    campo_hora_abertura.grid(row=4,column=1,padx=55,pady=10,sticky="w")
    campo_hora_abertura.bind("<KeyRelease>",mascara_hora)

    #--DESCRIÇÃO
    label_descricao = ctk.CTkLabel(frame_campos,text="Descrição",width=100)
    label_descricao.grid(row=5,column=0,padx=10,pady=10,sticky="e")

    campo_descricao = ctk.CTkEntry(frame_campos,placeholder_text="Digite a descrição",width=600)
    campo_descricao.grid(row=5,column=1,padx=55,pady=10,sticky="w")
    
    #--HORA PRIMEIRO RETORNO
    label_hora_primeiro_retorno = ctk.CTkLabel(frame_campos,text="Hora do primeiro retorno",width=100)
    label_hora_primeiro_retorno.grid(row=6,column=0,padx=10,pady=10,sticky="e")

    campo_hora_primeiro_retorno = ctk.CTkEntry(frame_campos,placeholder_text="Digite a hora do primeiro retorno",width=600)
    campo_hora_primeiro_retorno.grid(row=6,column=1,padx=55,pady=10,sticky="w")
    campo_hora_primeiro_retorno.bind("<KeyRelease>",mascara_hora)

    #--DATA RETORNO FINAL
    label_data_retorno_final = ctk.CTkLabel(frame_campos,text='Data do Retorno Final', width=100)
    label_data_retorno_final.grid(row=7, column=0, padx=10,pady=10,sticky="e")

    campo_data_retorno_final = ctk.CTkEntry(frame_campos, placeholder_text='Digite a data do Retorno Final', width=600)
    campo_data_retorno_final.grid(row=7, column=1, padx=55,pady=10,sticky="w")
    campo_data_retorno_final.bind("<KeyRelease>", mascara_data)

    #--HORA PRIMEIRO RETORNO
    label_hora_retorno_final = ctk.CTkLabel(frame_campos,text="Hora do retorno final",width=100)
    label_hora_retorno_final.grid(row=8,column=0,padx=10,pady=10,sticky="e")

    campo_hora_retorno_final = ctk.CTkEntry(frame_campos,placeholder_text="Digite a hora do retorno final",width=600)
    campo_hora_retorno_final.grid(row=8,column=1,padx=55,pady=10,sticky="w")
    campo_hora_retorno_final.bind("<KeyRelease>",mascara_hora)

    #--NOME ATENDENTE
    atendentes = []
    param = []

    sql = 'SELECT * FROM tecnicos'
    resultados = funcao_select(sql,param)

    for linha in resultados:
        id_atendente = linha[0]
        nome_atendente = linha[1]

        atendentes.append(f"{id_atendente} - {nome_atendente}")

    #--TECNICO
    label_tecnico = ctk.CTkLabel(frame_campos,text="Tecnico",width=100)
    label_tecnico.grid(row=9,column=0,padx=10,pady=10,sticky="e")

    campo_tecnico = ctk.CTkOptionMenu(frame_campos,values=atendentes, width=600)
    campo_tecnico.grid(row=9,column=1,padx=55,pady=10,sticky="w")
    campo_tecnico.set("Selecione")

    #--STATUS
    label_status = ctk.CTkLabel(frame_campos,text="Status",width=100)
    label_status.grid(row=10,column=0,padx=10,pady=10,sticky="e")

    campo_status = ctk.CTkOptionMenu(frame_campos,values=status,width=600)
    campo_status.grid(row=10,column=1,padx=55,pady=10,sticky="w")
    campo_status.set("Selecione")

    # -- BOTÃO CADASTRAR TICKET
    botao_cadastrar_ticket = ctk.CTkButton(frame_campos,text="CADASTRAR TICKET", command=cadastro_ticket, width=500, height=50, fg_color="white", text_color="black")
    botao_cadastrar_ticket.grid(row=12, column=0, columnspan=2, pady=20)

    app.mainloop()