from banco import funcao_select

def atualiza_menu_clientes():
    try:
        recarrega_clientes = funcao_select('SELECT * FROM clientes', [])
        clientes_novos = [f"{l[0]} - {l[1]}" for l in recarrega_clientes]
        return clientes_novos
        
    except Exception as e:
        print(f"Erro ao atualizar menus: {e}")
        return []
    
def atualiza_menu_tecnicos():
    try:
        recarrega_tecnicos = funcao_select('SELECT * FROM tecnicos', [])
        tecnicos_novos = [f"{l[0]} - {l[1]}" for l in recarrega_tecnicos]
        return tecnicos_novos
    
    except Exception as e:
        print(f"Erro ao atualizar menus: {e}")
        return []