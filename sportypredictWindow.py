# Importing libraries
import tkinter as tk
from tkinter import messagebox
from mongodb_connect import MongoDB
from pymongo import DESCENDING
import numpy as np
from sklearn.linear_model import LinearRegression

# Class that will calculate likelihood of player achieving prediction
class Calculation:
    def __init__(self, sample_data):
        self.sample_data = sample_data
        self.model_points = None
        self.model_assists = None
        self.model_rebounds = None

    # Saves to lists
    def _extract_stats(self):
        points = []
        assists = []
        rebounds = []

        for game in self.sample_data:
            points.append(game['points'])
            assists.append(game['assists'])
            rebounds.append(game['totReb'])

        self.points = np.array(points)
        self.assists = np.array(assists)
        self.rebounds = np.array(rebounds)

    # Prepare to train
    def _prepare_feature_sets(self):
        self.X_train_points = np.column_stack((self.assists, self.rebounds))
        self.X_train_assists = np.column_stack((self.points, self.rebounds))
        self.X_train_rebounds = np.column_stack((self.points, self.assists))

    # Trains models
    def _train_models(self):
        self.model_points = self._train_model(self.X_train_points, self.points)
        self.model_assists = self._train_model(self.X_train_assists, self.assists)
        self.model_rebounds = self._train_model(self.X_train_rebounds, self.rebounds)

    def _train_model(self, X, y):
        model = LinearRegression()
        model.fit(X, y)
        return model

    # Returns prediction of points
    def _predict_points(self, assists, rebounds):
        user_input = np.array([[assists, rebounds]])
        prediction = self.model_points.predict(user_input)[0]
        return prediction

    # Returns prediction of assists
    def _predict_assists(self, points, rebounds):
        user_input = np.array([[points, rebounds]])
        prediction = self.model_assists.predict(user_input)[0]
        return prediction

    # Returns prediction of rebounds
    def _predict_rebounds(self, points, assists):
        user_input = np.array([[points, assists]])
        prediction = self.model_rebounds.predict(user_input)[0]
        return prediction

    # Returns likelihood
    def _evaluate_likelihood(self, predicted, actual):
        if predicted >= actual:
            return "Very likely"
        elif 0.9 * actual <= predicted < actual:
            return "Probable"
        else:
            return "Not very likely"

    # Determines if statistic is Points, Assists or Rebounds
    def predict_stat(self, stat, value):
        if stat == "Points":
            predicted_value = self._predict_points(self.assists[-1], self.rebounds[-1])
        elif stat == "Assists":
            predicted_value = self._predict_assists(self.points[-1], self.rebounds[-1])
        elif stat == "Rebounds":
            predicted_value = self._predict_rebounds(self.points[-1], self.assists[-1])
        else:
            raise ValueError("Invalid stat choice.")

        likelihood = self._evaluate_likelihood(predicted_value, value)

        return predicted_value, likelihood

# Class that runs the application
class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("SportyPredict")
        self.master.geometry("600x400")

        # Label on top of screen
        self.titleLabel = tk.Label(master, text="SportyPredict")
        self.titleLabel.grid(row=0, column=1, padx=10, pady=10)

        # Label on left side of screen
        self.predictLabel = tk.Label(master, text="PREDICTION")
        self.predictLabel.grid(row=1, column=0, padx=10, pady=10)
        self.playerValue = tk.StringVar(value="Select a Player...")
        self.playerMenu = tk.OptionMenu(master, self.playerValue, "LeBron James", 
                                         "Stephen Curry", "Nikola Jokic")
        self.playerMenu.grid(row=2, column=0, padx=10, pady=10)

        # Label on middle of screen lined up with left side
        self.statValue = tk.StringVar(value="Select a Statistic...")
        self.statMenu = tk.OptionMenu(master, self.statValue, "Points", 
                                         "Assists", "Rebounds")
        self.statMenu.grid(row=2, column=1, padx=10, pady=10)

        # Label on right side of screen lined up with middle and left side
        self.valueLabel = tk.Label(master, text="VALUE")
        self.valueLabel.grid(row=1, column=2, padx=10, pady=10)
        self.valueText = tk.Entry(master)
        self.valueText.grid(row=2, column=2, padx=10, pady=10)

        # Button that calculates if prediction could be right
        self.calculateButton = tk.Button(master, text="CALCULATE", command=self.calculate)
        self.calculateButton.grid(row=3, column=1, padx=10, pady=10)
    
    # Method that returns value of required statistic
    def getStat(self):
        return self.statValue.get()
    
    # Method that returns value of amount of statistic
    def getValue(self):
        return self.valueText.get()
    
    def getPlayer(self):
        return self.playerValue.get()

    """
    # Method that returns data of player
    def storeInfo(self):
        player_name = self.playerValue.get().split()[0]
        mongo_db = MongoDB()
        games = mongo_db.games(player_name)

        index = 0
        for item in games:
            if "player" in item:
                break
            index += 1
        result = games[index:] if index < len(games) else []
        return result
        """
    

    # Calculates data likelihood
    def calculate(self):
        player = self.getPlayer()

        lebron_data = [
        {'player': {'id': 265, 'firstname': 'LeBron', 'lastname': 'James'}, 'team': {'id': 17, 'name': 'Los Angeles Lakers', 'nickname': 'Lakers', 'code': 'LAL', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png'}, 'game': {'id': 13779}, 'points': 24, 'pos': 'SF', 'min': '35', 'fgm': 10, 'fga': 21, 'fgp': '47.6', 'ftm': 4, 'fta': 5, 'ftp': '80.0', 'tpm': 0, 'tpa': 1, 'tpp': '0', 'offReb': 1, 'defReb': 10, 'totReb': 11, 'assists': 4, 'pFouls': 5, 'steals': 2, 'turnovers': 6, 'blocks': 0, 'plusMinus': '+19', 'comment': None}, {'player': {'id': 265, 'firstname': 'LeBron', 'lastname': 'James'}, 'team': {'id': 17, 'name': 'Los Angeles Lakers', 'nickname': 'Lakers', 'code': 'LAL', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png'}, 'game': {'id': 12854}, 'points': 33, 'pos': 'SF', 'min': '40', 'fgm': 14, 'fga': 27, 'fgp': '51.9', 'ftm': 2, 'fta': 3, 'ftp': '66.7', 'tpm': 3, 'tpa': 8, 'tpp': '37.5', 'offReb': 2, 'defReb': 6, 'totReb': 8, 'assists': 9, 'pFouls': 1, 'steals': 3, 'turnovers': 4, 'blocks': 1, 'plusMinus': '-4', 'comment': None}, {'player': {'id': 265, 'firstname': 'LeBron', 'lastname': 'James'}, 'team': {'id': 17, 'name': 'Los Angeles Lakers', 'nickname': 'Lakers', 'code': 'LAL', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png'}, 'game': {'id': 12879}, 'points': 23, 'pos': 'SF', 'min': '36', 'fgm': 7, 'fga': 17, 'fgp': '41.2', 'ftm': 7, 'fta': 10, 'ftp': '70.0', 'tpm': 2, 'tpa': 6, 'tpp': '33.3', 'offReb': 2, 'defReb': 5, 'totReb': 7, 'assists': 14, 'pFouls': 1, 'steals': 2, 'turnovers': 2, 'blocks': 0, 'plusMinus': '-28', 'comment': None}
        ]

        steph_data = [
            {'player': {'id': 124, 'firstname': 'Stephen', 'lastname': 'Curry'}, 'team': {'id': 11, 'name': 'Golden State Warriors', 'nickname': 'Warriors', 'code': 'GSW', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/d/de/Warriors_de_Golden_State_logo.svg/1200px-Warriors_de_Golden_State_logo.svg.png'}, 'game': {'id': 13337}, 'points': 41, 'pos': 'PG', 'min': '35', 'fgm': 15, 'fga': 31, 'fgp': '48.4', 'ftm': 2, 'fta': 2, 'ftp': '100.0', 'tpm': 9, 'tpa': 19, 'tpp': '47.4', 'offReb': 1, 'defReb': 3, 'totReb': 4, 'assists': 5, 'pFouls': 3, 'steals': 0, 'turnovers': 4, 'blocks': 0, 'plusMinus': '-6', 'comment': None}, {'player': {'id': 124, 'firstname': 'Stephen', 'lastname': 'Curry'}, 'team': {'id': 11, 'name': 'Golden State Warriors', 'nickname': 'Warriors', 'code': 'GSW', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/d/de/Warriors_de_Golden_State_logo.svg/1200px-Warriors_de_Golden_State_logo.svg.png'}, 'game': {'id': 13932}, 'points': 16, 'pos': 'PG', 'min': '35', 'fgm': 4, 'fga': 14, 'fgp': '28.6', 'ftm': 6, 'fta': 8, 'ftp': '75.0', 'tpm': 2, 'tpa': 8, 'tpp': '25.0', 'offReb': 1, 'defReb': 1, 'totReb': 2, 'assists': 10, 'pFouls': 2, 'steals': 1, 'turnovers': 4, 'blocks': 0, 'plusMinus': '-2', 'comment': None}, {'player': {'id': 124, 'firstname': 'Stephen', 'lastname': 'Curry'}, 'team': {'id': 11, 'name': 'Golden State Warriors', 'nickname': 'Warriors', 'code': 'GSW', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/d/de/Warriors_de_Golden_State_logo.svg/1200px-Warriors_de_Golden_State_logo.svg.png'}, 'game': {'id': 13350}, 'points': 32, 'pos': 'PG', 'min': '32', 'fgm': 12, 'fga': 24, 'fgp': '50.0', 'ftm': 2, 'fta': 2, 'ftp': '100.0', 'tpm': 6, 'tpa': 13, 'tpp': '46.2', 'offReb': 0, 'defReb': 1, 'totReb': 1, 'assists': 8, 'pFouls': 1, 'steals': 3, 'turnovers': 1, 'blocks': 0, 'plusMinus': '+25', 'comment': None}
        ]

        jokic_data = [
            {'player': {'id': 279, 'firstname': 'Nikola', 'lastname': 'Jokic'}, 'team': {'id': 9, 'name': 'Denver Nuggets', 'nickname': 'Nuggets', 'code': 'DEN', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/3/35/Nuggets_de_Denver_2018.png/180px-Nuggets_de_Denver_2018.png'}, 'game': {'id': 13662}, 'points': 36, 'pos': 'C', 'min': '40', 'fgm': 14, 'fga': 24, 'fgp': '58.3', 'ftm': 5, 'fta': 6, 'ftp': '83.3', 'tpm': 3, 'tpa': 8, 'tpp': '37.5', 'offReb': 1, 'defReb': 16, 'totReb': 17, 'assists': 10, 'pFouls': 2, 'steals': 0, 'turnovers': 5, 'blocks': 0, 'plusMinus': '+12', 'comment': None}, {'player': {'id': 279, 'firstname': 'Nikola', 'lastname': 'Jokic'}, 'team': {'id': 9, 'name': 'Denver Nuggets', 'nickname': 'Nuggets', 'code': 'DEN', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/3/35/Nuggets_de_Denver_2018.png/180px-Nuggets_de_Denver_2018.png'}, 'game': {'id': 13678}, 'points': 19, 'pos': 'C', 'min': '31', 'fgm': 6, 'fga': 13, 'fgp': '46.2', 'ftm': 5, 'fta': 6, 'ftp': '83.3', 'tpm': 2, 'tpa': 3, 'tpp': '66.7', 'offReb': 1, 'defReb': 13, 'totReb': 14, 'assists': 11, 'pFouls': 1, 'steals': 2, 'turnovers': 4, 'blocks': 0, 'plusMinus': '+19', 'comment': None}, {'player': {'id': 279, 'firstname': 'Nikola', 'lastname': 'Jokic'}, 'team': {'id': 9, 'name': 'Denver Nuggets', 'nickname': 'Nuggets', 'code': 'DEN', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/3/35/Nuggets_de_Denver_2018.png/180px-Nuggets_de_Denver_2018.png'}, 'game': {'id': 13702}, 'points': 28, 'pos': 'C', 'min': '34', 'fgm': 12, 'fga': 20, 'fgp': '60.0', 'ftm': 2, 'fta': 2, 'ftp': '100.0', 'tpm': 2, 'tpa': 2, 'tpp': '100.0', 'offReb': 5, 'defReb': 8, 'totReb': 13, 'assists': 7, 'pFouls': 2, 'steals': 3, 'turnovers': 5, 'blocks': 1, 'plusMinus': '+23', 'comment': None}
        ]

        if player == "Lebron James":
            player_data = lebron_data
        elif player == "Stephen Curry":
            player_data = steph_data
        else:
            player_data = jokic_data
        predictor = Calculation(player_data)
        predictor._extract_stats()
        predictor._prepare_feature_sets()
        predictor._train_models()

        stat = self.getStat()
        value = float(self.getValue())
        predicted_value, likelihood = predictor.predict_stat(stat, value)

        result_message = f"Prediction: {predicted_value:.2f}, Likelihood: {likelihood}"
        messagebox.showinfo("Prediction Result", result_message)

# Runs application
window = tk.Tk()
my_gui = MainWindow(window)
window.mainloop()