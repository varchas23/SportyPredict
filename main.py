import streamlit as st
from pymongo import MongoClient
import numpy as np
from sklearn.linear_model import LinearRegression

# MongoDB class
# MongoDB class (Updated)
class MongoDB:
    def __init__(self, uri="mongodb+srv://SportyPredictAdmin:Password@sportypredict.fpxpjl1.mongodb.net/", db_name="my_database"):
        self.client = MongoClient(uri)
        self.db = self.client.my_database

    def games(self, player_firstname, num_games=None):
        collection = self.db['PlayerStats']
        query = {"response.player.firstname": player_firstname}
        projection = {
            "_id": 0,
            "response": 1
        }
        games = collection.find(query, projection)

        game_data = []
        for game in games:
            responses = game.get("response", [])
            for response in responses:
                if "player" in response and response["player"]["firstname"] == player_firstname:
                    game_data.append({
                        "game_id": response.get("game", {}).get("id", 0),
                        "points": response.get("points", 0),
                        "assists": response.get("assists", 0),
                        "totReb": response.get("totReb", 0),
                        "steals": response.get("steals", 0),  # Added stealing stat
                        "blocks": response.get("blocks", 0)   # Added blocking stat
                    })
        
        if num_games is not None:
            return game_data[-num_games:]
        else:
            return game_data


# Class that will calculate likelihood of player achieving prediction
class Calculation:
    def __init__(self, sample_data):
        self.sample_data = sample_data
        self.model_points = None
        self.model_assists = None
        self.model_rebounds = None
        self.model_steals = None  # Model for predicting steals
        self.model_blocks = None  # Model for predicting blocks

    def _extract_stats(self):
        points = []
        assists = []
        rebounds = []
        steals = []   # List for stealing stats
        blocks = []   # List for blocking stats

        for game in self.sample_data:
            points.append(game['points'])
            assists.append(game['assists'])
            rebounds.append(game['totReb'])
            steals.append(game['steals'])   # Added stealing stat
            blocks.append(game['blocks'])   # Added blocking stat

        self.points = np.array(points)
        self.assists = np.array(assists)
        self.rebounds = np.array(rebounds)
        self.steals = np.array(steals)     # Array for stealing stats
        self.blocks = np.array(blocks)     # Array for blocking stats

    def _prepare_feature_sets(self):
        self.X_train_points = np.column_stack((self.assists, self.rebounds, self.steals, self.blocks))
        self.X_train_assists = np.column_stack((self.points, self.rebounds, self.steals, self.blocks))
        self.X_train_rebounds = np.column_stack((self.points, self.assists, self.steals, self.blocks))
        self.X_train_steals = np.column_stack((self.points, self.assists, self.rebounds, self.blocks))  # Features for stealing model
        self.X_train_blocks = np.column_stack((self.points, self.assists, self.rebounds, self.steals))  # Features for blocking model

    def _train_models(self):
        self.model_points = self.train_model(self.X_train_points, self.points)
        self.model_assists = self.train_model(self.X_train_assists, self.assists)
        self.model_rebounds = self.train_model(self.X_train_rebounds, self.rebounds)
        self.model_steals = self.train_model(self.X_train_steals, self.steals)   # Training stealing model
        self.model_blocks = self.train_model(self.X_train_blocks, self.blocks)   # Training blocking model

    def train_model(self, X, y):  # Corrected method name
        model = LinearRegression()
        model.fit(X, y)
        return model

    def _predict_points(self, assists, rebounds, steals, blocks):
        user_input = np.array([[assists, rebounds, steals, blocks]])
        prediction = self.model_points.predict(user_input)[0]
        return prediction

    def _predict_assists(self, points, rebounds, steals, blocks):
        user_input = np.array([[points, rebounds, steals, blocks]])
        prediction = self.model_assists.predict(user_input)[0]
        return prediction

    def _predict_rebounds(self, points, assists, steals, blocks):
        user_input = np.array([[points, assists, steals, blocks]])
        prediction = self.model_rebounds.predict(user_input)[0]
        return prediction

    def _predict_steals(self, points, assists, rebounds, blocks):
        user_input = np.array([[points, assists, rebounds, blocks]])
        prediction = self.model_steals.predict(user_input)[0]   # Predicting steals
        return prediction

    def _predict_blocks(self, points, assists, rebounds, steals):
        user_input = np.array([[points, assists, rebounds, steals]])
        prediction = self.model_blocks.predict(user_input)[0]   # Predicting blocks
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
            predicted_value = self._predict_points(self.assists[-1], self.rebounds[-1], self.steals[-1], self.blocks[-1])
        elif stat == "Assists":
            predicted_value = self._predict_assists(self.points[-1], self.rebounds[-1], self.steals[-1], self.blocks[-1])
        elif stat == "Rebounds":
            predicted_value = self._predict_rebounds(self.points[-1], self.assists[-1], self.steals[-1], self.blocks[-1])
        elif stat == "Steals":   # Prediction for Steals
            predicted_value = self._predict_steals(self.points[-1], self.assists[-1], self.rebounds[-1], self.blocks[-1])
        elif stat == "Blocks":   # Prediction for Blocks
            predicted_value = self._predict_blocks(self.points[-1], self.assists[-1], self.rebounds[-1], self.steals[-1])
        else:
            raise ValueError("Invalid stat choice.")

        likelihood = self._evaluate_likelihood(predicted_value, value)

        return predicted_value, likelihood

# Streamlit UI (Updated)
# Streamlit UI (Updated)
st.title("SportyPredict")

player = st.selectbox("Select a Player", ["LeBron James", "Stephen Curry", "Nikola Jokic"])
stat = st.selectbox("Select a Statistic", ["Points", "Assists", "Rebounds", "Steals", "Blocks"])  # Added "Steals" and "Blocks" options
value = st.number_input("Enter the Value")

# Get total number of games for selected player from MongoDB
player_first = player.split()[0]
mongo_db = MongoDB()
total_games = len(mongo_db.games(player_first))

# Add a slider for selecting the number of previous games, with maximum value set to total number of games
num_previous_games = st.slider("Select the number of previous games to base analysis on", min_value=1, max_value=total_games, value=10)

if st.button("Calculate"):
    games = mongo_db.games(player_first, num_previous_games)

    if not games:
        st.error("No data found for the player.")
    else:
        predictor = Calculation(games)
        predictor._extract_stats()
        predictor._prepare_feature_sets()
        predictor._train_models()

        predicted_value, likelihood = predictor.predict_stat(stat, value)

        st.write(f"Prediction: {predicted_value:.2f}")
        st.write(f"Likelihood: {likelihood}")

        # Display table for selected number of previous games
        st.subheader(f"Performance Table for Last {num_previous_games} Games")
        reversed_performance_data = {
    "Points": [game['points'] for game in reversed(games)],
    "Assists": [game['assists'] for game in reversed(games)],
    "Rebounds": [game['totReb'] for game in reversed(games)],
    "Steals": [game['steals'] for game in reversed(games)],   # Adding stealing stats
    "Blocks": [game['blocks'] for game in reversed(games)]   # Adding blocking stats
}

    st.table(reversed_performance_data)


