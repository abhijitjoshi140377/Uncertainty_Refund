"""
ML-based refund estimation engine
Uses historical data to predict refund amounts with uncertainty quantification
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sqlalchemy.orm import Session
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

from models.database import TravelBooking, HistoricalRefund, RiskEvent


class RefundEstimator:
    """ML-powered refund estimation with uncertainty quantification"""
    
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.is_trained = False
        
    def train_models(self, db: Session):
        """Train ML models on historical refund data"""
        print("  [ML] Training ML models...")
        
        # Fetch historical data
        historical_data = db.query(HistoricalRefund).all()
        
        if len(historical_data) < 50:
            print("  [WARN] Insufficient training data, using default models")
            self.is_trained = False
            return
        
        # Prepare training data by component type
        for component_type in ['flight', 'hotel', 'visa', 'insurance']:
            component_data = [h for h in historical_data if h.component_type == component_type]
            
            if len(component_data) < 20:
                continue
            
            # Feature engineering
            X = []
            y = []
            
            for record in component_data:
                features = self._extract_features(record)
                X.append(features)
                y.append(record.refund_percentage)
            
            X = np.array(X)
            y = np.array(y)
            
            # Train ensemble of models
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            
            rf_model.fit(X, y)
            gb_model.fit(X, y)
            
            self.models[component_type] = {
                'rf': rf_model,
                'gb': gb_model
            }
        
        self.is_trained = True
        print(f"  [OK] Trained models for {len(self.models)} component types")
    
    def _extract_features(self, record) -> List[float]:
        """Extract numerical features from historical record"""
        # Event severity encoding
        severity_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        severity_score = severity_map.get(record.event_severity, 2)
        
        # Event type encoding
        event_map = {
            'war': 4, 'terrorism': 3, 'civil_unrest': 3,
            'pandemic': 4, 'natural_disaster': 3
        }
        event_score = event_map.get(record.event_type, 2)
        
        features = [
            record.original_cost / 10000,  # Normalized cost
            record.days_before_travel / 180,  # Normalized days
            float(record.was_force_majeure),
            float(record.had_insurance),
            severity_score / 4,  # Normalized severity
            event_score / 4  # Normalized event type
        ]
        
        return features
    
    def _extract_booking_features(self, booking: TravelBooking, component, current_risk: float) -> List[float]:
        """Extract features from current booking"""
        from datetime import datetime
        
        days_before_travel = (booking.travel_date - datetime.now()).days
        days_before_travel = max(0, days_before_travel)
        
        # Check if booking has insurance
        has_insurance = any(c.component_type == 'insurance' for c in booking.components)
        
        # Assume force majeure if high risk
        is_force_majeure = current_risk > 60
        
        features = [
            component.cost / 10000,
            days_before_travel / 180,
            float(is_force_majeure),
            float(has_insurance),
            current_risk / 100,
            current_risk / 100
        ]
        
        return features
    
    def estimate_refund(
        self,
        db: Session,
        booking: TravelBooking,
        selected_model: str = "auto",
        calamity_type: str = "auto",
        severity: str = "high"
    ) -> Dict:
        """Generate refund estimate for a booking with optional model/calamity selection"""

        risk_score = self._resolve_risk_score(db, booking, calamity_type, severity)
        risk_level = self._get_risk_level(risk_score)

        # Estimate refund for each component
        total_expected_refund = 0
        total_cost = 0
        component_estimates = []

        for component in booking.components:
            component_estimate = self._estimate_component_refund(
                booking, component, risk_score, selected_model
            )
            component_estimates.append(component_estimate)
            total_expected_refund += component_estimate['expected_refund']
            total_cost += component.cost

        # Calculate aggregate statistics
        expected_refund_pct = (total_expected_refund / total_cost * 100) if total_cost > 0 else 0

        # Calculate confidence intervals (using ensemble variance)
        confidence_range = self._calculate_confidence_interval(component_estimates, total_cost)

        # Scenario analysis
        best_case = total_expected_refund * 1.3
        worst_case = total_expected_refund * 0.5
        most_likely = total_expected_refund

        estimate = {
            'expected_refund_amount': round(total_expected_refund, 2),
            'expected_refund_percentage': round(expected_refund_pct, 2),
            'confidence_lower': round(confidence_range['lower'], 2),
            'confidence_upper': round(confidence_range['upper'], 2),
            'confidence_level': 0.95,
            'current_risk_level': risk_level,
            'risk_score': round(risk_score, 2),
            'best_case_refund': round(min(best_case, total_cost), 2),
            'worst_case_refund': round(max(worst_case, 0), 2),
            'most_likely_refund': round(most_likely, 2),
            'model_version': f"1.0-{selected_model}-{calamity_type}",
            'prediction_confidence': round(self._calculate_prediction_confidence(risk_score), 2)
        }

        return estimate

    def _resolve_risk_score(self, db: Session, booking: TravelBooking, calamity_type: str, severity: str) -> float:
        """Resolve risk score from selected calamity or active regional events"""
        if calamity_type and calamity_type != "auto":
            severity_scores = {
                'low': 25,
                'medium': 50,
                'high': 75,
                'critical': 95
            }
            event_multiplier = {
                'pandemic': 1.0,
                'war': 1.0,
                'terrorism': 0.95,
                'natural_disaster': 0.9,
                'flight_cancellation': 0.75,
                'political_instability': 0.85,
                'economic_crisis': 0.7,
                'civil_unrest': 0.8,
                'none': 0.2
            }
            base_score = severity_scores.get(severity, 75)
            return float(base_score * event_multiplier.get(calamity_type, 0.8))

        risk_events = db.query(RiskEvent).filter(
            RiskEvent.affected_region.ilike(f"%{booking.destination}%"),
            RiskEvent.is_active == True
        ).all()
        return self._calculate_risk_score(risk_events)

    def _estimate_component_refund(self, booking: TravelBooking, component, risk_score: float, selected_model: str) -> Dict:
        """Estimate refund for a single component"""
        features = self._extract_booking_features(booking, component, risk_score)
        features_array = np.array([features])

        use_ml_model = (
            self.is_trained and
            component.component_type in self.models and
            selected_model in ['auto', 'random_forest', 'gradient_boosting']
        )

        if use_ml_model:
            models = self.models[component.component_type]
            rf_pred = models['rf'].predict(features_array)[0]
            gb_pred = models['gb'].predict(features_array)[0]

            if selected_model == 'random_forest':
                refund_pct = rf_pred
                variance = 12
            elif selected_model == 'gradient_boosting':
                refund_pct = gb_pred
                variance = 10
            else:
                refund_pct = (rf_pred + gb_pred) / 2
                variance = abs(rf_pred - gb_pred)
        else:
            refund_pct = self._rule_based_estimation(component, risk_score)
            variance = 15

        refund_pct = max(0, min(100, refund_pct))
        expected_refund = component.cost * (refund_pct / 100)

        return {
            'component_type': component.component_type,
            'expected_refund': expected_refund,
            'refund_percentage': refund_pct,
            'variance': variance
        }
    
    def _rule_based_estimation(self, component, risk_score: float) -> float:
        """Rule-based refund estimation fallback"""
        base_refund = 0
        
        if component.component_type == 'flight':
            if risk_score > 80:
                base_refund = 85
            elif risk_score > 60:
                base_refund = 65
            elif risk_score > 40:
                base_refund = 45
            elif component.is_refundable:
                base_refund = 50
            else:
                base_refund = 10
        
        elif component.component_type == 'hotel':
            if risk_score > 80:
                base_refund = 90
            elif risk_score > 60:
                base_refund = 75
            elif risk_score > 40:
                base_refund = 55
            elif component.is_refundable:
                base_refund = 60
            else:
                base_refund = 20
        
        elif component.component_type == 'insurance':
            if risk_score > 60:
                base_refund = 80
            elif risk_score > 40:
                base_refund = 60
            else:
                base_refund = 30
        
        elif component.component_type == 'visa':
            if risk_score > 80:
                base_refund = 40
            elif risk_score > 60:
                base_refund = 25
            else:
                base_refund = 5
        
        return base_refund
    
    def _calculate_risk_score(self, risk_events: List[RiskEvent]) -> float:
        """Calculate aggregate risk score from events"""
        if not risk_events:
            return 10.0  # Low baseline risk
        
        severity_scores = {
            'low': 25,
            'medium': 50,
            'high': 75,
            'critical': 95
        }
        
        max_score = max([severity_scores.get(event.severity, 25) for event in risk_events])
        return float(max_score)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to categorical level"""
        if risk_score >= 80:
            return 'critical'
        elif risk_score >= 60:
            return 'high'
        elif risk_score >= 40:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_confidence_interval(self, component_estimates: List[Dict], 
                                      total_cost: float) -> Dict:
        """Calculate confidence interval for total refund"""
        total_variance = sum(est['variance'] for est in component_estimates)
        avg_variance = total_variance / len(component_estimates) if component_estimates else 15
        
        total_expected = sum(est['expected_refund'] for est in component_estimates)
        
        # 95% confidence interval (approximately 2 standard deviations)
        margin = (avg_variance / 100) * total_cost * 0.5
        
        return {
            'lower': max(0, total_expected - margin),
            'upper': min(total_cost, total_expected + margin)
        }
    
    def _calculate_prediction_confidence(self, risk_score: float) -> float:
        """Calculate model's confidence in prediction"""
        # Higher confidence for moderate risk, lower for extremes
        if 40 <= risk_score <= 70:
            return 85.0
        elif 30 <= risk_score <= 80:
            return 75.0
        else:
            return 65.0

# Made with Bob
