import os
import sys
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from fpdf import FPDF
import csv
from PIL import Image, ImageTk

class SistemaMotoristas:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Motoristas")
        self.root.geometry("1000x800")
        
        # Carregar a logo da empresa
        self.carregar_logo()
        
        # Dados
        self.motoristas = []
        self.rotas_por_motorista = {}  # Dicionário para armazenar rotas por motorista
        self.carregar_dados()
        
        # Criar interface
        self.criar_interface()
    
    def carregar_logo(self):
        try:
            self.logo_image = Image.open("logo.png")
            self.logo_image = self.logo_image.resize((180, 60), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            self.logo_photo = None
            print("Arquivo de logo não encontrado. Usando texto alternativo.")
    
    def carregar_dados(self):
        try:
            with open('motoristas.csv', 'r', newline='', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                self.motoristas = list(leitor)
                
                # Carregar rotas por motorista
                for motorista in self.motoristas:
                    nome = motorista['nome']
                    if nome not in self.rotas_por_motorista:
                        self.rotas_por_motorista[nome] = []
                    self.rotas_por_motorista[nome].append({
                        'data': motorista['data'],
                        'rota': motorista['rota'],
                        'horario': motorista['horario'],
                        'valor': motorista['valor'],
                        'pagamento': motorista['pagamento']
                    })
        except FileNotFoundError:
            self.motoristas = []
            self.rotas_por_motorista = {}
    
    def salvar_dados(self):
        campos = ['data', 'nome', 'idade', 'pix', 'rota', 'horario', 'valor', 'pagamento']
        with open('motoristas.csv', 'w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            
            for nome, rotas in self.rotas_por_motorista.items():
                for rota in rotas:
                    motorista = {
                        'data': rota['data'],
                        'nome': nome,
                        'idade': next((m['idade'] for m in self.motoristas if m['nome'] == nome), ''),
                        'pix': next((m['pix'] for m in self.motoristas if m['nome'] == nome), ''),
                        'rota': rota['rota'],
                        'horario': rota['horario'],
                        'valor': rota['valor'],
                        'pagamento': rota['pagamento']
                    }
                    escritor.writerow(motorista)
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Frame do cabeçalho com logo
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(W, E), pady=(0, 10))
        
        # Adicionar a logo ou texto alternativo
        if hasattr(self, 'logo_photo') and self.logo_photo:
            logo_label = ttk.Label(header_frame, image=self.logo_photo)
            logo_label.grid(row=0, column=0, sticky=W, padx=(0, 20))
        else:
            logo_label = ttk.Label(header_frame, text="TRANSPORTADORA", font=('Arial', 14, 'bold'))
            logo_label.grid(row=0, column=0, sticky=W, padx=(0, 20))
        
        # Título do sistema
        title_label = ttk.Label(header_frame, text="Controle de Motoristas e Rotas", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=1, sticky=W)
        
        # Frame de cadastro de motorista
        motorista_frame = ttk.LabelFrame(main_frame, text="Cadastrar Motorista", padding="10")
        motorista_frame.grid(row=1, column=0, sticky=(W, E, N, S), padx=5, pady=5)
        
        # Nome Completo
        ttk.Label(motorista_frame, text="Nome Completo:").grid(row=0, column=0, sticky=W)
        self.nome_entry = ttk.Entry(motorista_frame)
        self.nome_entry.grid(row=0, column=1, sticky=(W, E))
        
        # Idade
        ttk.Label(motorista_frame, text="Idade:").grid(row=1, column=0, sticky=W)
        self.idade_spin = ttk.Spinbox(motorista_frame, from_=18, to=80, width=3)
        self.idade_spin.grid(row=1, column=1, sticky=W)
        
        # Chave PIX
        ttk.Label(motorista_frame, text="Chave PIX:").grid(row=2, column=0, sticky=W)
        self.pix_entry = ttk.Entry(motorista_frame)
        self.pix_entry.grid(row=2, column=1, sticky=(W, E))
        
        ttk.Button(motorista_frame, text="Cadastrar Motorista", command=self.cadastrar_motorista).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame de cadastro de rota
        rota_frame = ttk.LabelFrame(main_frame, text="Cadastrar Rota para Motorista", padding="10")
        rota_frame.grid(row=2, column=0, sticky=(W, E, N, S), padx=5, pady=5)
        
        # Motorista
        ttk.Label(rota_frame, text="Motorista:").grid(row=0, column=0, sticky=W)
        self.motorista_combobox = ttk.Combobox(rota_frame, state="readonly")
        self.motorista_combobox.grid(row=0, column=1, sticky=(W, E))
        
        # Data
        ttk.Label(rota_frame, text="Data:").grid(row=1, column=0, sticky=W)
        self.data_var = StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(rota_frame, textvariable=self.data_var, state='readonly').grid(row=1, column=1, sticky=W)
        
        # Rota
        ttk.Label(rota_frame, text="Rota:").grid(row=2, column=0, sticky=W)
        self.rota_entry = ttk.Entry(rota_frame)
        self.rota_entry.grid(row=2, column=1, sticky=(W, E))
        
        # Horário
        ttk.Label(rota_frame, text="Horário (HH:MM):").grid(row=3, column=0, sticky=W)
        frame_horario = ttk.Frame(rota_frame)
        frame_horario.grid(row=3, column=1, sticky=W)
        
        self.hora_spin = ttk.Spinbox(frame_horario, from_=0, to=23, width=2, format="%02.0f")
        self.hora_spin.grid(row=0, column=0)
        ttk.Label(frame_horario, text=":").grid(row=0, column=1)
        self.minuto_spin = ttk.Spinbox(frame_horario, from_=0, to=59, width=2, format="%02.0f")
        self.minuto_spin.grid(row=0, column=2)
        
        # Definir horário atual
        agora = datetime.now()
        self.hora_spin.set(agora.strftime("%H"))
        self.minuto_spin.set(agora.strftime("%M"))
        
        # Valor
        ttk.Label(rota_frame, text="Valor (R$):").grid(row=4, column=0, sticky=W)
        self.valor_entry = ttk.Entry(rota_frame)
        self.valor_entry.grid(row=4, column=1, sticky=(W, E))
        
        # Data de Pagamento
        ttk.Label(rota_frame, text="Pagamento:").grid(row=5, column=0, sticky=W)
        self.pagamento_var = StringVar()
        ttk.Radiobutton(rota_frame, text="Dia 15", variable=self.pagamento_var, value="15").grid(row=5, column=1, sticky=W)
        ttk.Radiobutton(rota_frame, text="Dia 31", variable=self.pagamento_var, value="31").grid(row=5, column=2, sticky=W)
        
        ttk.Button(rota_frame, text="Cadastrar Rota", command=self.cadastrar_rota).grid(row=6, column=0, columnspan=3, pady=10)
        
        # Frame de visualização
        visualizacao_frame = ttk.LabelFrame(main_frame, text="Motoristas e Rotas Cadastradas", padding="10")
        visualizacao_frame.grid(row=1, column=1, rowspan=2, sticky=(W, E, N, S), padx=5, pady=5)
        
        # Treeview
        colunas = ('nome', 'idade', 'pix', 'data', 'rota', 'horario', 'valor', 'pagamento')
        self.tree = ttk.Treeview(visualizacao_frame, columns=colunas, show='headings')
        
        # Configurar colunas
        col_widths = {
            'nome': 120,
            'idade': 50,
            'pix': 120,
            'data': 80,
            'rota': 100,
            'horario': 70,
            'valor': 80,
            'pagamento': 80
        }
        
        for col in colunas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=col_widths[col])
        
        self.tree.grid(row=0, column=0, sticky=(W, E, N, S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(visualizacao_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(N, S))
        
        # Frame de exportação
        exportacao_frame = ttk.Frame(main_frame)
        exportacao_frame.grid(row=3, column=0, columnspan=2, sticky=(W, E), padx=5, pady=5)
        
        ttk.Button(exportacao_frame, text="Exportar para PDF", command=self.exportar_pdf).grid(row=0, column=0, padx=5)
        ttk.Button(exportacao_frame, text="Exportar para Excel", command=self.exportar_excel).grid(row=0, column=1, padx=5)
        ttk.Button(exportacao_frame, text="Filtrar por Mês", command=self.filtrar_por_mes).grid(row=0, column=2, padx=5)
        ttk.Button(exportacao_frame, text="Remover Selecionado", command=self.remover_selecionado).grid(row=0, column=3, padx=5)
        
        # Atualizar visualização
        self.atualizar_combobox_motoristas()
        self.atualizar_visualizacao()
    
    def cadastrar_motorista(self):
        nome = self.nome_entry.get().strip()
        idade = self.idade_spin.get()
        pix = self.pix_entry.get().strip()
        
        # Validações
        if not nome:
            messagebox.showerror("Erro", "Informe o nome completo do motorista!")
            return
        
        if not idade.isdigit() or int(idade) < 18:
            messagebox.showerror("Erro", "Idade inválida! Deve ser número inteiro maior que 18.")
            return
        
        if not pix:
            messagebox.showerror("Erro", "Informe a chave PIX!")
            return
        
        # Verificar se motorista já existe
        if nome in self.rotas_por_motorista:
            messagebox.showerror("Erro", "Motorista já cadastrado!")
            return
        
        # Adicionar motorista
        self.rotas_por_motorista[nome] = []
        self.motoristas.append({
            'nome': nome,
            'idade': idade,
            'pix': pix
        })
        
        self.salvar_dados()
        self.atualizar_combobox_motoristas()
        self.atualizar_visualizacao()
        
        # Limpar campos
        self.nome_entry.delete(0, END)
        self.idade_spin.delete(0, END)
        self.idade_spin.insert(0, "18")
        self.pix_entry.delete(0, END)
        
        # Feedback
        messagebox.showinfo("Sucesso", "Motorista cadastrado com sucesso!")
    
    def cadastrar_rota(self):
        nome = self.motorista_combobox.get()
        data = self.data_var.get()
        rota = self.rota_entry.get().strip()
        
        # Obter horário
        hora = self.hora_spin.get().zfill(2)
        minuto = self.minuto_spin.get().zfill(2)
        horario = f"{hora}:{minuto}"
        
        valor = self.valor_entry.get()
        pagamento = self.pagamento_var.get()
        
        # Validações
        if not nome:
            messagebox.showerror("Erro", "Selecione um motorista!")
            return
        
        if not rota:
            messagebox.showerror("Erro", "Informe a rota!")
            return
        
        if not self.validar_valor(valor):
            messagebox.showerror("Erro", "Valor inválido! Exemplo: 55,00 ou R$55,00")
            return
        
        if not pagamento:
            messagebox.showerror("Erro", "Selecione a data de pagamento!")
            return
        
        # Formatar valor
        valor_float = float(valor.replace('R$', '').replace(',', '.').strip())
        valor_formatado = f"R${valor_float:.2f}".replace('.', ',')
        
        # Adicionar rota
        self.rotas_por_motorista[nome].append({
            'data': data,
            'rota': rota,
            'horario': horario,
            'valor': valor_formatado,
            'pagamento': pagamento
        })
        
        self.salvar_dados()
        self.atualizar_visualizacao()
        
        # Limpar campos de rota
        self.rota_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        self.pagamento_var.set('')
        
        # Atualizar data
        self.data_var.set(datetime.now().strftime("%d/%m/%Y"))
        
        # Feedback
        messagebox.showinfo("Sucesso", "Rota cadastrada com sucesso!")
    
    def validar_valor(self, valor_str):
        try:
            valor = float(valor_str.replace('R$', '').replace(',', '.').strip())
            return valor >= 0
        except ValueError:
            return False
    
    def atualizar_combobox_motoristas(self):
        motoristas = list(self.rotas_por_motorista.keys())
        self.motorista_combobox['values'] = motoristas
        if motoristas:
            self.motorista_combobox.current(0)
    
    def atualizar_visualizacao(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar motoristas e rotas
        for nome, rotas in self.rotas_por_motorista.items():
            motorista_info = next((m for m in self.motoristas if m['nome'] == nome), None)
            if motorista_info:
                for rota in rotas:
                    self.tree.insert('', END, values=(
                        nome,
                        motorista_info['idade'],
                        motorista_info['pix'],
                        rota['data'],
                        rota['rota'],
                        rota['horario'],
                        rota['valor'],
                        rota['pagamento']
                    ))
    
    def remover_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhum item selecionado!")
            return
        
        item = self.tree.item(selecionado[0])
        valores = item['values']
        nome = valores[0]
        data = valores[3]
        rota = valores[4]
        
        # Encontrar e remover a rota
        for r in self.rotas_por_motorista[nome]:
            if r['data'] == data and r['rota'] == rota:
                self.rotas_por_motorista[nome].remove(r)
                break
        
        # Se não houver mais rotas para o motorista, remover o motorista
        if not self.rotas_por_motorista[nome]:
            del self.rotas_por_motorista[nome]
            self.motoristas = [m for m in self.motoristas if m['nome'] != nome]
        
        self.salvar_dados()
        self.atualizar_combobox_motoristas()
        self.atualizar_visualizacao()
        messagebox.showinfo("Sucesso", "Item removido com sucesso!")
    
    def exportar_pdf(self):
        if not self.motoristas:
            messagebox.showerror("Erro", "Nenhum dado cadastrado para exportar!")
            return
        
        # Configurar PDF em modo paisagem (landscape)
        pdf = FPDF(orientation='L')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Configurar fonte
        pdf.set_font("Arial", 'B', 14)
        
        # Adicionar logo (se existir)
        if hasattr(self, 'logo_image'):
            temp_logo_path = "temp_logo.png"
            self.logo_image.save(temp_logo_path)
            pdf.image(temp_logo_path, x=10, y=8, w=40)
            os.remove(temp_logo_path)
        
        # Título
        pdf.cell(0, 10, "Relatório de Motoristas e Rotas", 0, 1, 'C')
        pdf.ln(10)
        
        # Cabeçalhos
        colunas = ['Motorista', 'Idade', 'PIX', 'Data', 'Rota', 'Horário', 'Valor', 'Pagamento']
        col_widths = [40, 15, 50, 20, 50, 20, 25, 25]
        
        pdf.set_font("Arial", 'B', 10)
        for i, coluna in enumerate(colunas):
            pdf.cell(col_widths[i], 10, coluna, 1, 0, 'C')
        pdf.ln()
        
        # Dados
        pdf.set_font("Arial", '', 8)
        for nome, rotas in self.rotas_por_motorista.items():
            motorista_info = next((m for m in self.motoristas if m['nome'] == nome), None)
            if motorista_info:
                for rota in rotas:
                    # Ajustar textos longos
                    nome_curto = nome[:20] + '...' if len(nome) > 20 else nome
                    pix_curto = motorista_info['pix'][:20] + '...' if len(motorista_info['pix']) > 20 else motorista_info['pix']
                    rota_curta = rota['rota'][:20] + '...' if len(rota['rota']) > 20 else rota['rota']
                    
                    pdf.cell(col_widths[0], 10, nome_curto, 1, 0, 'L')
                    pdf.cell(col_widths[1], 10, motorista_info['idade'], 1, 0, 'C')
                    pdf.cell(col_widths[2], 10, pix_curto, 1, 0, 'L')
                    pdf.cell(col_widths[3], 10, rota['data'], 1, 0, 'C')
                    pdf.cell(col_widths[4], 10, rota_curta, 1, 0, 'L')
                    pdf.cell(col_widths[5], 10, rota['horario'], 1, 0, 'C')
                    pdf.cell(col_widths[6], 10, rota['valor'], 1, 0, 'R')
                    pdf.cell(col_widths[7], 10, rota['pagamento'], 1, 0, 'C')
                    pdf.ln()
        
        # Salvar arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar PDF como"
        )
        
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Sucesso", f"PDF exportado com sucesso para:\n{file_path}")
    
    def exportar_excel(self):
        if not self.motoristas:
            messagebox.showerror("Erro", "Nenhum dado cadastrado para exportar!")
            return
        
        # Criar DataFrame
        dados = []
        for nome, rotas in self.rotas_por_motorista.items():
            motorista_info = next((m for m in self.motoristas if m['nome'] == nome), None)
            if motorista_info:
                for rota in rotas:
                    dados.append({
                        'Motorista': nome,
                        'Idade': motorista_info['idade'],
                        'PIX': motorista_info['pix'],
                        'Data': rota['data'],
                        'Rota': rota['rota'],
                        'Horário': rota['horario'],
                        'Valor': rota['valor'],
                        'Pagamento': rota['pagamento']
                    })
        
        df = pd.DataFrame(dados)
        
        # Salvar arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Salvar Excel como"
        )
        
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Excel exportado com sucesso para:\n{file_path}")
    
    def filtrar_por_mes(self):
        if not self.motoristas:
            messagebox.showerror("Erro", "Nenhum dado cadastrado para filtrar!")
            return
        
        # Janela de seleção de mês/ano
        filtro_window = Toplevel(self.root)
        filtro_window.title("Filtrar por Mês")
        filtro_window.geometry("300x150")
        
        ttk.Label(filtro_window, text="Selecione o mês e ano:").pack(pady=5)
        
        frame_mes = ttk.Frame(filtro_window)
        frame_mes.pack()
        
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        self.mes_var = StringVar()
        ttk.Combobox(frame_mes, textvariable=self.mes_var, values=meses, state="readonly").grid(row=0, column=0, padx=5)
        
        self.ano_var = StringVar(value=str(datetime.now().year))
        ttk.Spinbox(frame_mes, textvariable=self.ano_var, from_=2000, to=2100, width=5).grid(row=0, column=1, padx=5)
        
        ttk.Button(filtro_window, text="Filtrar", command=lambda: self.aplicar_filtro(filtro_window)).pack(pady=10)
    
    def aplicar_filtro(self, window):
        mes = self.mes_var.get()
        ano = self.ano_var.get()
        
        if not mes:
            messagebox.showerror("Erro", "Selecione um mês!")
            return
        
        try:
            mes_num = datetime.strptime(mes, "%B").month
            ano_num = int(ano)
        except ValueError:
            messagebox.showerror("Erro", "Data inválida!")
            return
        
        # Filtrar dados
        dados_filtrados = []
        for nome, rotas in self.rotas_por_motorista.items():
            motorista_info = next((m for m in self.motoristas if m['nome'] == nome), None)
            if motorista_info:
                for rota in rotas:
                    try:
                        data = datetime.strptime(rota['data'], "%d/%m/%Y")
                        if data.month == mes_num and data.year == ano_num:
                            dados_filtrados.append({
                                'Motorista': nome,
                                'Idade': motorista_info['idade'],
                                'PIX': motorista_info['pix'],
                                'Data': rota['data'],
                                'Rota': rota['rota'],
                                'Horário': rota['horario'],
                                'Valor': rota['valor'],
                                'Pagamento': rota['pagamento']
                            })
                    except ValueError:
                        continue
        
        if not dados_filtrados:
            messagebox.showinfo("Info", f"Nenhum dado encontrado para {mes}/{ano}")
            window.destroy()
            return
        
        # Mostrar resultados em nova janela
        resultado_window = Toplevel(self.root)
        resultado_window.title(f"Motoristas e Rotas - {mes}/{ano}")
        resultado_window.geometry("1000x400")
        
        # Treeview
        colunas = ['Motorista', 'Idade', 'PIX', 'Data', 'Rota', 'Horário', 'Valor', 'Pagamento']
        tree = ttk.Treeview(resultado_window, columns=colunas, show='headings')
        
        # Configurar colunas
        col_widths = {
            'Motorista': 120,
            'Idade': 50,
            'PIX': 120,
            'Data': 80,
            'Rota': 100,
            'Horário': 70,
            'Valor': 80,
            'Pagamento': 80
        }
        
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=col_widths[col])
        
        tree.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Adicionar dados filtrados
        for dado in dados_filtrados:
            tree.insert('', END, values=(
                dado['Motorista'],
                dado['Idade'],
                dado['PIX'],
                dado['Data'],
                dado['Rota'],
                dado['Horário'],
                dado['Valor'],
                dado['Pagamento']
            ))
        
        # Botão de exportar
        frame_botoes = ttk.Frame(resultado_window)
        frame_botoes.pack(pady=5)
        
        ttk.Button(frame_botoes, text="Exportar para PDF", 
                  command=lambda: self.exportar_filtro_pdf(dados_filtrados, f"{mes}_{ano}")).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="Exportar para Excel", 
                  command=lambda: self.exportar_filtro_excel(dados_filtrados, f"{mes}_{ano}")).grid(row=0, column=1, padx=5)
        
        window.destroy()
    
    def exportar_filtro_pdf(self, dados, nome_arquivo):
        # Configurar PDF em modo paisagem (landscape)
        pdf = FPDF(orientation='L')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Configurar fonte
        pdf.set_font("Arial", 'B', 14)
        
        # Adicionar logo (se existir)
        if hasattr(self, 'logo_image'):
            temp_logo_path = "temp_logo.png"
            self.logo_image.save(temp_logo_path)
            pdf.image(temp_logo_path, x=10, y=8, w=40)
            os.remove(temp_logo_path)
        
        # Título
        pdf.cell(0, 10, f"Relatório de Motoristas e Rotas - {nome_arquivo.replace('_', '/')}", 0, 1, 'C')
        pdf.ln(10)
        
        # Cabeçalhos
        colunas = ['Motorista', 'Idade', 'PIX', 'Data', 'Rota', 'Horário', 'Valor', 'Pagamento']
        col_widths = [40, 15, 50, 20, 50, 20, 25, 25]
        
        pdf.set_font("Arial", 'B', 10)
        for i, coluna in enumerate(colunas):
            pdf.cell(col_widths[i], 10, coluna, 1, 0, 'C')
        pdf.ln()
        
        # Dados
        pdf.set_font("Arial", '', 8)
        for dado in dados:
            # Ajustar textos longos
            nome_curto = dado['Motorista'][:20] + '...' if len(dado['Motorista']) > 20 else dado['Motorista']
            pix_curto = dado['PIX'][:20] + '...' if len(dado['PIX']) > 20 else dado['PIX']
            rota_curta = dado['Rota'][:20] + '...' if len(dado['Rota']) > 20 else dado['Rota']
            
            pdf.cell(col_widths[0], 10, nome_curto, 1, 0, 'L')
            pdf.cell(col_widths[1], 10, dado['Idade'], 1, 0, 'C')
            pdf.cell(col_widths[2], 10, pix_curto, 1, 0, 'L')
            pdf.cell(col_widths[3], 10, dado['Data'], 1, 0, 'C')
            pdf.cell(col_widths[4], 10, rota_curta, 1, 0, 'L')
            pdf.cell(col_widths[5], 10, dado['Horário'], 1, 0, 'C')
            pdf.cell(col_widths[6], 10, dado['Valor'], 1, 0, 'R')
            pdf.cell(col_widths[7], 10, dado['Pagamento'], 1, 0, 'C')
            pdf.ln()
        
        # Salvar arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar PDF como",
            initialfile=f"motoristas_rotas_{nome_arquivo}"
        )
        
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Sucesso", f"PDF exportado com sucesso para:\n{file_path}")
    
    def exportar_filtro_excel(self, dados, nome_arquivo):
        # Criar DataFrame
        df = pd.DataFrame(dados)
        
        # Salvar arquivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Salvar Excel como",
            initialfile=f"motoristas_rotas_{nome_arquivo}"
        )
        
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Excel exportado com sucesso para:\n{file_path}")

if __name__ == "__main__":
    root = Tk()
    app = SistemaMotoristas(root)
    root.mainloop()