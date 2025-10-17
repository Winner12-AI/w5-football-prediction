"""
Baseline ML Models for W-5 Framework

This module implements the quantitative baseline prediction layer using
traditional machine learning models (XGBoost, LightGBM).

Note: This is a research implementation. Production models use proprietary
optimizations and larger training datasets.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb


class BaselinePredictor:
    """
    Baseline predictor using ensemble of XGBoost and LightGBM models.
    
    This class provides the quantitative foundation for the W-5 framework,
    processing structured features to generate initial probability estimates.
    """
    
    def __init__(
        self,
        model_type: str = 'ensemble',
        random_state: int = 42
    ):
        """
        Initialize the baseline predictor.
        
        Args:
            model_type: Type of model ('xgboost', 'lightgbm', or 'ensemble')
            random_state: Random seed for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_names = None
        self.is_trained = False
        
    def _init_xgboost(self) -> xgb.XGBClassifier:
        """Initialize XGBoost model with research parameters."""
        return xgb.XGBClassifier(
            max_depth=7,
            learning_rate=0.05,
            n_estimators=500,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='multi:softprob',
            num_class=3,
            random_state=self.random_state,
            eval_metric='mlogloss',
            tree_method='hist'
        )
    
    def _init_lightgbm(self) -> lgb.LGBMClassifier:
        """Initialize LightGBM model with research parameters."""
        return lgb.LGBMClassifier(
            num_leaves=63,
            learning_rate=0.05,
            n_estimators=500,
            feature_fraction=0.8,
            bagging_fraction=0.8,
            bagging_freq=5,
            objective='multiclass',
            num_class=3,
            random_state=self.random_state,
            verbose=-1
        )
    
    def train(
        self,
        X: pd.DataFrame,
        y: np.ndarray,
        validation_split: float = 0.2
    ) -> Dict[str, float]:
        """
        Train the baseline models.
        
        Args:
            X: Feature dataframe
            y: Target labels (0: Home Win, 1: Draw, 2: Away Win)
            validation_split: Proportion of data for validation
            
        Returns:
            Dictionary of training metrics
        """
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=self.random_state
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        metrics = {}
        
        # Train XGBoost
        if self.model_type in ['xgboost', 'ensemble']:
            print("Training XGBoost model...")
            self.models['xgboost'] = self._init_xgboost()
            self.models['xgboost'].fit(
                X_train_scaled, y_train,
                eval_set=[(X_val_scaled, y_val)],
                verbose=False
            )
            xgb_acc = self.models['xgboost'].score(X_val_scaled, y_val)
            metrics['xgboost_accuracy'] = xgb_acc
            print(f"XGBoost validation accuracy: {xgb_acc:.4f}")
        
        # Train LightGBM
        if self.model_type in ['lightgbm', 'ensemble']:
            print("Training LightGBM model...")
            self.models['lightgbm'] = self._init_lightgbm()
            self.models['lightgbm'].fit(
                X_train_scaled, y_train,
                eval_set=[(X_val_scaled, y_val)],
                callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
            )
            lgb_acc = self.models['lightgbm'].score(X_val_scaled, y_val)
            metrics['lightgbm_accuracy'] = lgb_acc
            print(f"LightGBM validation accuracy: {lgb_acc:.4f}")
        
        self.is_trained = True
        return metrics
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict outcome probabilities.
        
        Args:
            X: Feature dataframe
            
        Returns:
            Array of shape (n_samples, 3) with probabilities for
            [Home Win, Draw, Away Win]
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from all models
        predictions = []
        
        if 'xgboost' in self.models:
            predictions.append(self.models['xgboost'].predict_proba(X_scaled))
        
        if 'lightgbm' in self.models:
            predictions.append(self.models['lightgbm'].predict_proba(X_scaled))
        
        # Ensemble: average predictions
        if len(predictions) > 1:
            return np.mean(predictions, axis=0)
        else:
            return predictions[0]
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict outcome classes.
        
        Args:
            X: Feature dataframe
            
        Returns:
            Array of predicted classes (0: Home Win, 1: Draw, 2: Away Win)
        """
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from trained models.
        
        Returns:
            DataFrame with feature names and importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        importance_dict = {}
        
        if 'xgboost' in self.models:
            importance_dict['xgboost'] = self.models['xgboost'].feature_importances_
        
        if 'lightgbm' in self.models:
            importance_dict['lightgbm'] = self.models['lightgbm'].feature_importances_
        
        # Average importance across models
        avg_importance = np.mean(list(importance_dict.values()), axis=0)
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': avg_importance
        }).sort_values('importance', ascending=False)
        
        return importance_df


class SimpleELOPredictor:
    """
    Simple ELO-based predictor for comparison baseline.
    
    This implements a basic ELO rating system as described in the paper,
    serving as a traditional statistical benchmark.
    """
    
    def __init__(self, k_factor: float = 32, home_advantage: float = 100):
        """
        Initialize ELO predictor.
        
        Args:
            k_factor: ELO K-factor for rating updates
            home_advantage: Home advantage in ELO points
        """
        self.k_factor = k_factor
        self.home_advantage = home_advantage
        self.ratings = {}
        
    def _expected_score(self, rating_a: float, rating_b: float) -> float:
        """Calculate expected score for team A against team B."""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    def predict_proba(
        self,
        home_rating: float,
        away_rating: float
    ) -> Tuple[float, float, float]:
        """
        Predict match outcome probabilities based on ELO ratings.
        
        Args:
            home_rating: Home team ELO rating
            away_rating: Away team ELO rating
            
        Returns:
            Tuple of (home_win_prob, draw_prob, away_win_prob)
        """
        # Adjust for home advantage
        adjusted_home = home_rating + self.home_advantage
        
        # Calculate expected score
        home_expected = self._expected_score(adjusted_home, away_rating)
        
        # Simple probability model
        # (Note: This is simplified; production models use more sophisticated approaches)
        draw_prob = 0.25  # Base draw probability
        home_win_prob = home_expected * (1 - draw_prob)
        away_win_prob = (1 - home_expected) * (1 - draw_prob)
        
        # Normalize to sum to 1
        total = home_win_prob + draw_prob + away_win_prob
        return (
            home_win_prob / total,
            draw_prob / total,
            away_win_prob / total
        )
    
    def update_ratings(
        self,
        home_team: str,
        away_team: str,
        result: int
    ):
        """
        Update ELO ratings after a match.
        
        Args:
            home_team: Home team identifier
            away_team: Away team identifier
            result: Match result (0: Home Win, 1: Draw, 2: Away Win)
        """
        # Initialize ratings if not present
        if home_team not in self.ratings:
            self.ratings[home_team] = 1500
        if away_team not in self.ratings:
            self.ratings[away_team] = 1500
        
        # Get current ratings
        home_rating = self.ratings[home_team]
        away_rating = self.ratings[away_team]
        
        # Calculate expected scores
        home_expected = self._expected_score(
            home_rating + self.home_advantage,
            away_rating
        )
        away_expected = 1 - home_expected
        
        # Determine actual scores
        if result == 0:  # Home win
            home_actual, away_actual = 1, 0
        elif result == 1:  # Draw
            home_actual, away_actual = 0.5, 0.5
        else:  # Away win
            home_actual, away_actual = 0, 1
        
        # Update ratings
        self.ratings[home_team] += self.k_factor * (home_actual - home_expected)
        self.ratings[away_team] += self.k_factor * (away_actual - away_expected)

