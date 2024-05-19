import tkinter as tk

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("SportyPredict")
        self.master.geometry("600x400")

        self.titleLabel = tk.Label(master, text="SportyPredict")
        self.titleLabel.grid(row=0, column=1, padx=10, pady=10)

        self.predictLabel = tk.Label(master, text="PREDICTION")
        self.predictLabel.grid(row=1, column=0, padx=10, pady=10)
        self.predictionValue = tk.StringVar(value="Select a Prediction...")
        self.predictMenu = tk.OptionMenu(master, self.predictionValue, "LeBron James 25 Points", 
                                         "Stephen Curry 5 Assists", "Nikola Jokic 10 Rebounds")
        self.predictMenu.grid(row=2, column=0, padx=10, pady=10)

        self.wagerLabel = tk.Label(master, text="WAGER")
        self.wagerLabel.grid(row=1, column=2, padx=10, pady=10)
        self.wagerText = tk.Entry(master)
        self.wagerText.grid(row=2, column=2, padx=10, pady=10)

        self.calculateButton = tk.Button(master, text="CALCULATE", command=self.calculate)
        self.calculateButton.grid(row=3, column=1, padx=10, pady=10)
    
    def calculate(self):
        pass

window = tk.Tk()
my_gui = MainWindow(window)
window.mainloop()
