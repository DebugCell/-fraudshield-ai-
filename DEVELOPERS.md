# 🛠️ FraudShield AI - Developer Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Dash Web Application                  │
│                    (app.py - Main)                      │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ components   │  │ utils        │  │ config       │  │
│  │ (UI)         │  │ (ML/Data)    │  │ (Constants)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│        Data Layer │ ML Engine │ Storage │ Cache        │
└─────────────────────────────────────────────────────────┘
```

## File Structure Explained

### `app.py` - Main Application (800+ lines)
**Purpose**: Core Dash application with dashboard layout and callbacks

**Key Sections**:
```python
1. Application Initialization    (Lines 1-50)
2. Custom Styling               (Lines 51-80)
3. Application Layout           (Lines 81-500)
   - Header Section
   - KPI Cards
   - Data Upload
   - Analytics
   - Transaction Table
   - Risk Intelligence
   - Model Performance
   - Reports
4. Callbacks/Interactions        (Lines 501-800)
   - Data loading
   - Chart updates
   - Table updates
   - Statistics updates
```

**To Add New Features**:
```python
# 1. Add to layout in app.layout
html.Div(id='my-new-section', ...)

# 2. Create callback
@callback(
    Output('my-new-section', 'children'),
    Input('data-store', 'data')
)
def update_my_section(data):
    # Your logic here
    return content
```

### `config.py` - Configuration (150+ lines)
**Purpose**: Centralized styling and configuration constants

**Main Sections**:
```python
COLORS        # Color palette
FONTS         # Typography
SPACING       # Spacing units
SHADOW        # Shadow styles
BORDER_RADIUS # Corner radius
TABLE_CONFIG  # Table settings
MODEL_CONFIG  # ML parameters
```

**To Customize Colors**:
```python
COLORS = {
    'primary': '#0052CC',        # Change this
    'high_risk': '#C62828',      # And this
    # Add your colors
}
```

### `components.py` - Reusable Components (400+ lines)
**Purpose**: Custom UI components with professional styling

**Available Components**:
```python
create_kpi_card()              # KPI metric cards
create_metric_badge()          # Small metric badges
create_section_header()        # Section titles
create_upload_component()      # File upload area
create_risk_indicator()        # Risk level display
create_empty_state()           # Empty state placeholder
create_metric_summary()        # Metrics summary
create_status_badge()          # Status indicators
get_custom_styles()            # CSS styles
```

**To Create New Component**:
```python
def create_custom_component(param1, param2):
    """
    Create custom component.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        dbc.Card: Component
    """
    return dbc.Card(
        dbc.CardBody([
            # Your content here
        ]),
        style={
            'border': 'none',
            'borderRadius': BORDER_RADIUS,
            'boxShadow': SHADOW['md'],
        }
    )
```

### `utils.py` - Data & ML Utilities (500+ lines)
**Purpose**: Data processing and machine learning functions

**Core Functions**:
```python
generate_sample_data()         # Create synthetic data
preprocess_data()              # Feature engineering
train_fraud_detection_model()  # Model training
calculate_risk_score()         # Risk calculation
get_risk_level()               # Risk categorization
create_analysis_report()       # Report generation
get_feature_importance()       # Feature analysis
```

**To Modify Model**:
```python
def train_fraud_detection_model(X, y):
    # Change parameters here
    model = RandomForestClassifier(
        n_estimators=150,      # Change from 100
        max_depth=20,          # Change from 15
        # Add/remove parameters
    )
    # Rest of code
```

## Customization Examples

### 1. Change Primary Color Theme
**File**: `config.py`
```python
COLORS = {
    'primary': '#1E40AF',       # Change from #0052CC
    'primary_light': '#DBEAFE',
    'primary_dark': '#1E3A8A',
}
```

### 2. Add New Chart
**File**: `app.py`
```python
# 1. Add to layout
dcc.Graph(id='new-chart'),

# 2. Create callback
@callback(Output('new-chart', 'figure'), Input('data-store', 'data'))
def update_new_chart(data):
    df = pd.read_json(data['df'])
    fig = go.Figure()
    fig.add_trace(...)
    return fig
```

### 3. Modify KPI Cards
**File**: `app.py` - Header Section
```python
dbc.Col(
    create_kpi_card(
        'New Metric',           # Title
        'Value',               # Main number
        'Subtitle',            # Small text
        '📊',                  # Icon
        'primary',             # Color
        '↑ 5%'                 # Trend
    )
)
```

### 4. Change Typography
**File**: `config.py`
```python
FONTS = {
    'family': "'Inter', sans-serif",  # Change font
    'size_xl': '20px',                # Change size
}
```

### 5. Add New Metric to Model
**File**: `utils.py`
```python
metrics = {
    'accuracy': accuracy_score(...),
    'my_new_metric': calculate_my_metric(...),  # Add this
}
```

## Advanced Customization

### A. Add Database Integration
```python
# 1. Update requirements.txt
sqlalchemy>=2.0
psycopg2>=2.9

# 2. Create models.py
from sqlalchemy import create_engine
# Define your models

# 3. Update app.py to load from DB
def load_data_from_db():
    # Query database
    return data
```

### B. Add Real-time Updates
```python
# Use interval callback
dcc.Interval(id='interval-component', interval=5000),

@callback(
    Output('kpi-container', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_realtime(n):
    # Fetch fresh data
    return kpi_cards
```

### C. Add Authentication
```python
# Install dash-auth
pip install dash-auth

# Add to app.py
import dash_auth
valid_credentials = {'user': 'password'}
auth = dash_auth.BasicAuth(app, valid_credentials)
```

### D. Add Multi-user Support
```python
from flask import session
from flask_session import Session

# Configure sessions
app.server.config['SECRET_KEY'] = 'your-secret'
Session(app.server)
```

## Performance Optimization

### 1. Reduce Chart Update Frequency
```python
# In callbacks, add prevent_initial_call
prevent_initial_call=True

# Or add debouncing
dcc.Input(id='search', debounce=500)
```

### 2. Optimize Data Loading
```python
# Use data sampling
df = df.sample(frac=0.1)  # Use 10% of data

# Or pagination
start_idx = (page - 1) * rows_per_page
df = df.iloc[start_idx:start_idx + rows_per_page]
```

### 3. Cache Expensive Calculations
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param):
    # Only runs when param changes
    return result
```

## Testing

### Unit Tests
```python
# tests/test_utils.py
def test_generate_sample_data():
    df = generate_sample_data(100)
    assert len(df) == 100
    assert 'Class' in df.columns
```

### Run Tests
```bash
pytest tests/
```

## Debugging

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Browser DevTools
1. Open F12 in browser
2. Check Console for errors
3. Check Network tab for requests
4. Use Dash Dev Tools (built-in)

### Debug Callbacks
```python
@callback(...)
def my_callback(data):
    print(f"Debug: {data}")  # Print to console
    return result
```

## Deployment Checklist

- [ ] Update `DASH_DEBUG = False` in `config.py`
- [ ] Set secure `SECRET_KEY`
- [ ] Configure database connection
- [ ] Set up logging
- [ ] Test all features
- [ ] Optimize for production
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review security settings
- [ ] Document custom changes

## Common Issues & Solutions

### Issue: Charts not updating
**Solution**: Check data store is being updated
```python
# Add to callback
print(f"Data store: {data_store}")  # Debug
```

### Issue: Slow performance
**Solution**: Reduce data size or add pagination
```python
df = df.head(1000)  # Limit rows
```

### Issue: Memory errors
**Solution**: Clear cache or use generators
```python
del large_dataframe  # Free memory
gc.collect()        # Garbage collection
```

## Resources

- **Dash Documentation**: https://dash.plotly.com/
- **Plotly Charts**: https://plotly.com/python/
- **Scikit-learn**: https://scikit-learn.org/
- **Bootstrap Components**: https://dash-bootstrap-components.opensource.faculty.ai/

## Support

For issues or questions:
1. Check comments in code
2. Review docstrings
3. Consult documentation
4. Test with simple examples

---

Happy coding! 🚀
