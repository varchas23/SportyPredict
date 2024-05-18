import tkinter as tk

class SportyPredict(tk.Frame):
    def __init__(self, master):
        self.master = master
        master.title("SportyPredict")

        self.titleLabel = tk.Label(master, text="SportyPredict").grid(row=0, column=1, padx=10, pady=10)

        self.predictLabel = tk.Label(master, text="PREDICTION").grid(row=1, column=0, padx=10, pady=10)
        self.predictionInitValue = tk.StringVar(value="Select a Prediction...")
        self.predictMenu = tk.OptionMenu(master, self.predictionInitValue, "LeBron James 25 Points", 
                                         "Stephen Curry 5 Assists", "Nikola Jokic 10 Rebounds")
        self.predictMenu.grid(row=2, column=0, padx=10, pady=10)

        self.wagerLabel = tk.Label(master, text="WAGER").grid(row=1, column=2, padx=10, pady=10)
        self.wagerText = tk.Entry(master).grid(row=2, column=2, padx=10, pady=10)

        self.calculateButton = tk.Button(master, text="CALCULATE").grid(row=3, column=1, padx=10, pady=10)

window = tk.Tk()
my_gui = SportyPredict(window)
window.mainloop()
