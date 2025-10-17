"""
Data Loading and Processing Utilities

This module provides utilities for loading and preprocessing football match data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class MatchDataLoader:
    """
    Loader for football match data.
    
    Handles loading, validation, and basic preprocessing of match datasets.
    """
    
    REQUIRED_COLUMNS = [
        'match_id', 'home_team', 'away_team', 'outcome'
    ]
    
    OUTCOME_MAPPING = {
        'H': 0,  # Home win
        'D': 1,  # Draw
        'A': 2,  # Away win
        0: 0,
        1: 1,
        2: 2
    }
    
    def __init__(self, data_dir: str = 'data/sample'):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir)
    
    def load_matches(
        self,
        filename: str,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Load match data from CSV file.
        
        Args:
            filename: Name of the CSV file
            validate: Whether to validate data structure
            
        Returns:
            DataFrame with match data
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        df = pd.read_csv(filepath)
        
        if validate:
            self._validate_data(df)
        
        # Normalize outcome column
        if 'outcome' in df.columns:
            df['outcome'] = df['outcome'].map(
                lambda x: self.OUTCOME_MAPPING.get(x, x)
            )
        
        return df
    
    def _validate_data(self, df: pd.DataFrame):
        """Validate that required columns are present."""
        missing = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def split_features_target(
        self,
        df: pd.DataFrame,
        feature_cols: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Split dataframe into features and target.
        
        Args:
            df: Input dataframe
            feature_cols: List of feature column names (if None, auto-detect)
            
        Returns:
            Tuple of (features_df, target_array)
        """
        if feature_cols is None:
            # Auto-detect: exclude ID, team names, and outcome
            exclude = ['match_id', 'home_team', 'away_team', 'outcome', 'date']
            feature_cols = [c for c in df.columns if c not in exclude]
        
        X = df[feature_cols]
        y = df['outcome'].values if 'outcome' in df.columns else None
        
        return X, y
    
    def create_train_test_split(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2,
        time_based: bool = True,
        date_column: str = 'date'
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Create train/test split.
        
        Args:
            df: Input dataframe
            test_size: Proportion for test set
            time_based: If True, use temporal split (no shuffle)
            date_column: Name of date column for temporal split
            
        Returns:
            Tuple of (train_df, test_df)
        """
        if time_based and date_column in df.columns:
            # Sort by date and split
            df = df.sort_values(date_column)
            split_idx = int(len(df) * (1 - test_size))
            train_df = df.iloc[:split_idx]
            test_df = df.iloc[split_idx:]
        else:
            # Random split
            from sklearn.model_selection import train_test_split
            train_df, test_df = train_test_split(
                df, test_size=test_size, random_state=42
            )
        
        return train_df, test_df


class FeatureEngineering:
    """
    Feature engineering utilities for match prediction.
    
    Provides methods to compute derived features from raw match data.
    """
    
    @staticmethod
    def compute_form(
        df: pd.DataFrame,
        team_col: str,
        outcome_col: str,
        window: int = 5
    ) -> pd.Series:
        """
        Compute recent form (win rate over last N matches).
        
        Args:
            df: Match dataframe
            team_col: Column name for team
            outcome_col: Column name for outcome
            window: Number of recent matches to consider
            
        Returns:
            Series with form scores
        """
        # This is a simplified version
        # Production implementation would handle home/away separately
        form = []
        
        for idx, row in df.iterrows():
            team = row[team_col]
            
            # Get recent matches for this team
            recent = df[
                (df[team_col] == team) & (df.index < idx)
            ].tail(window)
            
            if len(recent) == 0:
                form.append(0.5)  # Default
            else:
                wins = (recent[outcome_col] == 0).sum()  # Assuming 0 = win
                form.append(wins / len(recent))
        
        return pd.Series(form, index=df.index)
    
    @staticmethod
    def compute_head_to_head(
        df: pd.DataFrame,
        home_team: str,
        away_team: str,
        max_matches: int = 10
    ) -> Dict[str, float]:
        """
        Compute head-to-head statistics.
        
        Args:
            df: Historical match dataframe
            home_team: Home team name
            away_team: Away team name
            max_matches: Maximum number of historical matches to consider
            
        Returns:
            Dictionary with h2h statistics
        """
        # Find historical matches between these teams
        h2h = df[
            ((df['home_team'] == home_team) & (df['away_team'] == away_team)) |
            ((df['home_team'] == away_team) & (df['away_team'] == home_team))
        ].tail(max_matches)
        
        if len(h2h) == 0:
            return {
                'h2h_matches': 0,
                'h2h_home_wins': 0.33,
                'h2h_draws': 0.33,
                'h2h_away_wins': 0.33
            }
        
        # Count outcomes
        home_wins = len(h2h[
            (h2h['home_team'] == home_team) & (h2h['outcome'] == 0)
        ])
        away_wins = len(h2h[
            (h2h['away_team'] == home_team) & (h2h['outcome'] == 2)
        ])
        draws = len(h2h[h2h['outcome'] == 1])
        
        total = len(h2h)
        
        return {
            'h2h_matches': total,
            'h2h_home_wins': home_wins / total,
            'h2h_draws': draws / total,
            'h2h_away_wins': away_wins / total
        }
    
    @staticmethod
    def compute_goal_statistics(
        df: pd.DataFrame,
        team: str,
        window: int = 10
    ) -> Dict[str, float]:
        """
        Compute goal scoring and conceding statistics.
        
        Args:
            df: Match dataframe with goal columns
            team: Team name
            window: Number of recent matches
            
        Returns:
            Dictionary with goal statistics
        """
        # Get recent matches
        recent = df[
            (df['home_team'] == team) | (df['away_team'] == team)
        ].tail(window)
        
        if len(recent) == 0:
            return {
                'avg_goals_scored': 1.5,
                'avg_goals_conceded': 1.5,
                'goal_difference': 0.0
            }
        
        # Calculate goals (assuming columns exist)
        goals_scored = []
        goals_conceded = []
        
        for _, row in recent.iterrows():
            if row['home_team'] == team:
                goals_scored.append(row.get('home_goals', 0))
                goals_conceded.append(row.get('away_goals', 0))
            else:
                goals_scored.append(row.get('away_goals', 0))
                goals_conceded.append(row.get('home_goals', 0))
        
        return {
            'avg_goals_scored': np.mean(goals_scored) if goals_scored else 1.5,
            'avg_goals_conceded': np.mean(goals_conceded) if goals_conceded else 1.5,
            'goal_difference': np.mean(goals_scored) - np.mean(goals_conceded)
        }


def load_sample_data(sample_name: str = 'demo') -> Dict[str, any]:
    """
    Convenience function to load sample data for examples.
    
    Args:
        sample_name: Name of the sample dataset
        
    Returns:
        Dictionary with match context
    """
    # This would load from actual files in production
    # For now, return a mock example
    return {
        'home_team': 'Team_A001',
        'away_team': 'Team_B042',
        'quantitative_features': {
            'home_elo': 1650,
            'away_elo': 1580,
            'home_form_l5': 0.6,
            'away_form_l5': 0.4,
            'h2h_home_wins': 0.5,
            'h2h_draws': 0.3,
            'h2h_away_wins': 0.2,
            'home_avg_goals': 1.8,
            'away_avg_goals': 1.4
        },
        'qualitative_context': """
Recent news: Home team has won 3 of last 5 matches. 
Away team's star striker is returning from injury.
Weather forecast: Clear conditions, no significant impact expected.
Market sentiment: Slight favor towards home team.
        """.strip()
    }

