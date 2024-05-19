import numpy as np
from sklearn.linear_model import LinearRegression
import main_window

class Calculation:
    def __init__(self, sample_data):
        self.sample_data = sample_data
        self.model_points = None
        self.model_assists = None
        self.model_rebounds = None

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

    def _prepare_feature_sets(self):
        self.X_train_points = np.column_stack((self.assists, self.rebounds))
        self.X_train_assists = np.column_stack((self.points, self.rebounds))
        self.X_train_rebounds = np.column_stack((self.points, self.assists))

    def _train_models(self):
        self.model_points = self._train_model(self.X_train_points, self.points)
        self.model_assists = self._train_model(self.X_train_assists, self.assists)
        self.model_rebounds = self._train_model(self.X_train_rebounds, self.rebounds)

    def _train_model(self, X, y):
        model = LinearRegression()
        model.fit(X, y)
        return model

    def _predict_points(self, assists, rebounds):
        user_input = np.array([[assists, rebounds]])
        prediction = self.model_points.predict(user_input)[0]
        return prediction

    def _predict_assists(self, points, rebounds):
        user_input = np.array([[points, rebounds]])
        prediction = self.model_assists.predict(user_input)[0]
        return prediction

    def _predict_rebounds(self, points, assists):
        user_input = np.array([[points, assists]])
        prediction = self.model_rebounds.predict(user_input)[0]
        return prediction

    def _evaluate_likelihood(self, predicted, actual):
        if predicted >= actual:
            return "Very likely"
        elif 0.9 * actual <= predicted < actual:
            return "Probable"
        else:
            return "Not very likely"

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

# Sample data for a player from database
sample_data = [
    {'player': {'id': 265, 'firstname': 'LeBron', 'lastname': 'James'}, 'team': {'id': 17, 'name': 'Los Angeles Lakers', 'nickname': 'Lakers', 'code': 'LAL', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png'}, 'game': {'id': 13779}, 'points': 24, 'pos': 'SF', 'min': '35', 'fgm': 10, 'fga': 21, 'fgp': '47.6', 'ftm': 4, 'fta': 5, 'ftp': '80.0', 'tpm': 0, 'tpa': 1, 'tpp': '0', 'offReb': 1, 'defReb': 10, 'totReb': 11, 'assists': 4, 'pFouls': 5, 'steals': 2, 'turnovers': 6, 'blocks': 0, 'plusMinus': '+19', 'comment': None}, {'player': {'id': 265, 'firstname': 'LeBron', 'lastname': 'James'}, 'team': {'id': 17, 'name': 'Los Angeles Lakers', 'nickname': 'Lakers', 'code': 'LAL', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png'}, 'game': {'id': 12854}, 'points': 33, 'pos': 'SF', 'min': '40', 'fgm': 14, 'fga': 27, 'fgp': '51.9', 'ftm': 2, 'fta': 3, 'ftp': '66.7', 'tpm': 3, 'tpa': 8, 'tpp': '37.5', 'offReb': 2, 'defReb': 6, 'totReb': 8, 'assists': 9, 'pFouls': 1, 'steals': 3, 'turnovers': 4, 'blocks': 1, 'plusMinus': '-4', 'comment': None}, {'player': {'id': 265, 'firstname': 'LeBron', 'lastname': 'James'}, 'team': {'id': 17, 'name': 'Los Angeles Lakers', 'nickname': 'Lakers', 'code': 'LAL', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png'}, 'game': {'id': 12879}, 'points': 23, 'pos': 'SF', 'min': '36', 'fgm': 7, 'fga': 17, 'fgp': '41.2', 'ftm': 7, 'fta': 10, 'ftp': '70.0', 'tpm': 2, 'tpa': 6, 'tpp': '33.3', 'offReb': 2, 'defReb': 5, 'totReb': 7, 'assists': 14, 'pFouls': 1, 'steals': 2, 'turnovers': 2, 'blocks': 0, 'plusMinus': '-28', 'comment': None}
]

# Create an instance of the class
predictor = Calculation(sample_data)
# Call the method to extract stats
predictor._extract_stats()
# Call the method to prepare feature sets
predictor._prepare_feature_sets()
# Call the method to train models
predictor._train_models()
# Call the method to predict a stat and evaluate likelihood
predicted_value, likelihood = predictor.predict_stat(main_window.MainWindow.getStat, main_window.MainWindow.getValue)

# Output the predictions and evaluations
def predictionResults(predicted_value, likelihood):
    return f"Prediction: {predicted_value:.2f}, Likelihood: {likelihood}"
