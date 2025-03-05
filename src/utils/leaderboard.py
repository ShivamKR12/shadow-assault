import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self):
        self.leaderboard_file = 'leaderboard.json'
        self.max_entries = 10
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, 'r') as f:
                    return json.load(f)
            return []
        except:
            return []

    def save_scores(self):
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

    def add_score(self, player_name, score):
        entry = {
            'player': player_name,
            'score': score,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        if len(self.scores) > self.max_entries:
            self.scores = self.scores[:self.max_entries]
            
        self.save_scores()

    def get_top_scores(self, limit=10):
        return self.scores[:limit]
