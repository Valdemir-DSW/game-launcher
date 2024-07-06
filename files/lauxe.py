import os
import json
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk,font
from PIL import Image, ImageTk
import requests
import zipfile
from threading import Thread
import urllib3
import time
import subprocess
import webbrowser
# Desativar avisos de segurança sobre HTTPS não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
download_in_progress = False

#
#
#
#variaveis
# URL do arquivo ZIP para download
# Desativar avisos de segurança sobre HTTPS não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Variáveis globais
download_in_progress = False
JSON_URL = "https://github.com/Valdemir-DSW/game-launcher/raw/main/teste/news.json"
ZIP_URL = "https://github.com/Valdemir-DSW/game-launcher/raw/main/teste/gamediretorio/XP%20pinn%20ball.zip"
link1_nome = "site"
link1_cor = "blue"
link1_com = "valdemir-rs.rf.gd"
link2_nome = "github"
link2_cor = "orange"
link2_com = "https://github.com/Valdemir-DSW/game-launcher"
link3_nome = "libaaaaaaaaaaa"
link3_cor = "orange"
link3_com = "oraccccge"
local_json_path = os.path.abspath("gamelib/config.json")
exename = " "

# Funções utilitárias


# Função para verificar a existência da pasta gamelib
def check_gamelib():
    return os.path.exists('gamelib')

# Função para calcular o tamanho da pasta gamelib
def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Função para converter tamanho em bytes para uma string legível
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"

def on_close():
    global download_in_progress
    if download_in_progress:
        if messagebox.askokcancel("Questão", "Se você fechar agora o download será cancelado tem certeza que deseja fechar?"):
            download_in_progress = False
            root.destroy()
    else:
        root.destroy()
# Função para carregar configurações do arquivo JSON
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            return json.load(f)
    return {"notification_style": "info"}

# Função para salvar configurações no arquivo JSON
def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

# Função para extrair o arquivo ZIP
def extract_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall('gamelib')

  
    with open(local_json_path, 'r') as file:
        local_data = json.load(file)
        global exename
       
        exename = local_data["exename"]

    if settings['notification_style'] == 'info':
        messagebox.showinfo("Instalação", "Jogo instalado com sucesso!")
    else:
        messagebox.showwarning("Instalação", "Jogo instalado com sucesso!")
    update_ui()

# Função para baixar e instalar o jogo
def download_and_install():
    global download_in_progress
    install_button.config(state=tk.DISABLED)
    try:
        response = requests.get(ZIP_URL, stream=True, verify=False)  # Desabilitar verificação SSL
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar["maximum"] = total_size

        start_time = time.time()

        if response.status_code == 200:
            os.makedirs('cash', exist_ok=True)
            zip_path = os.path.join('cash', 'game.zip')
            downloaded_size = 0  # Tamanho baixado até o momento

            with open(zip_path, 'wb') as zip_file:
                for data in response.iter_content(block_size):
                    download_in_progress = True
                    zip_file.write(data)
                    downloaded_size += len(data)
                    progress_bar["value"] = downloaded_size

                    elapsed_time = time.time() - start_time
                    remaining_time = (total_size - downloaded_size) / (downloaded_size / elapsed_time) if downloaded_size > 0 else 0

                    progress_label.config(text=f"Baixado: {sizeof_fmt(downloaded_size)} / {sizeof_fmt(total_size)} | Restante: {sizeof_fmt(total_size - downloaded_size)} | Tempo Restante: {int(remaining_time // 60)}m {int(remaining_time % 60)}s")
                    root.update_idletasks()

            Thread(target=extract_zip, args=(zip_path,)).start()
        else:
            messagebox.showerror("Erro", "Falha ao baixar o arquivo.")
    except float as e:
        
        download_and_install()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante o download: {e}")    
    finally:
        install_button.config(state=tk.NORMAL)
        download_in_progress = False

def repair_game():
    if messagebox.askquestion("Tem certeza disso?", "Ao clicar em sim você irá baixar todo o jogo de novo você não irá poder jogar.\nApós o download ser concluído novamente você receberá uma mensagem, não feche a janela enquanto a execução estiver sendo feita!") == "yes":
        install_button.config(state=tk.DISABLED)
        Thread(target=download_and_install).start()

# Função para iniciar a instalação em uma nova thread
def install_game():
    install_button.config(state=tk.DISABLED)
    Thread(target=download_and_install).start()

# Função para atualizar a interface
def update_ui():
    if check_gamelib():
        install_button.config(text="Iniciar Jogo", command=run_game, state=tk.NORMAL, bg="orange")
        progress_bar.pack_forget()
        repair_button.place(x=444, y=544)
        progress_bar.place(x=444, y=800)
    else:
        install_button.config(text="Instalar Jogo", command=install_game, state=tk.NORMAL, bg="blue")
        progress_bar.place(x=444, y=544)
        repair_button.place(x=444, y=800)
        repair_button.pack_forget()

# Função para ler o caminho do executável e iniciar o jogo (simulada)
def run_game():
    
    past = "gamelib/"
    exe2 = past+exename
    exe =  os.path.abspath(exe2)
    print(exe2)
    subprocess.Popen(exe)
    if settings['notification_style'] == 'info':
       pass
    else:
        messagebox.showwarning("Iniciar Jogo", f"Iniciando o jogo: {exename}")

# Função para abrir a tela de configurações
def open_menu(event):
    load_and_display_news(event)
    if (1028 - 20) <= event.x <= (1028 + 20) and (61 - 20) <= event.y <= (61 + 20):  # Coordenadas específicas para o clique
        if settings_frame.winfo_ismapped():
            settings_frame.pack_forget()
        else:
            settings_frame.pack(pady=20)

def close_settings():
    settings_frame.pack_forget()

def update_notification_style(var):
    settings['notification_style'] = var.get()
    save_settings(settings)

def delete_files():
    if messagebox.askquestion("Tem certeza disso?", "Você tem certeza que deseja excluir todos os arquivos da pasta gamelib?") == "yes":
        shutil.rmtree('gamelib')
        messagebox.showinfo("Excluir Arquivos", "Todos os arquivos foram excluídos.")
        update_ui()

def clean_cash():
    if messagebox.askquestion("Tem certeza disso?", "Você tem certeza que deseja limpar a pasta de cache?") == "yes":
        shutil.rmtree('cash')
        os.makedirs('cash', exist_ok=True)
        messagebox.showinfo("Limpar Cache", "A pasta de cache foi limpa.")
        clean_cash_button.config(text="Nenhum Cash para limpar")

def get_image_paths(folder_path):
    # Lista todas as imagens na pasta especificada
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
def load_and_display_news(event):
     if (984 - 19) <= event.x <= (984 + 19) and (61 - 19) <= event.y <= (61 + 19): 
                try:
                    response = requests.get(JSON_URL)
                    response.raise_for_status()  # Verificar se houve algum erro na requisição
                    news_data = response.json()

                    news = sorted(news_data["news"], key=lambda x: x["vers"], reverse=True)  # Ordenar por versão mais recente

                    news_text = ""
                    for item in news:
                        news_text += f"Versão: {item['vers']}\nConteúdo: {item['content']}\n\n"

                    # Criar uma nova janela para exibir as notícias
                    news_window = tk.Toplevel(root)
                    news_window.title("Notícias")
                    news_window.geometry("500x400")
                    news_window.config(background="black")
                    news_window.resizable(False, False)
                    news_window.overrideredirect(True)

                    # Frame e Canvas para a barra de rolagem
                    frame = tk.Frame(news_window,background="black", bd=0, highlightthickness=0)
                    frame.pack(fill=tk.BOTH, expand=True)

                    canvas = tk.Canvas(frame,background="black", bd=0, highlightthickness=0)
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    scrollbar = tk.Scrollbar(frame,background="black", orient=tk.VERTICAL, command=canvas.yview, bd=0)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                    scrollable_frame = tk.Frame(canvas,background="black", bd=0)
                    def iniciar_arrasto(event):
                        news_window._x = event.x
                        news_window._y = event.y

                    def mover_janela(event):
                        nova_pos_x = news_window.winfo_pointerx() - news_window._x
                        nova_pos_y = news_window.winfo_pointery() - news_window._y
                        news_window.geometry(f"+{nova_pos_x}+{nova_pos_y}")

                    # Bindings para eventos de arrasto
                    news_window.bind("<ButtonPress-1>", iniciar_arrasto)
                    news_window.bind("<B1-Motion>", mover_janela)

                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(
                            scrollregion=canvas.bbox("all")
                        )
                    )

                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)

                    # Label para exibir as notícias
                    news_label = tk.Label(scrollable_frame, text=news_text, justify=tk.LEFT, wraplength=480, anchor="nw",background="black",fg="white", bd=0)
                    news_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                    # Botão para fechar a janela de notícias
                    close_button = tk.Button(news_window, text="Fechar", command=news_window.destroy)
                    close_button.pack(pady=10)
                
                except requests.exceptions.RequestException as e:
                          messagebox.showerror("Erro", f"Erro ao carregar as notícias: {e}")
def atualizar():
        update_ui()
        install_button.config(text="UPDATE", command=install_game, state=tk.NORMAL, bg="blue")
        progress_bar.place(x=444, y=544)
        repair_button.place(x=444, y=800)
        repair_button.pack_forget()  
        print('oi')                  
def load_image():
    global current_image_index
    global image_paths
    global image_label

    # Verifica se há imagens para carregar
    if image_paths:
        # Obtém o caminho da próxima imagem
        image_path = image_paths[current_image_index]

        # Carrega a imagem
        img = Image.open(image_path)
        img = img.resize((1132, 326),Image.LANCZOS)  # Redimensiona a imagem conforme necessário

        # Converte a imagem para o formato que o Tkinter pode exibir
        photo = ImageTk.PhotoImage(img)

        # Atualiza a imagem no Label
        image_label.config(image=photo)
        image_label.image = photo  # Mantém uma referência para evitar que a imagem seja coletada pelo garbage collector

        # Atualiza para a próxima imagem na próxima chamada
        current_image_index = (current_image_index + 1) % len(image_paths)

    # Atualiza a imagem a cada 5 segundos (5000 milissegundos)
    root.after(7444, load_image)
# Carregar as configurações iniciais
settings = load_settings()

# Criar a janela principal
root = tk.Tk()
root.title(" ")
root.geometry("1200x644")
root.resizable(False, False)

# Carregar a imagem de fundo
background_image = Image.open("back.png")
background_image = background_image.resize((1200, 664), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Criar um rótulo para a imagem de fundo
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Adicionar bind para o evento de clique no rótulo de fundo
background_label.bind("<Button-1>", open_menu)
image_label = tk.Label(root, bd=0)
image_label.place(x=28, y=100) 
folder_path = "updateimagem"
image_paths = get_image_paths(folder_path)
current_image_index = 0

# Inicia o carregamento da primeira imagem
load_image()

# Criar botão de ação
install_button = tk.Button(root, text="", command=None, font=("Helvetica", 16), width=30, height=4)
install_button.place(x=24, y=507)  # Ajuste a posição conforme necessário

# Criar barra de progresso
style = ttk.Style()
style.configure('Custom.Horizontal.TProgressbar', troughcolor='orange', background='black')
progress_bar = ttk.Progressbar(root, style='Custom.Horizontal.TProgressbar', length=200, mode='determinate')
progress_bar.place(x=400, y=800)  # Posiciona a barra de progresso ao lado do botão principal

# Criar botão de consertar arquivos
repair_button = tk.Button(root, text="Consertar Arquivos", command=repair_game)

custom_font = font.Font(family="fontekkk", size=10, weight="bold")
progress_label = tk.Label(root, font=custom_font,background="black",fg="orange",text="")
progress_label.place(x=444,y=584)

# Criar frame de configurações
settings_frame = tk.Frame(root, bg="black", width=1200)
settings_frame.pack_forget()

close_button = tk.Button(settings_frame, text="X", command=close_settings, bg="red", fg="white")
close_button.pack(pady=5, padx=5, anchor='ne')
gamelocaç = os.path.abspath("gamelib")
label = tk.Label(settings_frame, text=f"Menu > jogo em > {gamelocaç}", bg="black", fg="white")
label.pack(pady=20)

if check_gamelib():
    folder_size = get_folder_size('gamelib')
    size_label = tk.Label(settings_frame, text=f"Tamanho gasto pelo jogo {sizeof_fmt(folder_size)}", bg="black", fg="white")
    size_label.pack(pady=10)

    delete_button = tk.Button(settings_frame, text="Deletar jogo", command=delete_files, bg="red", fg="white")
    delete_button.pack(pady=10)

notification_var = tk.StringVar(value=settings['notification_style'])
notification_check = tk.Checkbutton(settings_frame, text="Usar notificações de aviso", variable=notification_var, onvalue='warning', offvalue='info', bg="black", fg="white", selectcolor="black", command=lambda: update_notification_style(notification_var))
notification_check.pack(pady=10)

# Adicionar botão para limpar a pasta cash
clean_cash_button = tk.Button(settings_frame, text=f"Limpar {sizeof_fmt(get_folder_size('cash'))} de Cache", command=clean_cash, bg="red", fg="white")
clean_cash_button.pack(pady=10)

try:
    # Fazer a requisição HTTP para obter o JSON da web
    response = requests.get(JSON_URL)
    response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
    
    # Carregar o JSON da web
    data = response.json()
    
    # Pegar a última versão do JSON da web
    latest_news = max(data["news"], key=lambda x: x["vers"])
    latest_version = latest_news["vers"]
    
    # Carregar o JSON local
    with open(local_json_path, 'r') as file:
        local_data = json.load(file)
        current_version = local_data["current_version"]
        exename = local_data["exename"]
    
    # Comparar as versões
    if latest_version > current_version:
        print(f"Nova versão disponível: {latest_version}")
        atualizar()
        

    else:
        pass
        update_ui()
    
except requests.exceptions.RequestException as e:
    print(f"Falha ao buscar o JSON da web: {e}")
    update_ui()
except FileNotFoundError:
    print(f"O arquivo {local_json_path} não foi encontrado.")
    update_ui()
except json.JSONDecodeError:
    print("Erro ao decodificar o JSON.")
    update_ui()
except KeyError as e:
    print(f"Chave não encontrada no JSON: {e}")
    update_ui()
def weblink(index):
    if index == 1 :
     webbrowser.open(link1_com)
    elif index == 2:
        webbrowser.open(link2_com) 
    else:
        webbrowser.open(link3_com) 

if link1_nome is not None:
    if link1_cor == "black":
        link1 = tk.Button(root, text=link1_nome, bg=link1_cor, fg="white", command=lambda: weblink(1))
    else:
        link1 = tk.Button(root, text=link1_nome, bg=link1_cor, command=lambda: weblink(1))
    link1.place(x=1000, y=510)

if link2_nome is not None:
    if link2_cor == "black":
        link2 = tk.Button(root, text=link2_nome, bg=link2_cor, fg="white", command=lambda: weblink(2))
    else:
        link2 = tk.Button(root, text=link2_nome, bg=link2_cor, command=lambda: weblink(2))
    link2.place(x=1000, y=550)

if link3_nome is not None:
    if link3_cor == "black":
        link3 = tk.Button(root, text=link3_nome, bg=link3_cor, fg="white", command=lambda: weblink(3))
    else:
        link3 = tk.Button(root, text=link3_nome, bg=link3_cor, command=lambda: weblink(3))
    link3.place(x=1000, y=590)

# Atualizar a interface com base na existência da pasta gamelib

root.protocol("WM_DELETE_WINDOW", on_close)
# Executar a aplicação
root.mainloop()
