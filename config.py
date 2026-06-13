# ============================================================================
# FraudShield AI - Configuration & Styling
# ============================================================================
# Professional Enterprise Dashboard Color Scheme & Configuration

# ============================================================================
# COLOR PALETTE - Corporate Banking Theme
# ============================================================================
COLORS = {
    # Primary Colors
    'primary': '#0052CC',           # Professional Blue
    'primary_light': '#E8EEFB',     # Light Blue Background
    'primary_dark': '#003DA3',      # Dark Blue for hover
    
    # Secondary Colors
    'secondary': '#66BB6A',         # Professional Green
    'secondary_light': '#E8F5E9',   # Light Green Background
    
    # Risk Colors - Subtle & Professional
    'high_risk': '#C62828',         # Deep Red (not neon)
    'medium_risk': '#F57C00',       # Professional Orange
    'low_risk': '#66BB6A',          # Professional Green
    
    # Neutral Colors
    'background': '#FFFFFF',        # Pure White
    'surface': '#F5F7FA',           # Soft Gray Background
    'border': '#E0E6ED',            # Light Gray Border
    'text_dark': '#1A202C',         # Dark Text
    'text_light': '#718096',        # Light Gray Text
    'text_lighter': '#A0AEC0',      # Lighter Gray Text
    
    # Status Colors
    'success': '#2E7D32',           # Banking Green
    'warning': '#F57C00',           # Banking Orange
    'danger': '#C62828',            # Banking Red
    'info': '#0052CC',              # Banking Blue
    
    # Chart Colors
    'chart_fraud': '#C62828',
    'chart_legitimate': '#2E7D32',
    'chart_neutral': '#0052CC',
}

# ============================================================================
# TYPOGRAPHY & SPACING
# ============================================================================
FONTS = {
    'family': "'Segoe UI', 'Helvetica Neue', sans-serif",
    'size_xs': '12px',
    'size_sm': '14px',
    'size_base': '16px',
    'size_lg': '18px',
    'size_xl': '22px',
    'size_2xl': '28px',
    'size_3xl': '32px',
}

SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
    '2xl': '48px',
}

SHADOW = {
    'sm': '0 1px 3px rgba(0, 0, 0, 0.08)',
    'md': '0 4px 12px rgba(0, 0, 0, 0.1)',
    'lg': '0 8px 24px rgba(0, 0, 0, 0.12)',
}

BORDER_RADIUS = '12px'

# ============================================================================
# LAYOUT CONFIGURATION
# ============================================================================
LAYOUT_CONFIG = {
    'margin': SPACING['lg'],
    'max_width': '1600px',
    'card_padding': SPACING['lg'],
}

# ============================================================================
# TABLE CONFIGURATION
# ============================================================================
TABLE_CONFIG = {
    'rows_per_page': 10,
    'max_rows_display': 1000,
    'pagination_size': 50,
}

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
MODEL_CONFIG = {
    'test_size': 0.20,
    'random_state': 42,
    'n_estimators': 100,
    'max_features': 'sqrt',
    'class_weight': 'balanced_subsample',
}

# ============================================================================
# PERFORMANCE METRICS TEMPLATE
# ============================================================================
DEFAULT_METRICS = {
    'accuracy': 0.9999,
    'precision': 0.90,
    'recall': 0.84,
    'f1_score': 0.87,
    'roc_auc': 0.95,
}
