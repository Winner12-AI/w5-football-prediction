"""
Full W-5 Pipeline Example

This script demonstrates the complete W-5 framework including:
1. Baseline ML prediction
2. AI Consensus mechanism
3. Meta-learning fusion

Note: Requires LLM API keys to be configured.
"""

import sys
sys.path.append('..')

import os
from dotenv import load_dotenv
from src.models.baseline import SimpleELOPredictor
from src.consensus.debate import ConsensusEngine
from src.data.loader import load_sample_data

# Load environment variables
load_dotenv()


def check_api_keys():
    """Check if required API keys are configured."""
    required_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
    missing = [key for key in required_keys if not os.getenv(key)]
    
    if missing:
        print("Warning: Missing API keys:", ', '.join(missing))
        print("The consensus mechanism will use mock responses.")
        print("To use real LLMs, configure keys in .env file.")
        return False
    return True


def main():
    print("="*70)
    print("W-5 Framework - Full Pipeline Example")
    print("="*70)
    print()
    
    # Check API configuration
    has_api_keys = check_api_keys()
    print()
    
    # Load sample match data
    print("Loading sample match data...")
    match_data = load_sample_data('demo')
    
    print(f"\nMatch: {match_data['home_team']} vs {match_data['away_team']}")
    print()
    
    # Step 1: Baseline Prediction
    print("="*70)
    print("STEP 1: Baseline ML Prediction")
    print("="*70)
    print()
    
    elo_predictor = SimpleELOPredictor()
    home_elo = match_data['quantitative_features']['home_elo']
    away_elo = match_data['quantitative_features']['away_elo']
    
    home_prob, draw_prob, away_prob = elo_predictor.predict_proba(
        home_elo, away_elo
    )
    
    baseline_prediction = {
        'home_win': home_prob,
        'draw': draw_prob,
        'away_win': away_prob
    }
    
    print(f"Baseline Prediction:")
    print(f"  Home Win: {home_prob:.1%}")
    print(f"  Draw:     {draw_prob:.1%}")
    print(f"  Away Win: {away_prob:.1%}")
    print()
    
    # Step 2: AI Consensus
    print("="*70)
    print("STEP 2: AI Consensus Mechanism")
    print("="*70)
    print()
    
    # Configure agents (using 3 agents for faster demo)
    agent_configs = [
        {'persona_type': 'statistician', 'llm_provider': 'openai', 'model_name': 'gpt-4'},
        {'persona_type': 'tactician', 'llm_provider': 'anthropic', 'model_name': 'claude-3-opus'},
        {'persona_type': 'sentiment_analyst', 'llm_provider': 'google', 'model_name': 'gemini-pro'}
    ]
    
    try:
        consensus_engine = ConsensusEngine(
            agent_configs=agent_configs,
            debate_rounds=2,
            min_agents=3
        )
        
        consensus_result = consensus_engine.run_consensus(
            match_data,
            baseline_prediction
        )
        
        print("\nConsensus Result:")
        consensus_pred = consensus_result['consensus_prediction']
        print(f"  Home Win: {consensus_pred['home_win']:.1%}")
        print(f"  Draw:     {consensus_pred['draw']:.1%}")
        print(f"  Away Win: {consensus_pred['away_win']:.1%}")
        print(f"\nOverall Confidence: {consensus_result['confidence']:.1%}")
        print(f"Agreement Score: {consensus_result['agreement_score']:.2f}")
        print()
        
        print("Debate Summary:")
        print("-"*70)
        print(consensus_result['debate_summary'])
        print()
        
    except Exception as e:
        print(f"Error running consensus: {e}")
        print("Using baseline prediction only.")
        consensus_result = None
    
    # Step 3: Meta-Learning Fusion
    print("="*70)
    print("STEP 3: Meta-Learning Fusion")
    print("="*70)
    print()
    
    if consensus_result:
        # In production, this would use a trained neural network
        # For demo, we use a simple weighted average
        baseline_weight = 0.3
        consensus_weight = 0.7
        
        final_prediction = {
            'home_win': (
                baseline_weight * baseline_prediction['home_win'] +
                consensus_weight * consensus_pred['home_win']
            ),
            'draw': (
                baseline_weight * baseline_prediction['draw'] +
                consensus_weight * consensus_pred['draw']
            ),
            'away_win': (
                baseline_weight * baseline_prediction['away_win'] +
                consensus_weight * consensus_pred['away_win']
            )
        }
    else:
        final_prediction = baseline_prediction
    
    print("Final W-5 Prediction:")
    print(f"  Home Win: {final_prediction['home_win']:.1%}")
    print(f"  Draw:     {final_prediction['draw']:.1%}")
    print(f"  Away Win: {final_prediction['away_win']:.1%}")
    print()
    
    # Determine winner
    probs = [
        ('Home Win', final_prediction['home_win']),
        ('Draw', final_prediction['draw']),
        ('Away Win', final_prediction['away_win'])
    ]
    predicted_outcome = max(probs, key=lambda x: x[1])
    
    print(f"Predicted Outcome: {predicted_outcome[0]} ({predicted_outcome[1]:.1%})")
    print()
    
    # Summary
    print("="*70)
    print("PIPELINE SUMMARY")
    print("="*70)
    print()
    print("The W-5 framework successfully combined:")
    print("  ✓ Quantitative baseline prediction (ELO-based)")
    if consensus_result:
        print("  ✓ Multi-agent AI consensus (3 LLM agents)")
        print("  ✓ Meta-learning fusion layer")
    else:
        print("  ✗ AI consensus (API keys not configured)")
        print("  ✗ Meta-learning fusion (requires consensus)")
    print()
    print("For production use with full accuracy, visit: https://winner12.com")
    print()
    print("="*70)


if __name__ == '__main__':
    main()

