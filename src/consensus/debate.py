"""
AI Consensus Debate Orchestration

This module implements the debate and synthesis process where multiple
AI agents collaborate to reach a consensus prediction.
"""

from typing import Dict, List, Any, Optional
import numpy as np
from .agent import LLMAgent


class ConsensusEngine:
    """
    Orchestrates the AI Consensus Mechanism.
    
    This engine manages multiple LLM agents, facilitates their debate,
    and synthesizes their diverse perspectives into a robust consensus.
    """
    
    def __init__(
        self,
        agent_configs: Optional[List[Dict[str, Any]]] = None,
        debate_rounds: int = 2,
        min_agents: int = 3
    ):
        """
        Initialize the consensus engine.
        
        Args:
            agent_configs: List of agent configurations
            debate_rounds: Number of debate iterations
            min_agents: Minimum number of agents required
        """
        self.debate_rounds = debate_rounds
        self.min_agents = min_agents
        self.agents = []
        
        # Initialize agents
        if agent_configs is None:
            # Default configuration with 5 agents
            agent_configs = [
                {'persona_type': 'statistician', 'llm_provider': 'openai', 'model_name': 'gpt-4'},
                {'persona_type': 'tactician', 'llm_provider': 'anthropic', 'model_name': 'claude-3-opus'},
                {'persona_type': 'sentiment_analyst', 'llm_provider': 'google', 'model_name': 'gemini-pro'},
                {'persona_type': 'news_analyst', 'llm_provider': 'openai', 'model_name': 'gpt-4'},
                {'persona_type': 'risk_assessor', 'llm_provider': 'anthropic', 'model_name': 'claude-3-opus'}
            ]
        
        for config in agent_configs:
            try:
                agent = LLMAgent(**config)
                self.agents.append(agent)
            except Exception as e:
                print(f"Warning: Failed to initialize agent {config}: {e}")
        
        if len(self.agents) < self.min_agents:
            raise ValueError(f"Need at least {self.min_agents} agents, got {len(self.agents)}")
    
    def run_consensus(
        self,
        match_context: Dict[str, Any],
        baseline_prediction: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Run the full consensus process.
        
        Args:
            match_context: Match information and context
            baseline_prediction: Optional baseline ML prediction
            
        Returns:
            Consensus result with:
                - consensus_prediction: Final probability distribution
                - confidence: Overall confidence score
                - agent_analyses: Individual agent outputs
                - debate_summary: Summary of key agreements/disagreements
        """
        print(f"\n{'='*60}")
        print(f"Starting AI Consensus Process")
        print(f"Agents: {len(self.agents)} | Rounds: {self.debate_rounds}")
        print(f"{'='*60}\n")
        
        # Round 1: Initial independent analysis
        print("Round 1: Independent Analysis")
        print("-" * 60)
        initial_analyses = self._round_1_analysis(match_context, baseline_prediction)
        
        # Round 2+: Debate and revision
        final_analyses = initial_analyses
        for round_num in range(2, self.debate_rounds + 1):
            print(f"\nRound {round_num}: Debate and Revision")
            print("-" * 60)
            final_analyses = self._debate_round(
                match_context,
                baseline_prediction,
                final_analyses
            )
        
        # Synthesize consensus
        print("\nSynthesizing Consensus...")
        print("-" * 60)
        consensus = self._synthesize_consensus(final_analyses)
        
        print(f"\n{'='*60}")
        print(f"Consensus Complete")
        print(f"{'='*60}\n")
        
        return {
            'consensus_prediction': consensus['prediction'],
            'confidence': consensus['confidence'],
            'agent_analyses': final_analyses,
            'debate_summary': consensus['summary'],
            'agreement_score': consensus['agreement_score']
        }
    
    def _round_1_analysis(
        self,
        match_context: Dict[str, Any],
        baseline_prediction: Optional[Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """First round: Each agent analyzes independently."""
        analyses = []
        
        for i, agent in enumerate(self.agents):
            print(f"  Agent {i+1}/{len(self.agents)}: {agent.persona.name}")
            analysis = agent.analyze(match_context, baseline_prediction)
            analyses.append(analysis)
            
            # Print summary
            pred = analysis['prediction']
            print(f"    Prediction: H:{pred['home_win']:.2%} D:{pred['draw']:.2%} A:{pred['away_win']:.2%}")
            print(f"    Confidence: {analysis['confidence']:.2%}")
        
        return analyses
    
    def _debate_round(
        self,
        match_context: Dict[str, Any],
        baseline_prediction: Optional[Dict[str, float]],
        previous_analyses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Subsequent rounds: Agents review peers' analyses and revise.
        
        In production, this would involve more sophisticated prompting
        where agents explicitly respond to each other's reasoning.
        """
        # Summarize previous round for context
        peer_summary = self._summarize_peer_analyses(previous_analyses)
        
        # Add peer summary to context
        enhanced_context = match_context.copy()
        enhanced_context['peer_analyses'] = peer_summary
        
        # Each agent revises their analysis
        revised_analyses = []
        for i, agent in enumerate(self.agents):
            print(f"  Agent {i+1}: {agent.persona.name} (revising)")
            
            # In a full implementation, we'd pass peer analyses to the agent
            # For this research version, we simulate revision by slight adjustment
            analysis = agent.analyze(enhanced_context, baseline_prediction)
            
            # Blend with previous analysis (simulating consideration of peers)
            prev = previous_analyses[i]['prediction']
            curr = analysis['prediction']
            
            # Weighted average: 70% new, 30% previous (moving toward consensus)
            blended_pred = {
                'home_win': 0.7 * curr['home_win'] + 0.3 * prev['home_win'],
                'draw': 0.7 * curr['draw'] + 0.3 * prev['draw'],
                'away_win': 0.7 * curr['away_win'] + 0.3 * prev['away_win']
            }
            
            analysis['prediction'] = blended_pred
            revised_analyses.append(analysis)
            
            print(f"    Revised: H:{blended_pred['home_win']:.2%} D:{blended_pred['draw']:.2%} A:{blended_pred['away_win']:.2%}")
        
        return revised_analyses
    
    def _summarize_peer_analyses(
        self,
        analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Summarize peer analyses for context."""
        predictions = [a['prediction'] for a in analyses]
        
        avg_pred = {
            'home_win': np.mean([p['home_win'] for p in predictions]),
            'draw': np.mean([p['draw'] for p in predictions]),
            'away_win': np.mean([p['away_win'] for p in predictions])
        }
        
        return {
            'average_prediction': avg_pred,
            'num_agents': len(analyses),
            'key_factors': self._extract_common_factors(analyses)
        }
    
    def _extract_common_factors(
        self,
        analyses: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract factors mentioned by multiple agents."""
        from collections import Counter
        
        all_factors = []
        for analysis in analyses:
            all_factors.extend(analysis.get('key_factors', []))
        
        # Return factors mentioned by at least 2 agents
        factor_counts = Counter(all_factors)
        common = [f for f, count in factor_counts.items() if count >= 2]
        return common[:5]  # Top 5
    
    def _synthesize_consensus(
        self,
        analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesize final consensus from agent analyses.
        
        Uses weighted voting based on agent confidence and historical reliability.
        """
        # Extract predictions and confidences
        predictions = [a['prediction'] for a in analyses]
        confidences = [a['confidence'] for a in analyses]
        
        # Weighted average by confidence
        weights = np.array(confidences)
        weights = weights / weights.sum()
        
        consensus_pred = {
            'home_win': sum(w * p['home_win'] for w, p in zip(weights, predictions)),
            'draw': sum(w * p['draw'] for w, p in zip(weights, predictions)),
            'away_win': sum(w * p['away_win'] for w, p in zip(weights, predictions))
        }
        
        # Calculate agreement score (inverse of variance)
        variance = np.mean([
            np.var([p['home_win'] for p in predictions]),
            np.var([p['draw'] for p in predictions]),
            np.var([p['away_win'] for p in predictions])
        ])
        agreement_score = 1 / (1 + variance * 10)  # Normalized
        
        # Overall confidence (weighted average)
        overall_confidence = np.average(confidences, weights=weights)
        
        # Generate summary
        summary = self._generate_debate_summary(analyses, consensus_pred, agreement_score)
        
        return {
            'prediction': consensus_pred,
            'confidence': overall_confidence,
            'agreement_score': agreement_score,
            'summary': summary
        }
    
    def _generate_debate_summary(
        self,
        analyses: List[Dict[str, Any]],
        consensus: Dict[str, float],
        agreement_score: float
    ) -> str:
        """Generate human-readable summary of the debate."""
        outcome = max(consensus.items(), key=lambda x: x[1])
        outcome_name = outcome[0].replace('_', ' ').title()
        
        summary_parts = [
            f"Consensus Outcome: {outcome_name} ({outcome[1]:.1%} probability)",
            f"Agreement Level: {'High' if agreement_score > 0.7 else 'Moderate' if agreement_score > 0.5 else 'Low'} ({agreement_score:.2f})",
            f"\nAgent Perspectives:"
        ]
        
        for analysis in analyses:
            pred = analysis['prediction']
            agent_outcome = max(pred.items(), key=lambda x: x[1])
            summary_parts.append(
                f"  - {analysis['agent']}: {agent_outcome[0].replace('_', ' ').title()} "
                f"({agent_outcome[1]:.1%}, confidence: {analysis['confidence']:.1%})"
            )
        
        common_factors = self._extract_common_factors(analyses)
        if common_factors:
            summary_parts.append(f"\nKey Factors (consensus): {', '.join(common_factors)}")
        
        return "\n".join(summary_parts)

