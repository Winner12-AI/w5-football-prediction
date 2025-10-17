"""
Basic Prediction Example

This script demonstrates how to use the W-5 framework for a simple prediction.
"""

import sys
sys.path.append('..')

from src.models.baseline import BaselinePredictor
from src.data.loader import load_sample_data

def main():
    print("="*60)
    print("W-5 Framework - Basic Prediction Example")
    print("="*60)
    print()
    
    # Load sample match data
    print("Loading sample match data...")
    match_data = load_sample_data('demo')
    
    print(f"Match: {match_data['home_team']} vs {match_data['away_team']}")
    print()
    
    # Display quantitative features
    print("Quantitative Features:")
    for key, value in match_data['quantitative_features'].items():
        print(f"  {key}: {value}")
    print()
    
    # Display qualitative context
    print("Qualitative Context:")
    print(match_data['qualitative_context'])
    print()
    
    # Make prediction using baseline model
    print("-"*60)
    print("Step 1: Baseline ML Prediction")
    print("-"*60)
    
    # Note: In a real scenario, you would train the model first
    # For this demo, we'll use a simple ELO-based prediction
    from src.models.baseline import SimpleELOPredictor
    
    elo_predictor = SimpleELOPredictor()
    home_elo = match_data['quantitative_features']['home_elo']
    away_elo = match_data['quantitative_features']['away_elo']
    
    home_prob, draw_prob, away_prob = elo_predictor.predict_proba(
        home_elo, away_elo
    )
    
    print(f"\nBaseline Prediction (ELO-based):")
    print(f"  Home Win: {home_prob:.1%}")
    print(f"  Draw:     {draw_prob:.1%}")
    print(f"  Away Win: {away_prob:.1%}")
    print()
    
    # Determine predicted outcome
    probs = [home_prob, draw_prob, away_prob]
    outcomes = ['Home Win', 'Draw', 'Away Win']
    predicted_outcome = outcomes[probs.index(max(probs))]
    
    print(f"Predicted Outcome: {predicted_outcome}")
    print()
    
    print("-"*60)
    print("Step 2: AI Consensus (Requires API Keys)")
    print("-"*60)
    print()
    print("To run the full W-5 pipeline with AI Consensus:")
    print("1. Set up API keys in .env file")
    print("2. Run: python examples/full_pipeline.py")
    print()
    
    print("="*60)
    print("Example Complete")
    print("="*60)


if __name__ == '__main__':
    main()

