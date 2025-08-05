from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import os
from huggingface_hub import hf_hub_download
import joblib
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Add the parent directory to the path to import from tree module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Global variables to store loaded model and data
model = None
df = None
player_name_map = None

def load_model_and_data():
    """Load the model and data once when the server starts"""
    global model, df, player_name_map
    
    try:
        # Load the model from Hugging Face
        model_path = hf_hub_download(
            repo_id='parthdiwane/sportly-random-forest',
            filename='rf1_bin_model.pkl'
        )
        model = joblib.load(model_path)
        
        # Load the CSV data
        # Adjust the path according to your project structure
        csv_path = '../stats/singles_net_stats/singles_net_stats2.csv'
        df = pd.read_csv(csv_path)
        
        # Import and build player name map
        from tree.random_forest import build_player_name_map
        player_name_map = build_player_name_map()
        
        print("Model and data loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading model and data: {e}")
        return False

def find_winner(p1: str, p2: str):
    """Find the winner between two players using the trained model"""
    try:
        trained_feature_names = model.feature_names_in_
        
        # Get player numbers from the name map
        if p1 not in player_name_map or p2 not in player_name_map:
            return None, f"One or both players not found in database"
        
        num_p1, num_p2 = player_name_map[p1], player_name_map[p2]
        
        # Get data for both players
        df1 = df[(df['p1'] == num_p1)]
        df2 = df[(df['p1'] == num_p2)]
        
        if df1.empty or df2.empty:
            return None, "Insufficient data for one or both players"
        
        # Calculate probabilities
        p_i = model.predict_proba(df1[trained_feature_names])[:,1]
        p_j = model.predict_proba(df2[trained_feature_names])[:,1]
        
        # Mean probability
        p_i = p_i.mean()
        p_j = p_j.mean()
        
        # Apply Bradley-Terry model
        bt = p_i / (p_i + p_j)
        
        # Determine winner
        if 1 - bt > bt:
            winner = p2
            winner_prob = (1 - bt) * 100
        else:
            winner = p1
            winner_prob = bt * 100
        
        return {
            'winner': winner,
            'confidence': round(winner_prob, 1),
            'player1_prob': round(bt * 100, 1),
            'player2_prob': round((1 - bt) * 100, 1)
        }, None
        
    except Exception as e:
        return None, f"Error in prediction: {str(e)}"

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to predict match winner"""
    try:
        data = request.get_json()
        
        if not data or 'player1' not in data or 'player2' not in data:
            return jsonify({'error': 'Missing player1 or player2 in request'}), 400
        
        player1 = data['player1']
        player2 = data['player2']
        
        if player1 == player2:
            return jsonify({'error': 'Cannot predict match between same player'}), 400
        
        # Make prediction
        result, error = find_winner(player1, player2)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/players', methods=['GET'])
def get_players():
    """API endpoint to get list of available players"""
    try:
        if player_name_map is None:
            return jsonify({'error': 'Player data not loaded'}), 500
        
        players = list(player_name_map.keys())
        players.sort()
        
        return jsonify({'players': players})
        
    except Exception as e:
        return jsonify({'error': f'Error getting players: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("Loading model and data...")
    if load_model_and_data():
        print("Starting Flask server on port 5001...")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("Failed to load model and data. Exiting.")