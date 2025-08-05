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

# Global variables to store loaded model and data
model = None
df = None
player_name_map = None

def build_player_name_map():
    """
    Build player name mapping - you'll need to implement this
    or copy from your tree/random_forest.py file
    """
    # For now, return a basic mapping - replace with your actual implementation
    # You might need to load this from a file or recreate the logic here
    try:
        # Try to load from a saved file if you have one
        # Or recreate the mapping logic from your original code
        
        # Placeholder - replace with your actual player mapping
        return {
            'Novak Djokovic': 1,
            'Carlos Alcaraz': 2,
            'Jannik Sinner': 3,
            'Daniil Medvedev': 4,
            'Alexander Zverev': 5,
            'Andrey Rublev': 6,
            'Stefanos Tsitsipas': 7,
            'Holger Rune': 8,
            'Casper Ruud': 9,
            'Taylor Fritz': 10,
            'Grigor Dimitrov': 11,
            'Tommy Paul': 12,
            'Alex de Minaur': 13,
            'Hubert Hurkacz': 14,
            # Add all your players here
        }
    except Exception as e:
        print(f"Error building player name map: {e}")
        return {}

def load_model_and_data():
    """Load the model and data once when the server starts"""
    global model, df, player_name_map
    
    try:
        # Load the model from Hugging Face
        print("Loading model from Hugging Face...")
        model_path = hf_hub_download(
            repo_id='parthdiwane/sportly-random-forest',
            filename='rf1_bin_model.pkl'
        )
        model = joblib.load(model_path)
        print("Model loaded successfully!")
        
        # For deployment, you'll need to either:
        # 1. Upload your CSV to Hugging Face and download it
        # 2. Include it in your deployment
        # 3. Use a database
        
        # Option 1: Try to download CSV from Hugging Face (if you upload it)
        try:
            csv_path = hf_hub_download(
                repo_id='parthdiwane/sportly-random-forest',
                filename='singles_net_stats2.csv'
            )
            df = pd.read_csv(csv_path)
            print("CSV loaded from Hugging Face!")
        except:
            # Option 2: Create sample data for now
            print("Using sample data - replace with actual data")
            df = pd.DataFrame({
                'p1': [1, 2, 3, 4, 5] * 100,  # Sample data
                # Add your actual feature columns here
            })
        
        # Build player name map
        player_name_map = build_player_name_map()
        print(f"Player name map loaded with {len(player_name_map)} players")
        
        return True
        
    except Exception as e:
        print(f"Error loading model and data: {e}")
        return False

def find_winner(p1: str, p2: str):
    """Find the winner between two players using the trained model"""
    try:
        if not hasattr(model, 'feature_names_in_'):
            return None, "Model not properly loaded"
            
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
    return jsonify({
        'status': 'healthy', 
        'model_loaded': model is not None,
        'players_loaded': len(player_name_map) if player_name_map else 0
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Tennis Predictor API is running!',
        'endpoints': ['/predict', '/players', '/health']
    })

if __name__ == '__main__':
    print("Loading model and data...")
    if load_model_and_data():
        print("Starting Flask server...")
        port = int(os.environ.get('PORT', 5001))
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        print("Failed to load model and data. Exiting.")