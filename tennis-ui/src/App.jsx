import { useState } from 'react';
import { ChevronDown, Trophy, TrendingUp, User } from 'lucide-react';

export default function TennisPredictor() {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availablePlayers, setAvailablePlayers] = useState([]);
  const [playersLoading, setPlayersLoading] = useState(true);

  // API base URL - adjust this to match your Flask server
  const API_BASE_URL = 'http://localhost:5001';

  // Sample tennis players as fallback - you can replace with your actual data
  const fallbackPlayers = [
    'Novak Djokovic',
    'Carlos Alcaraz',
    'Jannik Sinner',
    'Daniil Medvedev',
    'Alexander Zverev',
    'Andrey Rublev',
    'Stefanos Tsitsipas',
    'Holger Rune',
    'Casper Ruud',
    'Taylor Fritz',
    'Grigor Dimitrov',
    'Tommy Paul',
    'Alex de Minaur',
    'Hubert Hurkacz',
  ].sort();

  // Fetch available players from the API
  const fetchPlayers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/players`);
      if (response.ok) {
        const data = await response.json();
        setAvailablePlayers(data.players);
      } else {
        console.warn('Failed to fetch players from API, using fallback list');
        setAvailablePlayers(fallbackPlayers);
      }
    } catch (error) {
      console.warn('Error fetching players from API, using fallback list:', error);
      setAvailablePlayers(fallbackPlayers);
    } finally {
      setPlayersLoading(false);
    }
  };

  // Load players when component mounts
  useState(() => {
    fetchPlayers();
  }, []);

  const handlePredict = async () => {
    if (!player1 || !player2 || player1 === player2) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          player1: player1,
          player2: player2
        })
      });

      if (response.ok) {
        const result = await response.json();
        setPrediction({
          winner: result.winner,
          confidence: result.confidence,
          player1Prob: result.player1_prob,
          player2Prob: result.player2_prob
        });
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to get prediction');
      }
    } catch (error) {
      console.error('Error making prediction:', error);
      setError('Failed to connect to prediction service. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetPrediction = () => {
    setPlayer1('');
    setPlayer2('');
    setPrediction(null);
    setError(null);
  };

  // Use available players or fallback
  const players = availablePlayers.length > 0 ? availablePlayers : fallbackPlayers;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <Trophy className="h-8 w-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Match Point</h1>
          </div>
          <p className="text-gray-600 mt-1">Calculated Wins. Every. Time.</p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {/* Prediction Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">Match Prediction</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Player 1 Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Player 1
              </label>
              <div className="relative">
                <select
                  value={player1}
                  onChange={(e) => setPlayer1(e.target.value)}
                  disabled={playersLoading}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none text-gray-900 disabled:bg-gray-100"
                >
                  <option value="">{playersLoading ? 'Loading players...' : 'Select a player'}</option>
                  {players.filter(p => p !== player2).map(player => (
                    <option key={player} value={player}>{player}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none" />
              </div>
            </div>

            {/* Player 2 Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Player 2
              </label>
              <div className="relative">
                <select
                  value={player2}
                  onChange={(e) => setPlayer2(e.target.value)}
                  disabled={playersLoading}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none text-gray-900 disabled:bg-gray-100"
                >
                  <option value="">{playersLoading ? 'Loading players...' : 'Select a player'}</option>
                  {players.filter(p => p !== player1).map(player => (
                    <option key={player} value={player}>{player}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-3.5 h-5 w-5 text-gray-400 pointer-events-none" />
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handlePredict}
              disabled={!player1 || !player2 || player1 === player2 || loading || playersLoading}
              className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Predicting...
                </div>
              ) : (
                'Predict Winner'
              )}
            </button>
            <button
              onClick={resetPrediction}
              className="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
            >
              Reset
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="text-red-800 font-medium">Error</div>
              <div className="text-red-600 text-sm mt-1">{error}</div>
            </div>
          )}

          {/* Prediction Results */}
          {prediction && (
            <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Results</h3>
              
              <div className="text-center mb-4">
                <div className="text-2xl font-bold text-blue-600 mb-1">
                  {prediction.winner}
                </div>
                <div className="text-gray-600">
                  Predicted Winner ({prediction.confidence}% confidence)
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-700">{player1}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-1000"
                        style={{ width: `${prediction.player1Prob}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-medium text-gray-600 w-12">
                      {prediction.player1Prob.toFixed(1)}%
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-700">{player2}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-indigo-500 h-2 rounded-full transition-all duration-1000"
                        style={{ width: `${prediction.player2Prob}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-medium text-gray-600 w-12">
                      {prediction.player2Prob.toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* About Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <User className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">About the Author/Model</h2>
          </div>

          <div className="prose max-w-none text-gray-600">
            <p className="mb-4">
              hey! im parth and im am an incoming freshman at ucsb studying ce. im interested in ai/ml, statistics, chip design (don't know much about it though), and quantum computing.
              besides academic stuff, i like going to the gym, playing badminton, watching anime (watching bleach rn), and haning out w/ friends and family. 
            </p>
            
            <p className="mb-4">
              The model analyzes multiple factors such as:
            </p>
            
            <ul className="list-disc pl-6 mb-4 space-y-1">
              <li>Historical match performance</li>
              <li>Physical factors like difference in age, height, weight, etc.</li>
              <li>Differences in number of aces hit, break poited faced/saved, elo/rank, etc</li>
              <li>Surface-specific performance metrics</li>
              <li>Other factors such as the players handedness</li>
            </ul>

            <p className="mb-4">
              Built with a passion for both tennis and data science, this tool aims to provide tennis 
              enthusiasts with data-driven insights into match outcomes. While no prediction model can 
              be 100% accurate due to the inherent unpredictability in sports, this system strives to 
              offer the most informed predictions possible based on available data.
            </p>

            <h3 className="text-lg font-semibold text-gray-900 mt-8 mb-4">How the Model Works</h3>
            
            <p className="mb-4">
              This is a decision tree model and uses a <strong className="text-red-600">random forest algorithm</strong>. It throws the players stats into its decision nodes and probabilities are outputted using a majority vote.
              But, the model does a pairwise comparison of <strong>all</strong> matches that a given player has played. So the output of a predict function isn't the real chance that player 1 beats player 2. Thus we apply a <a href="https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model" className="text-blue-600 underline hover:text-blue-700">Bradley-Terry</a> model to get the <strong>actual</strong> chance that player 1 beats player 2.
              To find the chance that player 2 beats player 1, all we do is 1 - P(player 1 wins). Then output the one with the higher probability of winning.
            </p>

            <div className="bg-gray-50 rounded-lg p-4 mt-6">
              <p className="text-sm text-gray-600 italic">
                "Pause and Ponder" 
                - 3b1b
              </p>
            </div>
          </div>
        </div>

        {/* View Code/Contact Info Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <User className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">View Code / Contact Info</h2>
          </div>
          
          <div className="flex justify-center items-center gap-6">
            <a 
              href="https://github.com/yourghubusername" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center justify-center w-12 h-12 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors group"
            >
              <svg className="w-6 h-6 text-blue-600 group-hover:text-blue-700" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>

            <a 
              href="https://linkedin.com/in/yourlinkedinusername" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center justify-center w-12 h-12 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors group"
            >
              <svg className="w-6 h-6 text-blue-600 group-hover:text-blue-700" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>

            <a 
              href="mailto:your.email@example.com" 
              className="flex items-center justify-center w-12 h-12 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors group"
            >
              <svg className="w-6 h-6 text-blue-600 group-hover:text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </a>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>© 2025 Match Point</p>
            <p className="mt-1">Predictions are for <b>entertainment purposes only</b> and should not be used for betting.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}