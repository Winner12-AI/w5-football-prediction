"""
AI Consensus Agent Implementation

This module implements individual LLM agents with specialized personas
for the AI Consensus Mechanism.

Note: This is a research implementation demonstrating the framework.
Production systems use optimized prompting and additional safeguards.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class AgentPersona:
    """Defines an AI agent's role and analytical focus."""
    name: str
    role: str
    focus_areas: List[str]
    system_prompt: str


class LLMAgent:
    """
    Individual LLM agent with a specific persona for match analysis.
    
    Each agent approaches the prediction task from a unique perspective,
    contributing to the diversity of the consensus mechanism.
    """
    
    # Predefined personas based on research paper
    PERSONAS = {
        'statistician': AgentPersona(
            name="The Statistician",
            role="Quantitative Data Analyst",
            focus_areas=["historical data", "statistical patterns", "numerical trends"],
            system_prompt="""You are a statistical analyst specializing in football analytics.
Your role is to analyze match predictions based primarily on quantitative data:
historical performance, head-to-head records, goal statistics, and numerical trends.
You rely on data-driven insights and statistical significance.
Provide clear probability assessments and confidence levels."""
        ),
        
        'tactician': AgentPersona(
            name="The Tactician",
            role="Tactical Analysis Expert",
            focus_areas=["formations", "playing styles", "tactical matchups"],
            system_prompt="""You are a tactical analyst with deep knowledge of football strategy.
Your role is to evaluate how team formations, playing styles, and tactical approaches
will influence the match outcome. Consider formation matchups, tactical flexibility,
and strategic advantages. Assess how tactics might override statistical expectations."""
        ),
        
        'sentiment_analyst': AgentPersona(
            name="The Sentiment Analyst",
            role="Market & Public Opinion Expert",
            focus_areas=["market sentiment", "public opinion", "betting trends"],
            system_prompt="""You are a sentiment analyst tracking market dynamics and public opinion.
Your role is to interpret betting market movements, social media sentiment, and fan
expectations. Identify when public sentiment diverges from statistical reality and
assess the wisdom of the crowd versus potential biases."""
        ),
        
        'news_analyst': AgentPersona(
            name="The News Analyst",
            role="Media & Context Specialist",
            focus_areas=["team news", "injuries", "morale", "external factors"],
            system_prompt="""You are a sports journalist analyzing contextual factors.
Your role is to evaluate team news, injury reports, player morale, managerial
pressure, and other qualitative factors that might not appear in statistics.
Consider the narrative and human elements that influence performance."""
        ),
        
        'risk_assessor': AgentPersona(
            name="The Risk Assessor",
            role="Uncertainty Quantification Expert",
            focus_areas=["uncertainty", "variance", "unpredictability"],
            system_prompt="""You are a risk analyst specializing in uncertainty quantification.
Your role is to identify sources of unpredictability, assess confidence levels,
and highlight factors that increase variance. Flag high-risk predictions and
scenarios where outcomes are particularly uncertain."""
        )
    }
    
    def __init__(
        self,
        persona_type: str,
        llm_provider: str = 'openai',
        model_name: str = 'gpt-4',
        temperature: float = 0.7
    ):
        """
        Initialize an LLM agent with a specific persona.
        
        Args:
            persona_type: Type of persona ('statistician', 'tactician', etc.)
            llm_provider: LLM provider ('openai', 'anthropic', 'google')
            model_name: Specific model to use
            temperature: Sampling temperature for generation
        """
        if persona_type not in self.PERSONAS:
            raise ValueError(f"Unknown persona: {persona_type}")
        
        self.persona = self.PERSONAS[persona_type]
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.temperature = temperature
        self._client = None
        
    def _init_client(self):
        """Initialize the LLM client based on provider."""
        if self._client is not None:
            return
        
        if self.llm_provider == 'openai':
            from openai import OpenAI
            self._client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        elif self.llm_provider == 'anthropic':
            from anthropic import Anthropic
            self._client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        elif self.llm_provider == 'google':
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self._client = genai
        else:
            raise ValueError(f"Unsupported provider: {self.llm_provider}")
    
    def analyze(
        self,
        match_context: Dict[str, Any],
        baseline_prediction: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a match and provide prediction from this agent's perspective.
        
        Args:
            match_context: Dictionary containing match information
            baseline_prediction: Optional baseline ML prediction to consider
            
        Returns:
            Dictionary containing:
                - prediction: Predicted outcome probabilities
                - confidence: Confidence score (0-1)
                - reasoning: Textual explanation
                - key_factors: List of influential factors
        """
        self._init_client()
        
        # Construct analysis prompt
        prompt = self._construct_prompt(match_context, baseline_prediction)
        
        # Get LLM response
        response = self._query_llm(prompt)
        
        # Parse and structure response
        analysis = self._parse_response(response)
        
        # Add agent metadata
        analysis['agent'] = self.persona.name
        analysis['persona_type'] = self.persona.role
        
        return analysis
    
    def _construct_prompt(
        self,
        match_context: Dict[str, Any],
        baseline_prediction: Optional[Dict[str, float]] = None
    ) -> str:
        """Construct the analysis prompt for the LLM."""
        prompt_parts = [
            f"Match Analysis Request:",
            f"Home Team: {match_context.get('home_team', 'Team A')}",
            f"Away Team: {match_context.get('away_team', 'Team B')}",
            ""
        ]
        
        # Add quantitative data if available
        if 'quantitative_features' in match_context:
            prompt_parts.append("Quantitative Data:")
            for key, value in match_context['quantitative_features'].items():
                prompt_parts.append(f"  - {key}: {value}")
            prompt_parts.append("")
        
        # Add qualitative context if available
        if 'qualitative_context' in match_context:
            prompt_parts.append("Qualitative Context:")
            prompt_parts.append(match_context['qualitative_context'])
            prompt_parts.append("")
        
        # Add baseline prediction if provided
        if baseline_prediction:
            prompt_parts.append("Baseline ML Prediction:")
            prompt_parts.append(f"  - Home Win: {baseline_prediction.get('home_win', 0):.1%}")
            prompt_parts.append(f"  - Draw: {baseline_prediction.get('draw', 0):.1%}")
            prompt_parts.append(f"  - Away Win: {baseline_prediction.get('away_win', 0):.1%}")
            prompt_parts.append("")
        
        prompt_parts.extend([
            f"Your Task (as {self.persona.name}):",
            f"Analyze this match from your perspective as a {self.persona.role}.",
            f"Focus on: {', '.join(self.persona.focus_areas)}",
            "",
            "Provide your analysis in the following JSON format:",
            "{",
            '  "home_win_probability": <float 0-1>,',
            '  "draw_probability": <float 0-1>,',
            '  "away_win_probability": <float 0-1>,',
            '  "confidence": <float 0-1>,',
            '  "reasoning": "<your detailed reasoning>",',
            '  "key_factors": ["factor1", "factor2", "factor3"]',
            "}"
        ])
        
        return "\n".join(prompt_parts)
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM and return the response."""
        try:
            if self.llm_provider == 'openai':
                response = self._client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.persona.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == 'anthropic':
                response = self._client.messages.create(
                    model=self.model_name,
                    max_tokens=1500,
                    temperature=self.temperature,
                    system=self.persona.system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif self.llm_provider == 'google':
                model = self._client.GenerativeModel(self.model_name)
                response = model.generate_content(
                    f"{self.persona.system_prompt}\n\n{prompt}",
                    generation_config={'temperature': self.temperature}
                )
                return response.text
            
        except Exception as e:
            # Fallback to mock response for demonstration
            print(f"LLM query failed: {e}. Using mock response.")
            return self._mock_response()
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured format."""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                # Validate and normalize probabilities
                probs = [
                    parsed.get('home_win_probability', 0.33),
                    parsed.get('draw_probability', 0.33),
                    parsed.get('away_win_probability', 0.33)
                ]
                total = sum(probs)
                probs = [p / total for p in probs]
                
                return {
                    'prediction': {
                        'home_win': probs[0],
                        'draw': probs[1],
                        'away_win': probs[2]
                    },
                    'confidence': parsed.get('confidence', 0.7),
                    'reasoning': parsed.get('reasoning', ''),
                    'key_factors': parsed.get('key_factors', [])
                }
        except Exception as e:
            print(f"Failed to parse response: {e}")
        
        # Fallback to default
        return {
            'prediction': {'home_win': 0.4, 'draw': 0.3, 'away_win': 0.3},
            'confidence': 0.5,
            'reasoning': 'Analysis unavailable',
            'key_factors': []
        }
    
    def _mock_response(self) -> str:
        """Generate a mock response for testing without API access."""
        import random
        
        # Generate random probabilities
        probs = [random.random() for _ in range(3)]
        total = sum(probs)
        probs = [p / total for p in probs]
        
        return json.dumps({
            'home_win_probability': probs[0],
            'draw_probability': probs[1],
            'away_win_probability': probs[2],
            'confidence': random.uniform(0.6, 0.9),
            'reasoning': f'Mock analysis from {self.persona.name}',
            'key_factors': ['Factor A', 'Factor B', 'Factor C']
        })

