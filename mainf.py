import customtkinter as tk
import json
import os
import ctypes
import sys

arquivo = "data.json"

#  C
try:
    caminho_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libprocess.so")
    if sys.platform == "win32":
        caminho_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "process.dll")
    
    lib = ctypes.CDLL(caminho_lib)
    
    
    lib.media.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float]
    lib.media.restype = ctypes.c_float
    
    lib.media_exame.argtypes = [ctypes.c_float, ctypes.c_float]
    lib.media_exame.restype = ctypes.c_float
    
    lib.media_com_atividades.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
    lib.media_com_atividades.restype = ctypes.c_float
except Exception as e:
    print(f"Erro ao carregar biblioteca C: {e}")
    lib = None

#---------------------------------------------------------------------FUNÇÕES DE ORGANIZAÇÃO

def load_data():
    if os.path.exists(arquivo):
        with open(arquivo,"r",encoding="utf-8") as f:
            try:
                dados = json.load(f)
                return dados
            except json.JSONDecodeError:
                return []
    else:
        return []
    
def save_data(lista):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(lista,f,indent=4,ensure_ascii=False)

def f_add_turma(codigo, lista_dados):

    for turma in lista_dados:
        if turma["codigo"] == codigo.upper() or turma["codigo"] == codigo:
            return False
    
    nova_turma = {
        "codigo": codigo,
        "alunos": {},
        "atividades": {}
    }
    lista_dados.append(nova_turma)
    save_data(lista_dados)
    return True


turmas = load_data()

#---------------------------------------------------------------------FUNÇÕES DE ORGANIZAÇÃO

def o_add_window():
    x = root.winfo_x()
    y = root.winfo_y()
    adicionar_turma = tk.CTkToplevel()
    adicionar_turma.geometry(f"+{x+50}+{y+50}")
    adicionar_turma.geometry("350x250")
    adicionar_turma.title("ADICIONAR TURMA")
    adicionar_turma.columnconfigure(0,weight=1)
    adicionar_turma.columnconfigure(1,weight=1)
    adicionar_turma.columnconfigure(2,weight=1)
    adicionar_turma.columnconfigure(3,weight=1)
    adicionar_turma.columnconfigure(4,weight=1)
    adicionar_turma.columnconfigure(5,weight=1)
    adicionar_turma.columnconfigure(6,weight=1)
    adicionar_turma.columnconfigure(7,weight=1)
    adicionar_turma.columnconfigure(8,weight=1)

    adicionar_turma.rowconfigure(0, weight=1)
    adicionar_turma.rowconfigure(1, weight=1)
    adicionar_turma.rowconfigure(2, weight=1)
    adicionar_turma.rowconfigure(3, weight=1)
    adicionar_turma.rowconfigure(4, weight=1)
    adicionar_turma.rowconfigure(5, weight=1)
    adicionar_turma.rowconfigure(6, weight=1)
    adicionar_turma.rowconfigure(7, weight=1)
    adicionar_turma.rowconfigure(8, weight=1)


    entrada1 = tk.CTkEntry(adicionar_turma,placeholder_text="Insira aqui o codigo da turma...",font=("Arial",20),width=350,height=45)
    entrada1.grid(row=0,column=0,pady=5,sticky="w")

    label_i = tk.CTkLabel(adicionar_turma,text="",font=("Arial",18))
    label_i.grid(row=4,column=0)

    estado = tk.IntVar(value=1)
    check_upper = tk.CTkCheckBox(adicionar_turma,text="Inserir codigo Upper Case",variable=estado)
    check_upper.grid(row=2,column=0)

    def click_insert():
        estado_valor = estado.get()
        dados = load_data()
        if estado_valor == 1:
            codigo = entrada1.get().upper()
        elif estado_valor == 0:
            codigo = entrada1.get()
        else:
            codigo = ""

        if codigo.strip() == "":
            label_i.configure(text="Digite o codigo da turma!")
            label_i.after(2000,lambda:label_i.configure(text=""))

            return
        


        isadded = f_add_turma(codigo,dados)
        
        if isadded:
            label_i.configure(text=f"Turma adicionada!( {codigo} )")
            label_i.after(2000,lambda:label_i.configure(text=""))
        else:
            label_i.configure(text=f"Turma {codigo} ja existe!")

        label_i.after(2000,lambda:label_i.configure(text=""))
        entrada1.delete(0,tk.END)
        update_list(frame_turmas)

    botao_inserir = tk.CTkButton(adicionar_turma,text="INSERIR",font=("Arial",20),height=45,command=click_insert)
    botao_inserir.grid(row=1,column=0,sticky="n")

    adicionar_turma.transient(root)
    adicionar_turma.focus()
    adicionar_turma.grab_set()


def o_manage_window():#----------------------------------------------------Manage
    x = root.winfo_x()
    y = root.winfo_y()
    manage = tk.CTk()
    manage.geometry(f"+{x+50}+{y+50}")
    manage.geometry("1000x900")
    manage.title("Configurar Elementos")
    for i in range(15):
        manage.columnconfigure(i,weight=1)
    
    for i in range(15):
        manage.rowconfigure(i,weight=1)
    
    codigos = []

    for turma in turmas:
        codigos.append(turma["codigo"])


    s_label = tk.CTkLabel(manage,text="",font=("Arial",20,"bold"))
    s_label.grid(column=0,row=1,sticky="nw")

    def intermedio(choice=None):
        try:
            botao_alunos.destroy()
            botao_atividades.destroy()
        except Exception:
            pass
        
        show_manager()

    select_box = tk.CTkComboBox(manage,values=codigos,width=300,height=50,font=("Arial",20,"bold"),command=intermedio)
    select_box.grid(column=0,row=0,sticky="wn")
    select_box.set("Selecione a turma...")


    def show_manager():
        if select_box.get() == "Selecione a turma...":
            pass
        else:
            global turma_selecionada
            turma_selecionada = select_box.get()
            s_label.configure(text=f"TURMA SELECIONADA: {turma_selecionada}")
            s_label.grid(column=0,row=1,sticky="nw")

        def hide_manage():
            select_box.grid_forget()
            s_label.grid_forget()
            botao_alunos.grid_forget()
            botao_atividades.grid_forget()
            update_button.grid_forget()
            tip.grid_forget()
            delete_button.grid_forget()

        def back_manage():
            
            try:
                back_button_student.destroy()
            except:
                pass
            
            try:
                show_label_student.destroy()
            except:
                pass
            
            try:
                add_student_button.destroy()
            except:
                pass
            
            try:
                addin_student_button.destroy()
            except:
                pass

            try:
                name_entry.destroy()
            except:
                pass
            
            try:
                id_entry.destroy()
            except:
                pass

            
            try:
                back_button_activities.destroy()
            except:
                pass
            
            try:
                show_label_activities.destroy()
            except:
                pass
            
            try:
                add_activity_button.destroy()
            except:
                pass
            
            try:
                activity_name_entry.destroy()
            except:
                pass
            
            try:
                activity_desc_entry.destroy()
            except:
                pass
            
            try:
                activity_date_entry.destroy()
            except:
                pass
            
            try:
                activity_value_entry.destroy()
            except:
                pass
            
            try:
                addin_activity_button.destroy()
            except:
                pass
            
            try:
                remove_activity_button.destroy()
            except:
                pass
            
            try:
                activity_status_label.destroy()
            except:
                pass
            
            try:
                desc_label.destroy()
            except:
                pass
            
            try:
                date_frame.destroy()
            except:
                pass
            
            try:
                calendar_button.destroy()
            except:
                pass
            
            try:
                value_label.destroy()
            except:
                pass

            
            try:
                remove_student_button.destroy()
            except:
                pass
            
            try:
                upperID_checkbox.destroy()
            except:
                pass
            
            try:
                local_status_label.destroy()
            except:
                pass

            for widget in manage.grid_slaves():
                info = widget.grid_info()
                if info and 'row' in info:
                    row = info['row']
                    if row in [4, 5, 6]:
                        try:
                            widget.grid_forget()
                        except:
                            pass

            
            select_box.grid(column=0,row=0,sticky="wn")
            s_label.grid(column=0,row=1,sticky="nw")
            botao_alunos.grid(column=0,row=3,sticky="wn",padx=5)
            botao_atividades.grid(column=0,row=2,sticky="wn",padx=5)
            update_button.grid(column=1,row=0,sticky="wn")
            tip.grid(column=0,row=11,sticky="s")
            delete_button.grid(column=2,row=0,sticky="nw")
        #--------------------------------------ADICIONAR/REMOVER ALUNOS
        def manage_student():
            
            try:
                if name_entry.winfo_exists():
                    return
            except:
                pass

            def f_add_student(turma_codigo,nome,matricula):
                dados = load_data()
                for turma in dados:
                    if turma["codigo"] == turma_codigo:
                        if matricula in turma["alunos"]:
                            return False
                        turma["alunos"][matricula] = {

                            "nome":nome,
                            "notas":[]
                        }
                        save_data(dados)
                        return True
                return False

            def show_addstudent():
                global name_entry
                global id_entry
                global addin_student_button
                global remove_student_button
                global upperID_checkbox
                global local_status_label
                
                try:
                    if name_entry.winfo_exists():
                        return
                except:
                    pass

                def click_add_student():
                    turma_selecionada = select_box.get()
                    local_state_value = local_state.get()
                    nome = name_entry.get().title()
                    if local_state_value == 1:
                        matricula = id_entry.get().upper()
                    else:
                        matricula = id_entry.get()

                    local_status = f_add_student(turma_selecionada,nome,matricula)
                    if local_status:
                        update_student_scrollable(added_window_show_scroll)
                        local_status_label.configure(text="Aluno adicionado!")
                        local_status_label.after(2500,lambda:local_status_label.configure(text=""))
                        name_entry.delete(0,tk.END)
                        id_entry.delete(0,tk.END)
                    else:
                        update_student_scrollable(added_window_show_scroll)
                        local_status_label.configure(text="Não foi possível adicionar o aluno. Tente novamente!")
                        local_status_label.after(2500,lambda:local_status_label.configure(text=""))
                        name_entry.delete(0,tk.END)
                        id_entry.delete(0,tk.END)

                def confirm_delete_student_window():
                    confirm_window = tk.CTkToplevel(manage)
                    confirm_window.geometry("400x250")
                    confirm_window.title("CONFIRMAR OPERAÇÃO")

                    def confirm():
                        turma_selecionada = select_box.get()
                        local_state_value = upperID_checkbox.get()
                        if local_state_value == 1:
                            local_status = remove_student(turma_selecionada,id_entry.get().upper())
                            if local_status:
                                update_student_scrollable(added_window_show_scroll)
                                confirm_window.destroy()
                                id_entry.delete(0,tk.END)
                                status_label.configure(text="Aluno removido!")
                                status_label.after(2500,lambda:status_label.configure(text=""))
                            else:
                                update_student_scrollable(added_window_show_scroll)
                                confirm_window.destroy()
                                id_entry.delete(0,tk.END)
                                status_label.configure(text="Não foi possível remover o aluno!")
                                status_label.after(2500,lambda:status_label.configure(text=""))

                    def cancel():
                        update_student_scrollable(added_window_show_scroll)
                        confirm_window.destroy()


                    confirm_label = tk.CTkLabel(confirm_window,text="Deseja continuar?",font=("Arial",20,"bold"))
                    confirm_label.pack(side="top",expand=True,padx=10,pady=5)    


                    b_yes = tk.CTkButton(confirm_window,text="Sim",font=("Arial",20,"bold"),width=100,height=30,fg_color="red",command=confirm)
                    b_yes.pack(side="left",expand=True,padx=10,pady=10)


                    b_no = tk.CTkButton(confirm_window,text="Não",font=("Arial",20,"bold"),width=100,height=30,fg_color="gray",command=cancel)
                    b_no.pack(side="right",expand=True,padx=10,pady=10)

                    confirm_window.transient(manage)
                    confirm_window.focus()
                    confirm_window.grab_set()
                    confirm_window.wait_window()

                    show_addstudent()

                def remove_student(turma_codigo, matricula):
                    dados = load_data()

                    for turma in dados:
                        if turma["codigo"] == turma_codigo:
                            if matricula in turma["alunos"]:
                                del turma["alunos"][matricula]
                                save_data(dados)
                                return True
                            else:
                                return False
                    return False

                def show_remove_student_list():
                    
                    remove_window = tk.CTkToplevel(manage)
                    remove_window.geometry("600x500")
                    remove_window.title("Remover Aluno")
                    
                    turma_selecionada = select_box.get()
                    
                    label_info = tk.CTkLabel(remove_window, text="Selecione o aluno que deseja remover:", 
                                           font=("Arial", 18, "bold"))
                    label_info.pack(pady=10, padx=10)
                    
                    scroll_frame = tk.CTkScrollableFrame(remove_window)
                    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
                    
                    dados = load_data()
                    alunos_encontrados = False
                    
                    for turma in dados:
                        if turma["codigo"] == turma_selecionada:
                            if turma["alunos"]:
                                alunos_encontrados = True
                                for matricula, dados_aluno in turma["alunos"].items():
                                    def criar_comando_remover(mat, nome):
                                        def cmd():
                                            confirmar_remocao(mat, nome, remove_window)
                                        return cmd
                                    
                                    item_frame = tk.CTkFrame(scroll_frame)
                                    item_frame.pack(fill="x", padx=5, pady=5)
                                    
                                    nome_aluno = dados_aluno.get("nome", "Sem nome")
                                    info_label = tk.CTkLabel(item_frame, 
                                                            text=f"{matricula} - {nome_aluno}",
                                                            font=("Arial", 16))
                                    info_label.pack(side="left", padx=10, pady=5)
                                    
                                    btn_remove = tk.CTkButton(item_frame, text="REMOVER", 
                                                             fg_color="red", width=100,
                                                             command=criar_comando_remover(matricula, nome_aluno))
                                    btn_remove.pack(side="right", padx=10, pady=5)
                            break
                    
                    if not alunos_encontrados:
                        no_student_label = tk.CTkLabel(scroll_frame, 
                                                       text="Nenhum aluno cadastrado nesta turma.",
                                                       font=("Arial", 16))
                        no_student_label.pack(pady=20)
                    
                    def confirmar_remocao(matricula, nome_aluno, parent_window):
                        confirm_window = tk.CTkToplevel(parent_window)
                        confirm_window.geometry("450x200")
                        confirm_window.title("CONFIRMAR REMOÇÃO")
                        
                        confirm_label = tk.CTkLabel(confirm_window, 
                                                   text=f"Deseja remover o aluno:\n'{nome_aluno}' (Matrícula: {matricula})?",
                                                   font=("Arial", 18, "bold"))
                        confirm_label.pack(pady=20)
                        
                        def confirmar():
                            turma_selecionada = select_box.get()
                            if remove_student(turma_selecionada, matricula):
                                update_student_scrollable(added_window_show_scroll)
                                local_status_label.configure(text=f"Aluno '{nome_aluno}' removido!")
                                local_status_label.after(3000, lambda: local_status_label.configure(text=""))
                                confirm_window.destroy()
                                parent_window.destroy()
                            else:
                                local_status_label.configure(text="Erro ao remover aluno!")
                                local_status_label.after(2500, lambda: local_status_label.configure(text=""))
                                confirm_window.destroy()
                        
                        def cancelar():
                            confirm_window.destroy()
                        
                        btn_frame = tk.CTkFrame(confirm_window)
                        btn_frame.pack(pady=10)
                        
                        btn_yes = tk.CTkButton(btn_frame, text="Sim", font=("Arial", 18, "bold"),
                                             width=120, height=40, fg_color="red", command=confirmar)
                        btn_yes.pack(side="left", padx=10)
                        
                        btn_no = tk.CTkButton(btn_frame, text="Não", font=("Arial", 18, "bold"),
                                            width=120, height=40, fg_color="gray", command=cancelar)
                        btn_no.pack(side="right", padx=10)
                        
                        confirm_window.transient(parent_window)
                        confirm_window.focus()
                        confirm_window.grab_set()
                    
                    btn_close = tk.CTkButton(remove_window, text="Fechar", width=150, height=40,
                                           command=remove_window.destroy)
                    btn_close.pack(pady=10)
                    
                    remove_window.transient(manage)
                    remove_window.focus()
                    remove_window.grab_set()

                def confirm_delete_student_window():
                    
                    show_remove_student_list()
                    
                
                def click_remove_student():
                    
                    confirm_delete_student_window()

                
                name_entry = tk.CTkEntry(manage,placeholder_text="Nome do aluno...",font=("Arial",20),width=250,height=50)
                name_entry.grid(column=0,row=4,sticky="sw",pady=5)
                id_entry = tk.CTkEntry(manage,placeholder_text="Número da matrícula...",font=("Arial",20),width=200,height=50)
                id_entry.grid(column=0,row=5,sticky="nw",pady=5)
                
                
                addin_student_button = tk.CTkButton(manage,text="ADICIONAR",font=("Arial",20,"bold"),width=200,height=50,command=click_add_student)
                addin_student_button.grid(column=1,row=4,sticky="e",padx=5)
                
                remove_student_button = tk.CTkButton(manage,text="REMOVER ALUNO",font=("Arial",20,"bold"),width=200,height=50,fg_color="red",command=click_remove_student)
                remove_student_button.grid(column=2,row=4,sticky="w",padx=5)
                
                local_status_label = tk.CTkLabel(manage,text="",font=("Arial",18,"bold"))
                local_status_label.grid(column=0,row=6,sticky="w",columnspan=6)

                local_status_label.configure(text="Clique em 'Remover Aluno' para ver a lista de alunos cadastrados.")
                local_status_label.after(5000,lambda:local_status_label.configure(text=""))

             
                local_state = tk.IntVar(value=1)
                upperID_checkbox = tk.CTkCheckBox(manage,text="Matrícula Upper Case",font=("Arial",16,"bold"),variable=local_state)
                upperID_checkbox.grid(column=0,row=4,sticky="n",pady=2)

                def update_student_scrollable(frame):
                    global turmas
                    turmas = load_data()
                    turma_selecionada = select_box.get()

                    for widget in added_window_show_scroll.winfo_children():
                        widget.destroy()

                    for turma in turmas:
                        if turma["codigo"] == turma_selecionada:
                            for matricula,dados_aluno in turma["alunos"].items():
                                nome = dados_aluno["nome"]
                                item = tk.CTkLabel(added_window_show_scroll,text=f"{matricula} - {nome}",font=("Arial",22))
                                item.pack(fill="x",padx=10,pady=5)
                            break

                added_window = tk.CTkToplevel(manage)
                added_window.geometry("450x450")
                added_window.title("Alunos inseridos")
                added_window_show_scroll = tk.CTkScrollableFrame(added_window,label_text=turma_selecionada)
                added_window_show_scroll.pack(fill="both",expand=True,padx=5,pady=5)
                update_student_scrollable(added_window_show_scroll)
                
                added_window.transient(manage)

                
                def on_added_window_close():
                    try:
                        name_entry.destroy()
                    except:
                        pass
                    try:
                        id_entry.destroy()
                    except:
                        pass
                    try:
                        addin_student_button.destroy()
                    except:
                        pass
                    try:
                        remove_student_button.destroy()
                    except:
                        pass
                    try:
                        upperID_checkbox.destroy()
                    except:
                        pass
                    try:
                        local_status_label.destroy()
                    except:
                        pass
                    added_window.destroy()

                added_window.protocol("WM_DELETE_WINDOW", on_added_window_close)



        #--------------------------------------ADICIONAR/REMOVER ALUNOS


            hide_manage()
            turma_selecionada = select_box.get()
            global show_label_student
            global back_button_student
            global add_student_button
            show_label_student = tk.CTkLabel(manage,text=f"TURMA SELECIONADA: {turma_selecionada}",font=("Arial",15,"bold"),width=200)
            show_label_student.grid(column=1,row=0,sticky="nw")

            back_button_student = tk.CTkButton(manage,text="VOLTAR",font=("Arial",20,"bold"),width=100,height=50,command=back_manage)
            back_button_student.grid(column=0,row=0,sticky="nw")

            add_student_button = tk.CTkButton(manage,text="ALUNO",font=("Arial",20,"bold"),width=100,height=50,command=show_addstudent)
            add_student_button.grid(column=0,row=1,sticky="w")


        #--------------------------------------ADICIONAR/REMOVER ATIVIDADES
        def manage_activities():
            turma_selecionada = select_box.get()
            
            def f_add_activity(turma_codigo,nome_atividade,descricao,data_entrega,valor):
                dados = load_data()
                for turma in dados:
                    if turma["codigo"] == turma_codigo:
                        if nome_atividade in turma["atividades"]:
                            return False
                        turma["atividades"][nome_atividade] = {
                            "descricao":descricao,
                            "data_entrega":data_entrega,
                            "valor":valor
                        }
                        save_data(dados)
                        return True
                return False
            
            def show_add_activities():
                global activity_name_entry
                global activity_desc_entry
                global activity_date_entry
                global activity_value_entry
                global addin_activity_button
                global remove_activity_button
                global activity_status_label
                global add_activity_button
                global desc_label
                global date_frame
                global calendar_button
                global value_label
                
                
                try:
                    if activity_name_entry.winfo_exists():
                        return
                except:
                    pass

                def open_calendar():
                    """Abre um calendário para seleção de data"""
                    cal_window = tk.CTkToplevel(manage)
                    cal_window.geometry("350x400")
                    cal_window.title("Selecionar Data")
                    
                    from datetime import datetime
                    import calendar
                    
                    
                    nav_frame = tk.CTkFrame(cal_window)
                    nav_frame.pack(pady=10, padx=10, fill="x")
                    
                    current_date = datetime.now()
                    selected_month = tk.IntVar(value=current_date.month)
                    selected_year = tk.IntVar(value=current_date.year)
                    selected_day = tk.IntVar(value=0)
                    
                    month_label = tk.CTkLabel(nav_frame, text="", font=("Arial", 18, "bold"))
                    month_label.pack()
                    
                    
                    cal_frame = tk.CTkFrame(cal_window)
                    cal_frame.pack(pady=10, padx=10, fill="both", expand=True)
                    
                    def update_calendar():
                        
                        for widget in cal_frame.winfo_children():
                            widget.destroy()
                        
                        month = selected_month.get()
                        year = selected_year.get()
                        
                        
                        month_names = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                        month_label.configure(text=f"{month_names[month-1]} {year}")
                        
                        
                        days = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
                        for i, day in enumerate(days):
                            label = tk.CTkLabel(cal_frame, text=day, font=("Arial", 12, "bold"))
                            label.grid(row=0, column=i, padx=2, pady=2)
                        
                        
                        cal = calendar.monthcalendar(year, month)
                        
                        def select_day(day):
                            selected_day.set(day)
                            date_str = f"{day:02d}/{month:02d}/{year}"
                            activity_date_entry.configure(state="normal")
                            activity_date_entry.delete(0, tk.END)
                            activity_date_entry.insert(0, date_str)
                            activity_date_entry.configure(state="readonly")
                            cal_window.destroy()
                        
                        
                        for week_num, week in enumerate(cal):
                            for day_num, day in enumerate(week):
                                if day == 0:
                                    label = tk.CTkLabel(cal_frame, text="")
                                    label.grid(row=week_num+1, column=day_num, padx=2, pady=2)
                                else:
                                    btn = tk.CTkButton(cal_frame, text=str(day), width=40, height=30,
                                                      command=lambda d=day: select_day(d))
                                    btn.grid(row=week_num+1, column=day_num, padx=2, pady=2)
                    
                    def prev_month():
                        month = selected_month.get()
                        year = selected_year.get()
                        if month == 1:
                            selected_month.set(12)
                            selected_year.set(year - 1)
                        else:
                            selected_month.set(month - 1)
                        update_calendar()
                    
                    def next_month():
                        month = selected_month.get()
                        year = selected_year.get()
                        if month == 12:
                            selected_month.set(1)
                            selected_year.set(year + 1)
                        else:
                            selected_month.set(month + 1)
                        update_calendar()
                    
                    btn_prev = tk.CTkButton(nav_frame, text="<", width=50, command=prev_month)
                    btn_prev.pack(side="left", padx=5)
                    
                    btn_next = tk.CTkButton(nav_frame, text=">", width=50, command=next_month)
                    btn_next.pack(side="right", padx=5)
                    
                    update_calendar()
                    
                    cal_window.transient(manage)
                    cal_window.focus()
                    cal_window.grab_set()

                def click_add_activity():
                    turma_selecionada = select_box.get()
                    nome = activity_name_entry.get().strip()
                    descricao = activity_desc_entry.get("1.0", tk.END).strip()
                    data = activity_date_entry.get().strip()
                    try:
                        valor = float(activity_value_entry.get().strip())
                    except ValueError:
                        activity_status_label.configure(text="Valor deve ser um número!")
                        activity_status_label.after(2500, lambda: activity_status_label.configure(text=""))
                        return

                    if nome == "":
                        activity_status_label.configure(text="Digite o nome da atividade!")
                        activity_status_label.after(2500, lambda: activity_status_label.configure(text=""))
                        return

                    local_status = f_add_activity(turma_selecionada, nome, descricao, data, valor)
                    if local_status:
                        update_activities_scrollable(activities_window_scroll)
                        activity_status_label.configure(text="Atividade adicionada!")
                        activity_status_label.after(2500, lambda: activity_status_label.configure(text=""))
                        activity_name_entry.delete(0, tk.END)
                        activity_desc_entry.delete("1.0", tk.END)
                        activity_date_entry.configure(state="normal")
                        activity_date_entry.delete(0, tk.END)
                        activity_date_entry.configure(state="readonly")
                        activity_value_entry.delete(0, tk.END)
                    else:
                        activity_status_label.configure(text="Atividade já existe!")
                        activity_status_label.after(2500, lambda: activity_status_label.configure(text=""))

                def remove_activity(turma_codigo, nome_atividade):
                    dados = load_data()

                    for turma in dados:
                        if turma["codigo"] == turma_codigo:
                            if nome_atividade in turma["atividades"]:
                                del turma["atividades"][nome_atividade]
                                save_data(dados)
                                return True
                            else:
                                return False
                    return False

                def show_remove_activity_list():
                    
                    remove_window = tk.CTkToplevel(manage)
                    remove_window.geometry("600x500")
                    remove_window.title("Remover Atividade")
                    
                    turma_selecionada = select_box.get()
                    
                    label_info = tk.CTkLabel(remove_window, text="Selecione a atividade que deseja remover:", 
                                           font=("Arial", 18, "bold"))
                    label_info.pack(pady=10, padx=10)
                    
                    scroll_frame = tk.CTkScrollableFrame(remove_window)
                    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
                    
                    dados = load_data()
                    atividades_encontradas = False
                    
                    for turma in dados:
                        if turma["codigo"] == turma_selecionada:
                            if turma["atividades"]:
                                atividades_encontradas = True
                                for nome_atividade, dados_atividade in turma["atividades"].items():
                                    def criar_comando_remover(nome):
                                        def cmd():
                                            confirmar_remocao(nome, remove_window)
                                        return cmd
                                    
                                    item_frame = tk.CTkFrame(scroll_frame)
                                    item_frame.pack(fill="x", padx=5, pady=5)
                                    
                                    info_label = tk.CTkLabel(item_frame, 
                                                            text=f"{nome_atividade} - {dados_atividade.get('valor', 0)} pontos",
                                                            font=("Arial", 16))
                                    info_label.pack(side="left", padx=10, pady=5)
                                    
                                    btn_remove = tk.CTkButton(item_frame, text="REMOVER", 
                                                             fg_color="red", width=100,
                                                             command=criar_comando_remover(nome_atividade))
                                    btn_remove.pack(side="right", padx=10, pady=5)
                            break
                    
                    if not atividades_encontradas:
                        no_activity_label = tk.CTkLabel(scroll_frame, 
                                                       text="Nenhuma atividade cadastrada nesta turma.",
                                                       font=("Arial", 16))
                        no_activity_label.pack(pady=20)
                    
                    def confirmar_remocao(nome_atividade, parent_window):
                        confirm_window = tk.CTkToplevel(parent_window)
                        confirm_window.geometry("450x200")
                        confirm_window.title("CONFIRMAR REMOÇÃO")
                        
                        confirm_label = tk.CTkLabel(confirm_window, 
                                                   text=f"Deseja remover a atividade:\n'{nome_atividade}'?",
                                                   font=("Arial", 18, "bold"))
                        confirm_label.pack(pady=20)
                        
                        def confirmar():
                            turma_selecionada = select_box.get()
                            if remove_activity(turma_selecionada, nome_atividade):
                                update_activities_scrollable(activities_window_scroll)
                                activity_status_label.configure(text=f"Atividade '{nome_atividade}' removida!")
                                activity_status_label.after(3000, lambda: activity_status_label.configure(text=""))
                                confirm_window.destroy()
                                parent_window.destroy()
                            else:
                                activity_status_label.configure(text="Erro ao remover atividade!")
                                activity_status_label.after(2500, lambda: activity_status_label.configure(text=""))
                                confirm_window.destroy()
                        
                        def cancelar():
                            confirm_window.destroy()
                        
                        btn_frame = tk.CTkFrame(confirm_window)
                        btn_frame.pack(pady=10)
                        
                        btn_yes = tk.CTkButton(btn_frame, text="Sim", font=("Arial", 18, "bold"),
                                             width=120, height=40, fg_color="red", command=confirmar)
                        btn_yes.pack(side="left", padx=10)
                        
                        btn_no = tk.CTkButton(btn_frame, text="Não", font=("Arial", 18, "bold"),
                                            width=120, height=40, fg_color="gray", command=cancelar)
                        btn_no.pack(side="right", padx=10)
                        
                        confirm_window.transient(parent_window)
                        confirm_window.focus()
                        confirm_window.grab_set()
                    
                    btn_close = tk.CTkButton(remove_window, text="Fechar", width=150, height=40,
                                           command=remove_window.destroy)
                    btn_close.pack(pady=10)
                    
                    remove_window.transient(manage)
                    remove_window.focus()
                    remove_window.grab_set()

                def confirm_delete_activity_window():
                    
                    show_remove_activity_list()

                def click_remove_activity():
                    
                    confirm_delete_activity_window()

                activity_name_entry = tk.CTkEntry(manage, placeholder_text="Nome da atividade...", font=("Arial", 20), width=300, height=50)
                activity_name_entry.grid(column=0, row=4, sticky="w", pady=5, padx=5, columnspan=2)

                desc_label = tk.CTkLabel(manage, text="Descrição da atividade:", font=("Arial", 16, "bold"))
                desc_label.grid(column=0, row=5, sticky="w", padx=5)
                
                activity_desc_entry = tk.CTkTextbox(manage, font=("Arial", 16), width=600, height=120)
                activity_desc_entry.grid(column=0, row=6, sticky="w", pady=5, padx=5, columnspan=4)

                date_frame = tk.CTkFrame(manage)
                date_frame.grid(column=0, row=7, sticky="w", pady=5, padx=5)
                
                date_label = tk.CTkLabel(date_frame, text="Data:", font=("Arial", 16))
                date_label.pack(side="left", padx=5)
                
                activity_date_entry = tk.CTkEntry(date_frame, placeholder_text="Selecione...", font=("Arial", 16), width=150, height=40, state="readonly")
                activity_date_entry.pack(side="left", padx=5)
                
                calendar_button = tk.CTkButton(date_frame, text="Calendário", font=("Arial", 16), width=130, height=40, command=open_calendar)
                calendar_button.pack(side="left", padx=5)

                
                value_label = tk.CTkLabel(date_frame, text="Valor:", font=("Arial", 16))
                value_label.pack(side="left", padx=(20, 5))
                
                activity_value_entry = tk.CTkEntry(date_frame, placeholder_text="Pontos...", font=("Arial", 16), width=100, height=40)
                activity_value_entry.pack(side="left", padx=5)

                
            
            
            
            
                addin_activity_button = tk.CTkButton(manage, text="ADICIONAR", font=("Arial", 20, "bold"), width=200, height=50, command=click_add_activity)
                addin_activity_button.grid(column=1, row=8, sticky="e", padx=5, pady=10)

                remove_activity_button = tk.CTkButton(manage, text="REMOVER ATIVIDADE", font=("Arial", 20, "bold"), width=200, height=50, fg_color="red", command=click_remove_activity)
                remove_activity_button.grid(column=2, row=8, sticky="w", padx=5, pady=10)

                activity_status_label = tk.CTkLabel(manage, text="", font=("Arial", 18, "bold"))
                activity_status_label.grid(column=0, row=9, sticky="w", columnspan=6, padx=5)

                activity_status_label.configure(text="Clique em 'Remover Atividade' para ver a lista de atividades cadastradas.")
                activity_status_label.after(5000, lambda: activity_status_label.configure(text=""))

                def update_activities_scrollable(frame):
                    global turmas
                    turmas = load_data()
                    turma_selecionada = select_box.get()

                    for widget in activities_window_scroll.winfo_children():
                        widget.destroy()

                    for turma in turmas:
                        if turma["codigo"] == turma_selecionada:
                            for nome_atividade, dados_atividade in turma["atividades"].items():
                                descricao = dados_atividade.get("descricao", "Sem descrição")
                                data_entrega = dados_atividade.get("data_entrega", "Sem data")
                                valor = dados_atividade.get("valor", 0)
                                
                                item_frame = tk.CTkFrame(activities_window_scroll)
                                item_frame.pack(fill="x", padx=10, pady=5)
                                
                                nome_label = tk.CTkLabel(item_frame, text=f"Nome: {nome_atividade}", font=("Arial", 18, "bold"))
                                nome_label.pack(anchor="w", padx=5, pady=2)
                                
                                desc_label = tk.CTkLabel(item_frame, text=f"Descrição: {descricao}", font=("Arial", 14))
                                desc_label.pack(anchor="w", padx=5, pady=2)
                                
                                data_label = tk.CTkLabel(item_frame, text=f"Data: {data_entrega}", font=("Arial", 14))
                                data_label.pack(anchor="w", padx=5, pady=2)
                                
                                valor_label = tk.CTkLabel(item_frame, text=f"Valor: {valor} pontos", font=("Arial", 14))
                                valor_label.pack(anchor="w", padx=5, pady=2)
                            break

                activities_window = tk.CTkToplevel(manage)
                activities_window.geometry("500x500")
                activities_window.title("Atividades cadastradas")
                activities_window_scroll = tk.CTkScrollableFrame(activities_window, label_text=turma_selecionada)
                activities_window_scroll.pack(fill="both", expand=True, padx=5, pady=5)
                update_activities_scrollable(activities_window_scroll)

                activities_window.transient(manage)

                
                def on_activities_window_close():
                    try:
                        activity_name_entry.destroy()
                    except:
                        pass
                    try:
                        activity_desc_entry.destroy()
                    except:
                        pass
                    try:
                        desc_label.destroy()
                    except:
                        pass
                    try:
                        date_frame.destroy()
                    except:
                        pass
                    try:
                        activity_date_entry.destroy()
                    except:
                        pass
                    try:
                        activity_value_entry.destroy()
                    except:
                        pass
                    try:
                        calendar_button.destroy()
                    except:
                        pass
                    try:
                        value_label.destroy()
                    except:
                        pass
                    try:
                        addin_activity_button.destroy()
                    except:
                        pass
                    try:
                        remove_activity_button.destroy()
                    except:
                        pass
                    try:
                        activity_status_label.destroy()
                    except:
                        pass
                    activities_window.destroy()

                activities_window.protocol("WM_DELETE_WINDOW", on_activities_window_close)

            hide_manage()
            global show_label_activities
            global back_button_activities
            global add_activity_button
            
            show_label_activities = tk.CTkLabel(manage,text=f"TURMA SELECIONADA: {turma_selecionada}",font=("Arial",15,"bold"),width=200)
            show_label_activities.grid(column=1,row=0,sticky="nw")
            
            back_button_activities = tk.CTkButton(manage,text="VOLTAR",font=("Arial",20,"bold"),width=100,height=50,command=back_manage)
            back_button_activities.grid(column=0,row=0,sticky="nw")

            add_activity_button = tk.CTkButton(manage, text="ATIVIDADE", font=("Arial", 20, "bold"), width=120, height=50, command=show_add_activities)
            add_activity_button.grid(column=0, row=1, sticky="w")


        #--------------------------------------ADICIONAR/REMOVER ATIVIDADES

        global botao_alunos
        global botao_atividades

        if select_box.get() == "Selecione a turma...":
            pass
        else:

            botao_alunos = tk.CTkButton(manage,text="  ALUNOS  ",font=("Arial",20,"bold"),width=130,height=50,command=manage_student)
            botao_alunos.grid(column=0,row=3,sticky="wn",padx=5)

            botao_atividades = tk.CTkButton(manage,text="ATIVIDADES",font=("Arial",20,"bold"),width=100,height=50,command=manage_activities)
            botao_atividades.grid(column=0,row=2,sticky="wn",padx=5)


    status_label = tk.CTkLabel(manage,text="",font=("Arial",25,"bold"))
    status_label.grid(column=0,row=6,sticky="nw")

    def delete_class(codigo,turmas):
        new_list = []
        for turma in turmas:
            if turma["codigo"] != codigo:
                new_list.append(turma)

        if len(new_list) != len(turmas):
            save_data(new_list)
            return True
        else:
            return False
        
    def get_ids_all(turmas):
        turmas = load_data()
        codigos = []
        for turma in turmas:
            codigos.append(turma["codigo"])

        return codigos
        

    def confirm_delete_class_window():
        turma_selecionada = select_box.get()

        def confirm():
            global turmas
            delete = delete_class(turma_selecionada,turmas)
            if delete:

                try:
                    botao_alunos.grid_remove()
                    botao_atividades.grid_remove()
                    s_label.grid_remove()

                except Exception:
                    pass

                turmas = load_data()

                codigos = get_ids_all(turmas)
                select_box.configure(values=codigos)
                select_box.set("Selecione a turma...")

                update_list(frame_turmas)

                confirm_window.destroy()

                status_label.configure(text="Turma removida com sucesso!")
                status_label.after(4500,lambda:status_label.configure(text=""))
            else:
                confirm_window.destroy()
                status_label.configure(text="Não foi possível remover a turma... Por favor, tente novamente!")
                status_label.after(4500,lambda:status_label.configure(text=""))

        def cancel():
            confirm_window.destroy()

        x = manage.winfo_x
        y = manage.winfo_y

        confirm_window = tk.CTkToplevel(manage)
        confirm_window.geometry("350x150")
        confirm_window.title("CONFIRMAR")

        confirm_label = tk.CTkLabel(confirm_window,text="Deseja continuar?",font=("Arial",20,"bold"))
        confirm_label.pack(side="top",expand=True,padx=10,pady=5)

        b_yes = tk.CTkButton(confirm_window,text="Sim",font=("Arial",20,"bold"),width=100,height=30,fg_color="red",command=confirm)
        b_yes.pack(side="left",expand=True,padx=10,pady=10)

        b_no = tk.CTkButton(confirm_window,text="Não",font=("Arial",20,"bold"),width=100,height=30,fg_color="gray",command=cancel)
        b_no.pack(side="right",expand=True,padx=10,pady=10)

        confirm_window.transient(manage)
        confirm_window.focus()
        confirm_window.grab_set()
        confirm_window.wait_window()

    def update_list_fb():
        turmas = load_data()
        for turma in turmas:
            if not turma["codigo"] in codigos:
                codigos.append(turma["codigo"])
            else:
                continue
        select_box.configure(values=codigos)
    
    update_button = tk.CTkButton(manage,text="Atualizar",font=("Arial",20,"bold"),width=100,height=50,fg_color="gray",command=update_list_fb)
    update_button.grid(column=1,row=0,sticky="wn")

    delete_button = tk.CTkButton(manage,text="Remover",font=("Arial",20,"bold"),width=100,height=50,fg_color="red",command=confirm_delete_class_window)
    delete_button.grid(column=2,row=0,sticky="nw")

    tip = tk.CTkLabel(manage,text="Não está vendo o que queria? Tente atualizar a lista!",font=("Consolas",17))
    tip.grid(column=0,row=11,sticky="s")
        

    manage.mainloop()
#-------------------------------------------------------------------------Manage

#-------------------------------------------------------------------------Gerenciar Notas/Atividades
def o_grades_window():
    x = root.winfo_x()
    y = root.winfo_y()
    grades_window = tk.CTk()
    grades_window.geometry(f"+{x+50}+{y+50}")
    grades_window.geometry("1100x900")
    grades_window.title("Gerenciar Notas e Atividades")
    
    
    grades_window.columnconfigure(0, weight=1)
    grades_window.rowconfigure(1, weight=1)
    
    
    top_frame = tk.CTkFrame(grades_window, fg_color="transparent")
    top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
    
    turmas = load_data()
    codigos = [turma["codigo"] for turma in turmas]
    
    
    instruction_label = tk.CTkLabel(top_frame, text="Selecione a turma:", 
                                   font=("Arial", 16, "bold"))
    instruction_label.pack(side="left", padx=(0, 10))
    
    
    select_turma = tk.CTkComboBox(top_frame, values=codigos, width=300, height=40, 
                                 font=("Arial", 18, "bold"), command=lambda x: show_grades_interface())
    select_turma.pack(side="left", padx=10)
    select_turma.set("Escolha...")
    
    
    content_frame = tk.CTkFrame(grades_window)
    content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    content_frame.columnconfigure(0, weight=1)
    content_frame.rowconfigure(0, weight=0)
    content_frame.rowconfigure(1, weight=1)
    
    label_turma = tk.CTkLabel(content_frame, text="", font=("Arial", 24, "bold"))
    label_turma = tk.CTkLabel(content_frame, text="", font=("Arial", 24, "bold"))
    
    def show_grades_interface():
        turma_codigo = select_turma.get()
        if turma_codigo == "Escolha...":
            return
        
        label_turma.configure(text=f"TURMA: {turma_codigo}")
        label_turma.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 20))
        
    
        for widget in content_frame.grid_slaves():
            if widget != label_turma:
                widget.grid_forget()
        
    
        notas_frame = tk.CTkFrame(content_frame)
        notas_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        title_notas = tk.CTkLabel(notas_frame, text="GERENCIAR NOTAS DOS ALUNOS", 
                                 font=("Arial", 20, "bold"))
        title_notas.pack(pady=15)
        
        btn_add_grades = tk.CTkButton(notas_frame, text="Adicionar/Visualizar Notas", 
                                     font=("Arial", 18, "bold"), width=350, height=50,
                                     command=lambda: open_add_grades_window(turma_codigo))
        btn_add_grades.pack(pady=10, padx=20)
        
    
        separator = tk.CTkFrame(content_frame, height=2, fg_color="gray")
        separator.grid(row=2, column=0, sticky="ew", padx=40, pady=30)
        
    
        atividades_frame = tk.CTkFrame(content_frame)
        atividades_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        title_ativ = tk.CTkLabel(atividades_frame, text="LANCAR NOTAS DAS ATIVIDADES", 
                                font=("Arial", 20, "bold"))
        title_ativ.pack(pady=15)
        
        buttons_frame = tk.CTkFrame(atividades_frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        btn_lancar_atividades = tk.CTkButton(buttons_frame, text="Lancar Nota de Atividade", 
                                            font=("Arial", 18, "bold"), width=300, height=50,
                                            fg_color="orange",
                                            command=lambda: open_lancar_atividade_window(turma_codigo))
        btn_lancar_atividades.grid(row=0, column=0, padx=10, pady=10)
        
        btn_view_atividades = tk.CTkButton(buttons_frame, text="Visualizar Atividades", 
                                          font=("Arial", 18, "bold"), width=300, height=50,
                                          command=lambda: view_atividades_window(turma_codigo))
        btn_view_atividades.grid(row=0, column=1, padx=10, pady=10)
    
    def open_add_grades_window(turma_codigo):
    
        grades_win = tk.CTkToplevel(grades_window)
        grades_win.geometry("900x600")
        grades_win.title("Gerenciar Notas dos Alunos")
        
        title_label = tk.CTkLabel(grades_win, text=f"Notas - {turma_codigo}", 
                                 font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        scroll_frame = tk.CTkScrollableFrame(grades_win)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        def atualizar_lista_alunos():
            """Atualiza a lista de alunos com suas notas"""
    
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            
            dados = load_data()
            turma_selecionada = None
            for turma in dados:
                if turma["codigo"] == turma_codigo:
                    turma_selecionada = turma
                    break
            
            if not turma_selecionada or not turma_selecionada["alunos"]:
                no_students = tk.CTkLabel(scroll_frame, text="Nenhum aluno cadastrado nesta turma.",
                                         font=("Arial", 16))
                no_students.pack(pady=20)
                return
            
            for matricula, dados_aluno in turma_selecionada["alunos"].items():
                def criar_comando_aluno(mat, nome):
                    def cmd():
                        open_student_grades_window(turma_codigo, mat, nome, atualizar_lista_alunos)
                    return cmd
                
                aluno_frame = tk.CTkFrame(scroll_frame)
                aluno_frame.pack(fill="x", padx=5, pady=5)
                
                nome = dados_aluno.get("nome", "Sem nome")
                
    
                np1 = dados_aluno.get("np1", "-")
                np2 = dados_aluno.get("np2", "-")
                pim = dados_aluno.get("pim", "-")
                media_base = dados_aluno.get("media", "-")
                status = dados_aluno.get("status", "-")
                
              
                media = media_base
                if isinstance(media_base, (int, float)):
                    soma_atividades = dados_aluno.get("soma_atividades", 0)
                    if soma_atividades > 0:
                        
                        if lib is not None and isinstance(np1, (int, float)) and isinstance(np2, (int, float)) and isinstance(pim, (int, float)):
                            media = lib.media_com_atividades(
                                ctypes.c_float(np1),
                                ctypes.c_float(np2),
                                ctypes.c_float(pim),
                                ctypes.c_float(soma_atividades)
                            )
                        else:
                            
                            media = min(media_base + soma_atividades, 10.0)
                
    
                np1_str = f"{np1:.2f}" if isinstance(np1, (int, float)) else np1
                np2_str = f"{np2:.2f}" if isinstance(np2, (int, float)) else np2
                pim_str = f"{pim:.2f}" if isinstance(pim, (int, float)) else pim
                media_str = f"{media:.2f}" if isinstance(media, (int, float)) else media
                
                info_text = f"{matricula} - {nome}\nNP1: {np1_str} | NP2: {np2_str} | PIM: {pim_str} | Media: {media_str} | Status: {status}"
                
                info_label = tk.CTkLabel(aluno_frame, 
                                        text=info_text,
                                        font=("Arial", 16),
                                        justify="left")
                info_label.pack(side="left", padx=10, pady=5)
                
                btn_manage = tk.CTkButton(aluno_frame, text="GERENCIAR", width=120,
                                         command=criar_comando_aluno(matricula, nome))
                btn_manage.pack(side="right", padx=10, pady=5)
        
        atualizar_lista_alunos()
        grades_win.transient(grades_window)
    
    def open_student_grades_window(turma_codigo, matricula, nome, callback_atualizar=None):
    
        student_win = tk.CTkToplevel(grades_window)
        student_win.geometry("950x900")
        student_win.title(f"Notas - {nome}")
        
    
        student_win.update_idletasks()
        parent_x = grades_window.winfo_x()
        parent_y = grades_window.winfo_y()
        parent_width = grades_window.winfo_width()
        parent_height = grades_window.winfo_height()
        
        win_width = 950
        win_height = 900
        
        x = parent_x + (parent_width - win_width) // 2
        y = parent_y + (parent_height - win_height) // 2
        
        student_win.geometry(f"{win_width}x{win_height}+{x}+{y}")
        
        title_label = tk.CTkLabel(student_win, 
                                 text=f"Gerenciar Notas\n{nome} ({matricula})",
                                 font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
    
        input_frame = tk.CTkFrame(student_win)
        input_frame.pack(pady=10, padx=10, fill="x")
        
    
        tk.CTkLabel(input_frame, text="NP1:", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        np1_entry = tk.CTkEntry(input_frame, width=120, font=("Arial", 14))
        np1_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.CTkLabel(input_frame, text="NP2:", font=("Arial", 16, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        np2_entry = tk.CTkEntry(input_frame, width=120, font=("Arial", 14))
        np2_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.CTkLabel(input_frame, text="PIM:", font=("Arial", 16, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        pim_entry = tk.CTkEntry(input_frame, width=120, font=("Arial", 14))
        pim_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.CTkLabel(input_frame, text="Exame:", font=("Arial", 16, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        exame_entry = tk.CTkEntry(input_frame, width=120, font=("Arial", 14))
        exame_entry.grid(row=1, column=3, padx=5, pady=5)
        
        status_label = tk.CTkLabel(student_win, text="", font=("Arial", 16, "bold"), text_color="green")
        status_label.pack(pady=5)
        
        
        ativ_frame = tk.CTkFrame(student_win)
        ativ_frame.pack(pady=10, padx=10, fill="x")
        
        ativ_title = tk.CTkLabel(ativ_frame, text="Atividades Lancadas:", 
                                font=("Arial", 16, "bold"))
        ativ_title.pack(pady=5)
        
        ativ_scroll = tk.CTkScrollableFrame(ativ_frame, height=100)
        ativ_scroll.pack(fill="x", padx=5, pady=5)
        
        def atualizar_lista_atividades():
            for widget in ativ_scroll.winfo_children():
                widget.destroy()
            
            dados = load_data()
            for turma in dados:
                if turma["codigo"] == turma_codigo:
                    if matricula in turma["alunos"]:
                        notas_atividades = turma["alunos"][matricula].get("notas", [])
                        
                        if notas_atividades:
                            for idx, nota in enumerate(notas_atividades):
                                def criar_comando_remover_ativ(index):
                                    def cmd():
                                        remover_atividade(index)
                                    return cmd
                                
                                nota_ativ_frame = tk.CTkFrame(ativ_scroll)
                                nota_ativ_frame.pack(fill="x", pady=2, padx=5)
                                
                                nota_label = tk.CTkLabel(nota_ativ_frame, 
                                                        text=f"Atividade {idx + 1}: {nota:.2f} pontos",
                                                        font=("Arial", 13))
                                nota_label.pack(side="left", padx=10)
                                
                                btn_remover = tk.CTkButton(nota_ativ_frame, text="Remover", 
                                                          width=80, height=25,
                                                          fg_color="red",
                                                          command=criar_comando_remover_ativ(idx))
                                btn_remover.pack(side="right", padx=5)
                        else:
                            empty_label = tk.CTkLabel(ativ_scroll, 
                                                     text="Nenhuma atividade lancada.",
                                                     font=("Arial", 12))
                            empty_label.pack(pady=10)
                        break
        
        def remover_atividade(index):
    
            dados = load_data()
            for turma in dados:
                if turma["codigo"] == turma_codigo:
                    if matricula in turma["alunos"]:
                        if index < len(turma["alunos"][matricula].get("notas", [])):
                            nota_removida = turma["alunos"][matricula]["notas"].pop(index)
                            save_data(dados)
                            atualizar_lista_atividades()
                            status_label.configure(text=f"Atividade {nota_removida:.2f} removida! Recalcule a media.", text_color="orange")
                            status_label.after(4000, lambda: status_label.configure(text=""))
                            
    
                            info_label.configure(text="Clique em 'Salvar e Calcular Media' para atualizar.")
                        break
        
    
        result_frame = tk.CTkFrame(student_win)
        result_frame.pack(pady=15, padx=10, fill="both", expand=True)
        
        result_title = tk.CTkLabel(result_frame, text="Resultado:", 
                                   font=("Arial", 16, "bold"))
        result_title.pack(pady=5)
        
        info_label = tk.CTkLabel(result_frame, text="", font=("Arial", 15), justify="left")
        info_label.pack(pady=10, padx=10)
        
        def carregar_notas():
    
            dados = load_data()
            for turma in dados:
                if turma["codigo"] == turma_codigo:
                    if matricula in turma["alunos"]:
                        aluno = turma["alunos"][matricula]
                        np1_entry.delete(0, tk.END)
                        np2_entry.delete(0, tk.END)
                        pim_entry.delete(0, tk.END)
                        exame_entry.delete(0, tk.END)
                        
                        if "np1" in aluno:
                            np1_entry.insert(0, str(aluno["np1"]))
                        if "np2" in aluno:
                            np2_entry.insert(0, str(aluno["np2"]))
                        if "pim" in aluno:
                            pim_entry.insert(0, str(aluno["pim"]))
                        if "exame" in aluno:
                            exame_entry.insert(0, str(aluno["exame"]))
                        
                        
                        notas_atividades = aluno.get("notas", [])
                        soma_calculada = sum(notas_atividades)
                        
                        
                        if aluno.get("soma_atividades", 0) != soma_calculada:
                            aluno["soma_atividades"] = soma_calculada
                            save_data(dados)
    
                        atualizar_lista_atividades()
                        
    
                        if "media" in aluno:
                            atualizar_resultado()
                        break
        
        def calcular_e_salvar():
    
            if lib is None:
                status_label.configure(text="Erro: Biblioteca C nao carregada!", text_color="red")
                status_label.after(3000, lambda: status_label.configure(text=""))
                return
            
            try:
    
                np1_val = float(np1_entry.get()) if np1_entry.get().strip() else None
                np2_val = float(np2_entry.get()) if np2_entry.get().strip() else None
                pim_val = float(pim_entry.get()) if pim_entry.get().strip() else None
                exame_val = float(exame_entry.get()) if exame_entry.get().strip() else None
                
    
                if np1_val is None or np2_val is None or pim_val is None:
                    status_label.configure(text="Preencha NP1, NP2 e PIM!", text_color="orange")
                    status_label.after(3000, lambda: status_label.configure(text=""))
                    return
                
    
                dados = load_data()
                soma_atividades = 0.0
                for turma in dados:
                    if turma["codigo"] == turma_codigo:
                        if matricula in turma["alunos"]:
                            notas_atividades = turma["alunos"][matricula].get("notas", [])
                            soma_atividades = sum(notas_atividades)
                            break
                
    
                if soma_atividades > 0:
                    media = lib.media_com_atividades(ctypes.c_float(np1_val), 
                                                    ctypes.c_float(np2_val), 
                                                    ctypes.c_float(pim_val),
                                                    ctypes.c_float(soma_atividades))
                else:
                    media = lib.media(ctypes.c_float(np1_val), 
                                     ctypes.c_float(np2_val), 
                                     ctypes.c_float(pim_val))
                
    
                dados = load_data()
                for turma in dados:
                    if turma["codigo"] == turma_codigo:
                        if matricula in turma["alunos"]:
                            turma["alunos"][matricula]["np1"] = np1_val
                            turma["alunos"][matricula]["np2"] = np2_val
                            turma["alunos"][matricula]["pim"] = pim_val
                            turma["alunos"][matricula]["media"] = float(media)
                            turma["alunos"][matricula]["soma_atividades"] = soma_atividades
                            
    
                            if media >= 6.0:
                                turma["alunos"][matricula]["status"] = "APROVADO"
                            else:
                                turma["alunos"][matricula]["status"] = "REPROVADO"
                                
    
                                if exame_val is not None:
                                    media_final = lib.media_exame(ctypes.c_float(media), 
                                                                 ctypes.c_float(exame_val))
                                    turma["alunos"][matricula]["exame"] = exame_val
                                    turma["alunos"][matricula]["media_final"] = float(media_final)
                                    
                                    if media_final >= 5.0:
                                        turma["alunos"][matricula]["status"] = "APROVADO (EXAME)"
                                    else:
                                        turma["alunos"][matricula]["status"] = "REPROVADO (EXAME)"
                            
                            save_data(dados)
                            status_label.configure(text="Notas salvas e media calculada!", text_color="green")
                            status_label.after(3000, lambda: status_label.configure(text=""))
                            
    
                            atualizar_resultado()
                            
    
                            if callback_atualizar:
                                callback_atualizar()
                            break
                            
            except ValueError:
                status_label.configure(text="Digite valores numericos validos!", text_color="red")
                status_label.after(3000, lambda: status_label.configure(text=""))
        
        def atualizar_resultado():
    
            dados = load_data()
            for turma in dados:
                if turma["codigo"] == turma_codigo:
                    if matricula in turma["alunos"]:
                        aluno = turma["alunos"][matricula]
                        
                        if "media" in aluno:
                            resultado = "CALCULO REALIZADO EM C:\n\n"
                            resultado += f"NP1: {aluno.get('np1', 0):.2f}\n"
                            resultado += f"NP2: {aluno.get('np2', 0):.2f}\n"
                            resultado += f"PIM: {aluno.get('pim', 0):.2f}\n"
                            
                        
                            notas_atividades = aluno.get('notas', [])
                            soma_ativ = aluno.get('soma_atividades', 0)
                            if notas_atividades:
                                resultado += f"\nAtividades: {notas_atividades}\n"
                                resultado += f"Soma Atividades: +{soma_ativ:.2f}\n"
                            
                            resultado += f"\nMedia Final: {aluno['media']:.2f}\n"
                            
    
                            if aluno['media'] >= 10.0:
                                resultado += "(Limitado ao maximo de 10.0)\n"
                            
                            resultado += f"Status: {aluno.get('status', 'N/A')}\n"
                            
                            if "exame" in aluno and "media_final" in aluno:
                                resultado += f"\nExame: {aluno['exame']:.2f}\n"
                                resultado += f"Media com Exame: {aluno['media_final']:.2f}\n"
                                if aluno['media_final'] >= 10.0:
                                    resultado += "(Limitado ao maximo de 10.0)\n"
                            
                            info_label.configure(text=resultado)
                        break
        
    
        btn_salvar = tk.CTkButton(student_win, text="Salvar e Calcular Media", 
                                 width=250, height=40,
                                 font=("Arial", 16, "bold"),
                                 fg_color="green",
                                 command=calcular_e_salvar)
        btn_salvar.pack(pady=15)
        
    
        carregar_notas()
        
        student_win.transient(grades_window)
    
    def open_lancar_atividade_window(turma_codigo):
    
        ativ_win = tk.CTkToplevel(grades_window)
        
    
        ativ_win.update_idletasks()
        parent_x = grades_window.winfo_x()
        parent_y = grades_window.winfo_y()
        parent_width = grades_window.winfo_width()
        parent_height = grades_window.winfo_height()
        
        win_width = 900
        win_height = 750
        
        x = parent_x + (parent_width - win_width) // 2
        y = parent_y + (parent_height - win_height) // 2
        
        ativ_win.geometry(f"{win_width}x{win_height}+{x}+{y}")
        ativ_win.title("Lançar Nota de Atividade")
        
    
        header_frame = tk.CTkFrame(ativ_win, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        title_label = tk.CTkLabel(header_frame, 
                                 text=f"Lançar Nota de Atividade",
                                 font=("Arial", 24, "bold"))
        title_label.pack()
        
        subtitle_label = tk.CTkLabel(header_frame, 
                                    text=f"Turma: {turma_codigo}",
                                    font=("Arial", 16))
        subtitle_label.pack(pady=5)
        
        dados = load_data()
        turma_selecionada = None
        for turma in dados:
            if turma["codigo"] == turma_codigo:
                turma_selecionada = turma
                break
        
        if not turma_selecionada:
            return
        
    
        if not turma_selecionada["atividades"]:
            no_ativ = tk.CTkLabel(ativ_win, 
                                 text="Nenhuma atividade cadastrada nesta turma.",
                                 font=("Arial", 16))
            no_ativ.pack(pady=20)
            return
        
        if not turma_selecionada["alunos"]:
            no_aluno = tk.CTkLabel(ativ_win, 
                                  text="Nenhum aluno cadastrado nesta turma.",
                                  font=("Arial", 16))
            no_aluno.pack(pady=20)
            return
        
    
        select_frame = tk.CTkFrame(ativ_win)
        select_frame.pack(pady=15, padx=20, fill="x")
        
    
        select_inner = tk.CTkFrame(select_frame, fg_color="transparent")
        select_inner.pack(pady=15, padx=15)
        
        label_ativ = tk.CTkLabel(select_inner, text="Selecione a Atividade:", 
                                font=("Arial", 16, "bold"))
        label_ativ.pack(side="left", padx=(0, 15))
        
        atividades_nomes = list(turma_selecionada["atividades"].keys())
        combo_ativ = tk.CTkComboBox(select_inner, values=atividades_nomes, 
                                    width=350, height=35, font=("Arial", 15))
        combo_ativ.pack(side="left")
        combo_ativ.set("Escolha...")
        
    
        info_ativ_label = tk.CTkLabel(select_frame, text="", font=("Arial", 14), 
                                      text_color="gray")
        info_ativ_label.pack(pady=(0, 10))
        
        def atualizar_info_atividade(choice):
            if choice != "Escolha...":
                ativ_data = turma_selecionada["atividades"][choice]
                info_text = f"Valor: {ativ_data.get('valor', 0)} pontos | Data: {ativ_data.get('data_entrega', 'Sem data')}"
                info_ativ_label.configure(text=info_text)
                carregar_alunos()
        
        combo_ativ.configure(command=atualizar_info_atividade)
        
    
        lista_title = tk.CTkLabel(ativ_win, text="Lista de Alunos:", 
                                 font=("Arial", 16, "bold"))
        lista_title.pack(pady=(10, 5))
        
    
        alunos_scroll = tk.CTkScrollableFrame(ativ_win, height=350)
        alunos_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        status_ativ_label = tk.CTkLabel(ativ_win, text="", font=("Arial", 15, "bold"), 
                                       text_color="green")
        status_ativ_label.pack(pady=10)
        
        def carregar_alunos():
            for widget in alunos_scroll.winfo_children():
                widget.destroy()
            
            atividade_nome = combo_ativ.get()
            if atividade_nome == "Escolha...":
                empty_label = tk.CTkLabel(alunos_scroll, 
                                         text="Selecione uma atividade acima",
                                         font=("Arial", 14), text_color="gray")
                empty_label.pack(pady=30)
                return
            
            for matricula, dados_aluno in turma_selecionada["alunos"].items():
                aluno_frame = tk.CTkFrame(alunos_scroll, fg_color=("gray90", "gray20"))
                aluno_frame.pack(fill="x", padx=5, pady=5)
                
                nome = dados_aluno.get("nome", "Sem nome")
                
                nome_label = tk.CTkLabel(aluno_frame, 
                                        text=f"{matricula} - {nome}",
                                        font=("Arial", 15), width=400, anchor="w")
                nome_label.pack(side="left", padx=15, pady=10)
                
                nota_entry = tk.CTkEntry(aluno_frame, placeholder_text="Nota...", 
                                        width=100, height=35, font=("Arial", 15))
                nota_entry.pack(side="left", padx=10)
                
                def criar_comando_lancar(mat, entry):
                    def cmd():
                        lancar_nota_atividade(mat, entry, atividade_nome)
                    return cmd
                
                btn_lancar = tk.CTkButton(aluno_frame, text="Lancar", width=100, height=35,
                                         font=("Arial", 14, "bold"),
                                         command=criar_comando_lancar(matricula, nota_entry))
                btn_lancar.pack(side="left", padx=10)
        
        def lancar_nota_atividade(matricula, entry, atividade_nome):
            try:
                nota = float(entry.get())
                dados = load_data()
                for turma in dados:
                    if turma["codigo"] == turma_codigo:
                        if matricula in turma["alunos"]:
                            
                            turma["alunos"][matricula]["notas"].append(nota)
                            save_data(dados)
                            entry.delete(0, tk.END)
                            status_ativ_label.configure(
                                text=f"Nota {nota} lançada para {turma['alunos'][matricula]['nome']}!"
                            )
                            status_ativ_label.after(3000, 
                                lambda: status_ativ_label.configure(text=""))
                            break
            except ValueError:
                status_ativ_label.configure(text="Digite um número válido!")
                status_ativ_label.after(2000, lambda: status_ativ_label.configure(text=""))
        
        ativ_win.transient(grades_window)
    
    def view_atividades_window(turma_codigo):
    
        view_win = tk.CTkToplevel(grades_window)
        view_win.geometry("600x500")
        view_win.title("Atividades Cadastradas")
        
        title_label = tk.CTkLabel(view_win, 
                                 text=f"Atividades - {turma_codigo}",
                                 font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        dados = load_data()
        turma_selecionada = None
        for turma in dados:
            if turma["codigo"] == turma_codigo:
                turma_selecionada = turma
                break
        
        if not turma_selecionada or not turma_selecionada["atividades"]:
            no_ativ = tk.CTkLabel(view_win, 
                                 text="Nenhuma atividade cadastrada nesta turma.",
                                 font=("Arial", 16))
            no_ativ.pack(pady=20)
            return
        
        scroll_frame = tk.CTkScrollableFrame(view_win)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for nome_ativ, dados_ativ in turma_selecionada["atividades"].items():
            ativ_frame = tk.CTkFrame(scroll_frame)
            ativ_frame.pack(fill="x", padx=5, pady=10)
            
            nome_label = tk.CTkLabel(ativ_frame, text=f"📋 {nome_ativ}",
                                    font=("Arial", 16, "bold"))
            nome_label.pack(anchor="w", padx=10, pady=5)
            
            desc_label = tk.CTkLabel(ativ_frame, 
                                    text=f"Descrição: {dados_ativ.get('descricao', 'Sem descrição')}",
                                    font=("Arial", 13))
            desc_label.pack(anchor="w", padx=10, pady=2)
            
            data_label = tk.CTkLabel(ativ_frame, 
                                    text=f"Data: {dados_ativ.get('data_entrega', 'Sem data')}",
                                    font=("Arial", 13))
            data_label.pack(anchor="w", padx=10, pady=2)
            
            valor_label = tk.CTkLabel(ativ_frame, 
                                     text=f"Valor: {dados_ativ.get('valor', 0)} pontos",
                                     font=("Arial", 13, "bold"))
            valor_label.pack(anchor="w", padx=10, pady=2)
        
        view_win.transient(grades_window)
    
    grades_window.mainloop()
#-------------------------------------------------------------------------Gerenciar Notas/Atividades

root = tk.CTk()
root.title("GERENCIADOR")
root.geometry("1000x700")

root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.columnconfigure(2,weight=1)
root.columnconfigure(3,weight=1)
root.columnconfigure(4,weight=1)
root.columnconfigure(5,weight=1)
root.columnconfigure(6,weight=1)
root.columnconfigure(7,weight=1)
root.columnconfigure(8,weight=1)

root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)
root.rowconfigure(3,weight=1)
root.rowconfigure(4,weight=1)
root.rowconfigure(5,weight=1)
root.rowconfigure(6,weight=1)
root.rowconfigure(7,weight=1)
root.rowconfigure(8,weight=1)


sidebar = tk.CTkFrame(root,bg_color="white",width=300,height=3000,corner_radius=0,)
sidebar.grid(row=0,column=0,sticky="wns",rowspan=9)
sidebar.grid_propagate(False)
sidebar.columnconfigure(0,weight=1)
sidebar.columnconfigure(1,weight=1)
sidebar.columnconfigure(2,weight=1)
sidebar.rowconfigure(0,weight=1)
sidebar.rowconfigure(1,weight=1)
sidebar.rowconfigure(2,weight=1)
sidebar.rowconfigure(3,weight=1)
sidebar.rowconfigure(4,weight=1)
sidebar.rowconfigure(5,weight=1)
sidebar.rowconfigure(6,weight=1)
sidebar.rowconfigure(7,weight=1)
sidebar.rowconfigure(8,weight=1)



welcome = tk.CTkLabel(sidebar,text="GERENCIADOR",font=("Arial",35,"bold"))
welcome.grid(column=1,row=0,sticky="n",pady=20)

botao1 = tk.CTkButton(sidebar,text="Adicionar nova turma",font=("Arial",20),
                     width=250,height=150,command=o_add_window)
botao1.grid(row=1,column=1,sticky="ew",pady=10,padx=20)

botao2 = tk.CTkButton(sidebar,text="Configurar Turmas/Alunos/Atividades",
                     font=("Arial",15),width=250,height=150,command=o_manage_window)
botao2.grid(row=2,column=1,sticky="ew",pady=10,padx=20)

botao3 = tk.CTkButton(sidebar,text="Gerenciar Notas/Atividades",font=("Arial",20),
                     width=250,height=150,command=o_grades_window)
botao3.grid(row=3,column=1,sticky="ew",pady=10,padx=20)


if lib is not None:
    status_text = "Biblioteca C: CARREGADA"
    status_color = "green"
else:
    status_text = "Biblioteca C: NÃO CARREGADA"
    status_color = "red"

lib_status_frame = tk.CTkFrame(sidebar, fg_color="transparent")
lib_status_frame.grid(row=4, column=1, sticky="ew", pady=20, padx=20)

lib_status = tk.CTkLabel(lib_status_frame, text=status_text, 
                        font=("Arial", 13, "bold"), 
                        text_color=status_color)
lib_status.pack()

frame_turmas = tk.CTkScrollableFrame(root,label_text="Turmas cadastradas",
                                    label_font=("Arial",18,"bold"))
frame_turmas.grid(column=1,row=0,columnspan=8,rowspan=9,sticky="nsew",padx=10,pady=10)

def update_list(frame):
    global turmas
    turmas = load_data()

    for widget in frame.winfo_children():
        widget.destroy()

    for turma in turmas:
        item = tk.CTkLabel(frame, text=turma["codigo"], font=("Arial", 20))
        item.pack(fill="x", padx=10, pady=5)


update_list(frame_turmas)
root.mainloop()