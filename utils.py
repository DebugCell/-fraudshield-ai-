# ============================================================================
# FraudShield AI - Utility Functions
# ============================================================================
# Data processing, model training, and analytics utilities

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                             roc_auc_score, roc_curve, auc)
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA GENERATION & LOADING
# ============================================================================

def generate_sample_data(n_samples=5000):
    """
    Generate synthetic credit card transaction data for demonstration.
    
    Args:
        n_samples (int): Number of transactions to generate
        
    Returns:
        pd.DataFrame: Synthetic transaction dataset
    """
    np.random.seed(42)
    
    # Generate features similar to credit card fraud dataset
    data = {
        'Time': np.random.uniform(0, 86400, n_samples),
        'V1': np.random.normal(-0.1, 1, n_samples),
        'V2': np.random.normal(-0.1, 1, n_samples),
        'V3': np.random.normal(0.1, 1, n_samples),
        'V4': np.random.normal(0, 1, n_samples),
        'V5': np.random.normal(-0.1, 1, n_samples),
        'V6': np.random.normal(-0.1, 1, n_samples),
        'V7': np.random.normal(0, 1, n_samples),
        'V8': np.random.normal(0, 1, n_samples),
        'V9': np.random.normal(-0.2, 1, n_samples),
        'V10': np.random.normal(0, 1, n_samples),
        'V11': np.random.normal(0, 1, n_samples),
        'V12': np.random.normal(-0.1, 1, n_samples),
        'V13': np.random.normal(0, 1, n_samples),
        'V14': np.random.normal(-0.1, 1, n_samples),
        'V15': np.random.normal(0, 1, n_samples),
        'V16': np.random.normal(0, 1, n_samples),
        'V17': np.random.normal(-0.1, 1, n_samples),
        'V18': np.random.normal(0, 1, n_samples),
        'V19': np.random.normal(0, 1, n_samples),
        'V20': np.random.normal(0, 1, n_samples),
        'V21': np.random.normal(0, 1, n_samples),
        'V22': np.random.normal(0, 1, n_samples),
        'V23': np.random.normal(0, 1, n_samples),
        'V24': np.random.normal(0, 1, n_samples),
        'V25': np.random.normal(0, 1, n_samples),
        'V26': np.random.normal(0, 1, n_samples),
        'V27': np.random.normal(0, 1, n_samples),
        'V28': np.random.normal(0, 1, n_samples),
        'Amount': np.random.exponential(100, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create class labels (mostly legitimate, some fraud)
    fraud_indices = np.random.choice(n_samples, size=int(n_samples * 0.01), replace=False)
    df['Class'] = 0
    df.loc[fraud_indices, 'Class'] = 1
    
    # Add transaction ID
    df['TransactionID'] = ['TXN' + str(i).zfill(7) for i in range(n_samples)]
    df['Date'] = pd.date_range(start='2024-01-01', periods=n_samples, freq='h')
    
    return df[['TransactionID', 'Date', 'Time', 'Amount', 'Class'] + 
              [col for col in df.columns if col.startswith('V')]]


def preprocess_data(df):
    """
    Preprocess credit card fraud data.
    
    Args:
        df (pd.DataFrame): Raw transaction data
        
    Returns:
        tuple: (X_processed, y, X_original) for model training
    """
    X = df.drop(columns=['Class', 'TransactionID', 'Date'], errors='ignore')
    y = df['Class']
    
    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    # Scale Time column with StandardScaler
    if 'Time' in X_imputed.columns:
        scaler_time = StandardScaler()
        X_imputed['Time'] = scaler_time.fit_transform(X_imputed[['Time']])
    
    # Scale Amount column with RobustScaler
    if 'Amount' in X_imputed.columns:
        scaler_amount = RobustScaler()
        X_imputed['Amount'] = scaler_amount.fit_transform(X_imputed[['Amount']])
    
    return X_imputed, y, X


def train_fraud_detection_model(X, y):
    """
    Train RandomForest model with SMOTE for class imbalance.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target labels
        
    Returns:
        tuple: (trained_model, metrics_dict)
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    # Apply SMOTE
    smote = SMOTE(random_state=42, k_neighbors=5)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight='balanced'
    )
    
    model.fit(X_train_balanced, y_train_balanced)
    
    # Generate predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    from sklearn.metrics import (accuracy_score, precision_score, 
                                recall_score, f1_score)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1_score': f1_score(y_test, y_pred, zero_division=0),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
    }
    
    # Confusion matrix (convert to list for JSON serialization)
    cm = confusion_matrix(y_test, y_pred)
    metrics['confusion_matrix'] = cm.tolist()
    
    # ROC Curve data (convert to list for JSON serialization)
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    metrics['fpr'] = fpr.tolist()
    metrics['tpr'] = tpr.tolist()
    metrics['roc_auc_score'] = auc(fpr, tpr)
    
    # Store predictions as lists for JSON serialization in dcc.Store
    metrics['y_pred'] = y_pred.tolist()
    metrics['y_pred_proba'] = y_pred_proba.tolist()
    metrics['y_test'] = y_test.tolist()
    
    return model, metrics


def calculate_risk_score(transaction, model, y_pred_proba=None, pred_proba=None):
    """
    Calculate risk score for a transaction (0-100 scale).
    
    Args:
        transaction: Transaction data
        model: Trained model
        y_pred_proba: Prediction probabilities
        pred_proba: Single prediction probability
        
    Returns:
        int: Risk score 0-100
    """
    if pred_proba is not None:
        return int(pred_proba * 100)
    return int(np.mean(y_pred_proba) * 100) if y_pred_proba is not None else 50


def get_risk_level(risk_score):
    """
    Categorize risk level based on risk score.
    
    Args:
        risk_score (float): Risk score 0-100
        
    Returns:
        str: Risk level category
    """
    if risk_score >= 70:
        return 'HIGH'
    elif risk_score >= 40:
        return 'MEDIUM'
    else:
        return 'LOW'


def create_analysis_report(df, model, metrics):
    """
    Create comprehensive analysis report data.
    
    Args:
        df (pd.DataFrame): Transaction data
        model: Trained model
        metrics (dict): Model performance metrics
        
    Returns:
        dict: Report data
    """
    report = {
        'total_transactions': len(df),
        'fraud_count': (df['Class'] == 1).sum(),
        'legitimate_count': (df['Class'] == 0).sum(),
        'fraud_rate': (df['Class'] == 1).sum() / len(df) * 100,
        'avg_fraud_amount': df[df['Class'] == 1]['Amount'].mean() if (df['Class'] == 1).any() else 0,
        'avg_legitimate_amount': df[df['Class'] == 0]['Amount'].mean(),
        'max_transaction_amount': df['Amount'].max(),
        'min_transaction_amount': df['Amount'].min(),
        'metrics': metrics,
    }
    return report


# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================

def get_feature_importance(model, feature_names, top_n=10):
    """
    Get top N important features from model.
    
    Args:
        model: Trained model
        feature_names (list): Feature names
        top_n (int): Number of top features
        
    Returns:
        pd.DataFrame: Feature importance dataframe
    """
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    importance_df = pd.DataFrame({
        'Feature': [feature_names[i] for i in indices],
        'Importance': importances[indices],
        'Importance_Pct': (importances[indices] / importances.sum() * 100).round(2)
    })
    
    return importance_df
