import { useState } from 'react';
import { ChevronDown, Trophy, TrendingUp, User } from 'lucide-react';

export default function TennisPredictor() {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Sample tennis players - you can replace with your actual data
  const players = [
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

  const handlePredict = () => {
    if (!player1 || !player2 || player1 === player2) return;
    
    setLoading(true);
    
    // Simulate API call delay
    setTimeout(() => {
      // Mock prediction logic - replace with your actual model
      const confidence = Math.random() * 30 + 55; // 55-85% confidence
      const winner = Math.random() > 0.5 ? player1 : player2;
      
      setPrediction({
        winner,
        confidence: confidence.toFixed(1),
        player1Prob: winner === player1 ? confidence : 100 - confidence,
        player2Prob: winner === player2 ? confidence : 100 - confidence
      });
      setLoading(false);
    }, 1500);
  };

  const resetPrediction = () => {
    setPlayer1('');
    setPlayer2('');
    setPrediction(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <Trophy className="h-8 w-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Tennis Match Predictor</h1>
          </div>
          <p className="text-gray-600 mt-1">AI-powered tennis match outcome prediction</p>
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
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none text-gray-900"
                >
                  <option value="">Select a player</option>
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
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none text-gray-900"
                >
                  <option value="">Select a player</option>
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
              disabled={!player1 || !player2 || player1 === player2 || loading}
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
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="flex items-center gap-3 mb-6">
            <User className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">About the Author</h2>
          </div>

          <div className="prose max-w-none text-gray-600">
            <p className="mb-4">
              This tennis match prediction model was developed using advanced machine learning techniques, 
              specifically a decision tree algorithm trained on comprehensive tennis match data including 
              player statistics, head-to-head records, surface preferences, and recent form.
            </p>
            
            <p className="mb-4">
              The model analyzes multiple factors such as:
            </p>
            
            <ul className="list-disc pl-6 mb-4 space-y-1">
              <li>Historical match performance and win rates</li>
              <li>Head-to-head matchup statistics</li>
              <li>Recent form and momentum indicators</li>
              <li>Surface-specific performance metrics</li>
              <li>Physical and mental conditioning factors</li>
            </ul>

            <p className="mb-4">
              Built with a passion for both tennis and data science, this tool aims to provide tennis 
              enthusiasts with data-driven insights into match outcomes. While no prediction model can 
              be 100% accurate due to the inherent unpredictability in sports, this system strives to 
              offer the most informed predictions possible based on available data.
            </p>

            <div className="bg-gray-50 rounded-lg p-4 mt-6">
              <p className="text-sm text-gray-600 italic">
                "Tennis is a game of margins, and data helps us understand those margins better." 
                - Model Developer
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>© 2025 Tennis Match Predictor. Built with React and Tailwind CSS.</p>
            <p className="mt-1">Predictions are for entertainment purposes and should not be used for betting.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}