import tkinter as tk
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class LogsAppGUI:
    def __init__(self, root):
        self.root = root
        self.logs_text = None
        self.fig = None

        self.create_logs_text()
        self.start_logs_chart_update()

    def create_logs_text(self):
        self.logs_text = tk.Text(
            self.root,
            bg="black",
            fg="green"
        )
        self.logs_text.pack()

    def redirect_logs_output(self):
        def update_logs_text():
            while True:
                line = input()  # Aguarda a entrada do log
                if line:
                    self.insert_colored_text(line, "green")  # Adicione a cor desejada ao texto
                    self.logs_text.see(tk.END)

        t = threading.Thread(target=update_logs_text)
        t.daemon = True
        t.start()

    def insert_colored_text(self, text, color):
        self.logs_text.insert(tk.END, text)
        self.logs_text.tag_add(color, "end - %d chars" % len(text), tk.END)  # Aplica a tag ao texto inserido
        self.logs_text.tag_config(color, foreground=color)  # Configura a cor do texto para a tag

    def update_logs_chart(self, i):
        # Não é necessário atualizar o gráfico para logs em tempo real
        pass

    def start_logs_chart_update(self):
        self.fig = plt.figure()
        self.fig.subplots_adjust(bottom=0.2)  # Ajusta a parte inferior do gráfico para acomodar o texto dos logs

        # Cria uma animação que chama a função de atualização em intervalos regulares
        anim = animation.FuncAnimation(self.fig, self.update_logs_chart, interval=1000)  # Atualiza a cada 1 segundo (1000ms)

        plt.show()


# Crie a janela principal da GUI
root = tk.Tk()
root.title("Logs Viewer")
root.geometry("600x400")

# Crie a instância da GUI
app = LogsAppGUI(root)

# Inicie o loop de eventos da GUI
root.mainloop()
