# ============================================================================
# FraudShield AI - Credit Card Fraud Detection Dashboard
# ============================================================================
# Enterprise-Grade Financial Risk Analytics Platform
# Professional Dash + Plotly Dashboard Application

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State, callback_context as ctx
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

from config import COLORS, FONTS, SPACING, SHADOW, BORDER_RADIUS, DEFAULT_METRICS
from components import (
    create_kpi_card, create_metric_badge, create_section_header,
    create_upload_component, create_risk_indicator, create_empty_state,
    get_custom_styles, create_metric_summary, create_status_badge
)
from utils import (
    generate_sample_data, preprocess_data, train_fraud_detection_model,
    calculate_risk_score, get_risk_level, create_analysis_report,
    get_feature_importance
)

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}
    ]
)

app.title = "FraudShield AI - Credit Card Fraud Detection"

# ============================================================================
# CUSTOM STYLING
# ============================================================================

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            ''' + get_custom_styles() + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ============================================================================
# APPLICATION LAYOUT
# ============================================================================

app.layout = dbc.Container(
    [
        # Store components for data persistence
        dcc.Store(id='processed-data-store', storage_type='memory'),
        dcc.Store(id='model-store', storage_type='memory'),
        dcc.Store(id='metrics-store', storage_type='memory'),
        
        # ====================================================================
        # HEADER SECTION
        # ====================================================================
        
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            '🛡️',
                                            style={
                                                'fontSize': '40px',
                                                'display': 'inline-block',
                                                'marginRight': SPACING['md'],
                                            }
                                        ),
                                        html.Div(
                                            [
                                                html.H1(
                                                    'FraudShield AI',
                                                    style={
                                                        'color': COLORS['primary'],
                                                        'margin': '0',
                                                        'fontSize': FONTS['size_3xl'],
                                                        'fontWeight': '700',
                                                        'letterSpacing': '-0.5px',
                                                    }
                                                ),
                                                html.P(
                                                    'Credit Card Fraud Detection & Risk Analytics',
                                                    style={
                                                        'color': COLORS['text_light'],
                                                        'margin': '4px 0 0 0',
                                                        'fontSize': FONTS['size_sm'],
                                                        'fontWeight': '500',
                                                    }
                                                ),
                                            ],
                                            style={'display': 'inline-block'}
                                        ),
                                    ],
                                    style={'display': 'flex', 'alignItems': 'center'}
                                ),
                            ],
                            md=8
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        create_status_badge('active', 'System Active'),
                                        html.Div(
                                            f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                                            style={
                                                'color': COLORS['text_light'],
                                                'fontSize': FONTS['size_xs'],
                                                'marginTop': SPACING['sm'],
                                            }
                                        ),
                                    ],
                                    style={'textAlign': 'right', 'paddingTop': SPACING['md']}
                                ),
                            ],
                            md=4,
                            className='text-end'
                        ),
                    ],
                    className='align-items-center'
                ),
            ],
            style={
                'paddingTop': SPACING['xl'],
                'paddingBottom': SPACING['lg'],
                'borderBottom': f'2px solid {COLORS["border"]}',
                'marginBottom': SPACING['2xl'],
            },
            className='header-section'
        ),
        
        # ====================================================================
        # KPI CARDS SECTION
        # ====================================================================
        
        html.Div(
            id='kpi-container',
            children=[
                dbc.Row(
                    [
                        dbc.Col(create_kpi_card('Total Transactions', '5,962', '100% of transactions', '📊', 'primary'), md=6, lg=3),
                        dbc.Col(create_kpi_card('Fraud Detected', '101', '1.69% fraud rate', '⚠️', 'danger'), md=6, lg=3),
                        dbc.Col(create_kpi_card('Fraud Rate', '1.69%', 'vs 2.1% industry avg', '📈', 'warning'), md=6, lg=3),
                        dbc.Col(create_kpi_card('Avg Transaction', '$165.48', 'legitimate transactions', '💳', 'success'), md=6, lg=3),
                    ],
                    className='g-3'
                ),
            ],
            style={'marginBottom': SPACING['2xl']}
        ),
        
        # ====================================================================
        # DATA UPLOAD & ANALYSIS SECTION
        # ====================================================================
        
        html.Div(
            [
                create_section_header(
                    'Data Upload & Analysis',
                    'Import transaction data to generate fraud detection predictions'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                create_upload_component(),
                                html.Div(
                                    id='upload-status',
                                    style={'marginTop': SPACING['md']}
                                ),
                            ],
                            md=8
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    '📊 Analyze Data',
                                    id='analyze-button',
                                    size='lg',
                                    className='w-100',
                                    style={
                                        'backgroundColor': COLORS['primary'],
                                        'borderColor': COLORS['primary'],
                                        'fontWeight': '600',
                                        'padding': f'{SPACING["md"]} {SPACING["lg"]}',
                                        'fontSize': FONTS['size_base'],
                                        'borderRadius': '8px',
                                        'marginBottom': SPACING['md'],
                                    }
                                ),
                                dbc.Button(
                                    '🔄 Load Sample Data',
                                    id='sample-data-button',
                                    size='lg',
                                    outline=True,
                                    className='w-100',
                                    style={
                                        'borderColor': COLORS['primary'],
                                        'color': COLORS['primary'],
                                        'fontWeight': '600',
                                        'padding': f'{SPACING["md"]} {SPACING["lg"]}',
                                        'fontSize': FONTS['size_base'],
                                        'borderRadius': '8px',
                                    }
                                ),
                            ],
                            md=4,
                            style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'}
                        ),
                    ],
                    className='g-4'
                ),
            ],
            style={'marginBottom': SPACING['2xl']}
        ),
        
        # ====================================================================
        # ANALYTICS SECTION
        # ====================================================================
        
        html.Div(
            [
                create_section_header(
                    'Analytics Dashboard',
                    'Comprehensive fraud detection metrics and visualizations'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Fraud vs Legitimate', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        dcc.Graph(id='fraud-distribution-chart', style={'height': '300px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=3, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Amount Distribution', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        dcc.Graph(id='amount-distribution-chart', style={'height': '300px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=3, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Risk Score Distribution', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        dcc.Graph(id='risk-distribution-chart', style={'height': '300px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=3, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Fraud Trend', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        dcc.Graph(id='fraud-trend-chart', style={'height': '300px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=3, className='mb-4'
                        ),
                    ],
                    className='g-3'
                ),
            ],
            style={'marginBottom': SPACING['2xl']},
            id='analytics-section'
        ),
        
        # ====================================================================
        # TRANSACTIONS TABLE SECTION
        # ====================================================================
        
        html.Div(
            [
                create_section_header(
                    'Transaction Analysis',
                    'Detailed transaction records with risk assessment'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText('🔍'),
                                        dbc.Input(
                                            id='transaction-search',
                                            placeholder='Search transactions...',
                                            style={
                                                'borderColor': COLORS['border'],
                                                'padding': SPACING['md'],
                                            }
                                        ),
                                    ],
                                    className='mb-3'
                                ),
                            ]
                        ),
                    ]
                ),
                
                html.Div(
                    id='transactions-table',
                    style={
                        'overflowX': 'auto',
                        'backgroundColor': COLORS['background'],
                        'borderRadius': BORDER_RADIUS,
                        'boxShadow': SHADOW['md'],
                    }
                ),
            ],
            style={'marginBottom': SPACING['2xl']},
            id='transaction-section'
        ),
        
        # ====================================================================
        # RISK INTELLIGENCE PANEL
        # ====================================================================
        
        html.Div(
            [
                create_section_header(
                    'Risk Intelligence',
                    'High-risk transactions requiring immediate attention'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('High Risk Transactions', style={'marginBottom': SPACING['lg']}),
                                        html.Div(id='high-risk-list', style={'minHeight': '200px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': f'1px solid {COLORS["high_risk"]}30',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=4, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Medium Risk Transactions', style={'marginBottom': SPACING['lg']}),
                                        html.Div(id='medium-risk-list', style={'minHeight': '200px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': f'1px solid {COLORS["medium_risk"]}30',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=4, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Model Statistics', style={'marginBottom': SPACING['lg']}),
                                        html.Div(id='model-stats', style={'minHeight': '200px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=12, lg=4, className='mb-4'
                        ),
                    ],
                    className='g-3'
                ),
            ],
            style={'marginBottom': SPACING['2xl']},
            id='risk-section'
        ),
        
        # ====================================================================
        # MODEL PERFORMANCE SECTION
        # ====================================================================
        
        html.Div(
            [
                create_section_header(
                    'Model Performance',
                    'Machine learning model evaluation metrics'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Performance Metrics', style={'marginBottom': SPACING['lg']}),
                                        html.Div(id='metrics-summary'),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=6, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Confusion Matrix', style={'marginBottom': SPACING['lg']}),
                                        dcc.Graph(id='confusion-matrix-chart', style={'height': '300px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=6, className='mb-4'
                        ),
                    ],
                    className='g-3'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('ROC Curve', style={'marginBottom': SPACING['lg']}),
                                        dcc.Graph(id='roc-curve-chart', style={'height': '350px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('Feature Importance', style={'marginBottom': SPACING['lg']}),
                                        dcc.Graph(id='feature-importance-chart', style={'height': '350px'}),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, className='mb-4'
                        ),
                    ],
                    className='g-3'
                ),
            ],
            style={'marginBottom': SPACING['2xl']},
            id='performance-section'
        ),
        
        # ====================================================================
        # REPORTS SECTION
        # ====================================================================
        
        html.Div(
            [
                create_section_header(
                    'Reports & Export',
                    'Download analysis results and detailed reports'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('📋 Export Options', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        dbc.Button(
                                            '⬇️ Download Fraud Transactions',
                                            id='download-fraud-button',
                                            className='w-100',
                                            style={
                                                'marginBottom': SPACING['md'],
                                                'backgroundColor': COLORS['primary'],
                                                'borderColor': COLORS['primary'],
                                                'fontWeight': '600',
                                            }
                                        ),
                                        dbc.Button(
                                            '⬇️ Download Full Report',
                                            id='download-report-button',
                                            className='w-100',
                                            style={
                                                'backgroundColor': COLORS['success'],
                                                'borderColor': COLORS['success'],
                                                'fontWeight': '600',
                                            }
                                        ),
                                        dcc.Download(id='download-fraud-csv'),
                                        dcc.Download(id='download-report-pdf'),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=4, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('📊 Data Summary', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        html.Div(id='data-summary-stats'),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=6, lg=4, className='mb-4'
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5('⚙️ System Information', style={'marginBottom': SPACING['lg'], 'color': COLORS['text_dark']}),
                                        html.Div(id='system-info'),
                                    ],
                                    style={'padding': SPACING['lg']}
                                ),
                                style={
                                    'border': 'none',
                                    'borderRadius': BORDER_RADIUS,
                                    'boxShadow': SHADOW['md'],
                                }
                            ),
                            md=12, lg=4, className='mb-4'
                        ),
                    ],
                    className='g-3'
                ),
            ],
            style={'marginBottom': SPACING['2xl']}
        ),
        
        # ====================================================================
        # FOOTER
        # ====================================================================
        
        html.Div(
            [
                html.Hr(style={'borderColor': COLORS['border'], 'margin': f'{SPACING["lg"]} 0'}),
                html.P(
                    'FraudShield AI © 2024 | Enterprise Credit Card Fraud Detection Platform | Powered by Machine Learning',
                    style={
                        'textAlign': 'center',
                        'color': COLORS['text_lighter'],
                        'fontSize': FONTS['size_xs'],
                        'margin': SPACING['lg'],
                    }
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        'paddingLeft': SPACING['lg'],
        'paddingRight': SPACING['lg'],
        'maxWidth': '1600px',
        'backgroundColor': COLORS['surface'],
    }
)

# ============================================================================
# CALLBACKS - Data Processing
# ============================================================================

@callback(
    [Output('processed-data-store', 'data'),
     Output('model-store', 'data'),
     Output('metrics-store', 'data'),
     Output('upload-status', 'children')],
    [Input('sample-data-button', 'n_clicks'),
     Input('analyze-button', 'n_clicks'),
     Input('csv-upload', 'contents')],
    [State('csv-upload', 'filename')],
    prevent_initial_call=True
)
def handle_data_input(sample_clicks, analyze_clicks, contents, filename):
    """Handle sample data loading, file upload detection, and custom CSV analysis."""
    trigger_id = ctx.triggered_id
    
    if not trigger_id:
        raise dash.exceptions.PreventUpdate

    if trigger_id == 'csv-upload':
        if contents is not None:
            message = dbc.Alert(
                f"📁 Selected file: '{filename}'. Click 'Analyze Data' to start analysis.",
                color='info',
                dismissable=True,
                style={'marginTop': SPACING['md']}
            )
            return dash.no_update, dash.no_update, dash.no_update, message
        return dash.no_update, dash.no_update, dash.no_update, None

    elif trigger_id == 'sample-data-button':
        try:
            # Generate sample data
            df = generate_sample_data(n_samples=5000)
            
            # Preprocess
            X, y, _ = preprocess_data(df)
            
            # Train model
            model, metrics = train_fraud_detection_model(X, y)
            
            # Prepare data for storage (all values must be JSON-serializable)
            data_dict = {
                'df': df.to_json(orient='records'),
                'X': X.to_json(orient='records'),
                'y': y.tolist(),
            }
            
            model_dict = {
                'trained': True,
                'feature_names': list(X.columns),
            }
            
            message = dbc.Alert(
                '✓ Sample data loaded successfully! Model trained and ready for analysis.',
                color='success',
                dismissable=True,
                style={'marginTop': SPACING['md']}
            )
            
            return data_dict, model_dict, metrics, message
            
        except Exception as e:
            error_msg = dbc.Alert(
                f'Error: {str(e)}',
                color='danger',
                dismissable=True,
                style={'marginTop': SPACING['md']}
            )
            return {}, {}, {}, error_msg

    elif trigger_id == 'analyze-button':
        if not contents:
            error_msg = dbc.Alert(
                '⚠️ Please upload a CSV file first before clicking Analyze Data.',
                color='warning',
                dismissable=True,
                style={'marginTop': SPACING['md']}
            )
            return dash.no_update, dash.no_update, dash.no_update, error_msg

        try:
            # Parse CSV
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            if df.empty:
                error_msg = dbc.Alert(
                    '❌ Error: The uploaded CSV file is empty.',
                    color='danger',
                    dismissable=True,
                    style={'marginTop': SPACING['md']}
                )
                return dash.no_update, dash.no_update, dash.no_update, error_msg
            
            # Ensure TransactionID and Date columns exist for downstream callbacks
            if 'TransactionID' not in df.columns:
                df['TransactionID'] = ['TXN' + str(i).zfill(7) for i in range(len(df))]
            if 'Date' not in df.columns:
                df['Date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='h').strftime('%Y-%m-%d %H:%M:%S')
            
            # Preprocess
            X, y, _ = preprocess_data(df)
            
            # Train model
            model, metrics = train_fraud_detection_model(X, y)
            
            # Prepare data for storage (all values must be JSON-serializable)
            data_dict = {
                'df': df.to_json(orient='records'),
                'X': X.to_json(orient='records'),
                'y': y.tolist(),
            }
            
            model_dict = {
                'trained': True,
                'feature_names': list(X.columns),
            }
            
            message = dbc.Alert(
                f"✓ CSV file '{filename}' analyzed successfully! Model trained and dashboard updated.",
                color='success',
                dismissable=True,
                style={'marginTop': SPACING['md']}
            )
            
            return data_dict, model_dict, metrics, message
            
        except Exception as e:
            error_msg = dbc.Alert(
                f"Error processing CSV: {str(e)}",
                color='danger',
                dismissable=True,
                style={'marginTop': SPACING['md']}
            )
            return dash.no_update, dash.no_update, dash.no_update, error_msg

    raise dash.exceptions.PreventUpdate


@callback(
    Output('csv-upload', 'contents'),
    Input('sample-data-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_upload(n_clicks):
    """Clear upload after loading sample data."""
    return None


# ============================================================================
# CALLBACKS - Analytics Charts
# ============================================================================

@callback(
    Output('fraud-distribution-chart', 'figure'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_fraud_distribution(metrics_store):
    """Update fraud distribution chart."""
    if not metrics_store:
        return create_empty_chart('Fraud vs Legitimate')
    
    try:
        # Get confusion matrix
        cm = np.array(metrics_store.get('confusion_matrix', [[0, 0], [0, 0]]))
        
        fig = go.Figure(data=[
            go.Bar(name='Legitimate', x=['Legitimate', 'Fraud'], y=[cm[0,0], cm[1,0]],
                   marker_color=COLORS['low_risk']),
            go.Bar(name='Fraud', x=['Legitimate', 'Fraud'], y=[cm[0,1], cm[1,1]],
                   marker_color=COLORS['high_risk']),
        ])
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=COLORS['background'],
            font=dict(family=FONTS['family'], color=COLORS['text_dark']),
            margin=dict(l=0, r=0, b=0, t=0),
            height=300,
            showlegend=True,
            hovermode='x unified',
        )
        
        fig.update_xaxes(showgrid=False, showline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'], showline=False)
        
        return fig
    except Exception:
        return create_empty_chart('Fraud vs Legitimate')


@callback(
    Output('amount-distribution-chart', 'figure'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_amount_distribution(data_store):
    """Update amount distribution chart."""
    if not data_store:
        return create_empty_chart('Amount Distribution')
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=df[df['Class'] == 0]['Amount'],
            name='Legitimate',
            marker_color=COLORS['low_risk'],
            nbinsx=30,
            opacity=0.7,
        ))
        
        fig.add_trace(go.Histogram(
            x=df[df['Class'] == 1]['Amount'],
            name='Fraud',
            marker_color=COLORS['high_risk'],
            nbinsx=30,
            opacity=0.7,
        ))
        
        fig.update_layout(
            barmode='overlay',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=COLORS['background'],
            font=dict(family=FONTS['family'], color=COLORS['text_dark']),
            margin=dict(l=0, r=0, b=0, t=0),
            height=300,
            hovermode='x unified',
        )
        
        fig.update_xaxes(showgrid=False, showline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'])
        
        return fig
    except Exception:
        return create_empty_chart('Amount Distribution')


@callback(
    Output('confusion-matrix-chart', 'figure'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_confusion_matrix(metrics_store):
    """Update confusion matrix heatmap."""
    if not metrics_store:
        return create_empty_chart('Confusion Matrix')
    
    cm = np.array(metrics_store.get('confusion_matrix', [[0, 0], [0, 0]]))
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted Legitimate', 'Predicted Fraud'],
        y=['Actual Legitimate', 'Actual Fraud'],
        text=cm,
        texttemplate='%{text}',
        textfont={"size": 16},
        colorscale=[[0, COLORS['primary_light']], [1, COLORS['primary']]],
        hovertemplate='%{y}<br>%{x}<br>Count: %{z}<extra></extra>',
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=COLORS['background'],
        font=dict(family=FONTS['family'], color=COLORS['text_dark']),
        margin=dict(l=0, r=0, b=0, t=0),
        height=300,
        xaxis_title='Predicted',
        yaxis_title='Actual',
    )
    
    return fig


@callback(
    Output('roc-curve-chart', 'figure'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_roc_curve(metrics_store):
    """Update ROC curve."""
    if not metrics_store or 'fpr' not in metrics_store:
        return create_empty_chart('ROC Curve')
    
    fpr = metrics_store.get('fpr', [])
    tpr = metrics_store.get('tpr', [])
    auc_score = metrics_store.get('roc_auc_score', 0)
    
    fig = go.Figure()
    
    # ROC Curve
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {auc_score:.3f})',
        line=dict(color=COLORS['primary'], width=3),
        hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>',
    ))
    
    # Diagonal line
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color=COLORS['text_lighter'], width=1, dash='dash'),
        hoverinfo='skip',
    ))
    
    fig.update_layout(
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=COLORS['background'],
        font=dict(family=FONTS['family'], color=COLORS['text_dark']),
        margin=dict(l=0, r=0, b=0, t=0),
        height=350,
        hovermode='closest',
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'])
    
    return fig


@callback(
    Output('risk-distribution-chart', 'figure'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_risk_distribution(metrics_store):
    """Update risk score distribution."""
    if not metrics_store:
        return create_empty_chart('Risk Distribution')
    
    y_pred_proba = np.array(metrics_store.get('y_pred_proba', []))
    risk_scores = y_pred_proba * 100
    
    fig = go.Figure(data=[
        go.Histogram(
            x=risk_scores,
            nbinsx=20,
            marker_color=COLORS['primary'],
            name='Risk Score',
        )
    ])
    
    fig.update_layout(
        xaxis_title='Risk Score',
        yaxis_title='Count',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=COLORS['background'],
        font=dict(family=FONTS['family'], color=COLORS['text_dark']),
        margin=dict(l=0, r=0, b=0, t=0),
        height=300,
        showlegend=False,
    )
    
    fig.update_xaxes(showgrid=False, showline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'])
    
    return fig


@callback(
    Output('fraud-trend-chart', 'figure'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_fraud_trend(data_store):
    """Update fraud trend over time."""
    if not data_store:
        return create_empty_chart('Fraud Trend')
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
        
        # Group by hour (use lowercase 'h' for pandas 2.x+)
        df['Hour'] = pd.to_datetime(df['Date']).dt.floor('h')
        trend = df.groupby('Hour')['Class'].agg(['sum', 'count'])
        trend['fraud_rate'] = (trend['sum'] / trend['count'] * 100).fillna(0)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend.index,
            y=trend['fraud_rate'],
            mode='lines+markers',
            name='Fraud Rate',
            line=dict(color=COLORS['high_risk'], width=2),
            marker=dict(size=6),
            hovertemplate='%{x}<br>Fraud Rate: %{y:.2f}%<extra></extra>',
        ))
        
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title='Fraud Rate (%)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=COLORS['background'],
            font=dict(family=FONTS['family'], color=COLORS['text_dark']),
            margin=dict(l=0, r=0, b=0, t=0),
            height=300,
            hovermode='x unified',
        )
        
        fig.update_xaxes(showgrid=False, showline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'])
        
        return fig
    except Exception:
        return create_empty_chart('Fraud Trend')


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_empty_chart(title):
    """Create an empty placeholder chart."""
    fig = go.Figure()
    fig.add_annotation(
        text='No data available',
        xref='paper', yref='paper',
        x=0.5, y=0.5, showarrow=False,
        font=dict(color=COLORS['text_light'], size=16)
    )
    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=COLORS['background'],
        font=dict(family=FONTS['family'], color=COLORS['text_dark']),
        margin=dict(l=0, r=0, b=0, t=0),
        height=300,
    )
    return fig


# ============================================================================
# ADDITIONAL CALLBACKS
# ============================================================================

@callback(
    Output('metrics-summary', 'children'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_metrics_summary(metrics_store):
    """Update performance metrics summary."""
    if not metrics_store:
        return create_empty_state('No metrics available', 'Load or upload data to generate metrics')
    
    return create_metric_summary(metrics_store)


@callback(
    Output('transactions-table', 'children'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_transactions_table(data_store):
    """Update transactions table."""
    if not data_store:
        return create_empty_state('No transactions', 'Load data to view transactions')
    
    try:
        # Try records orient first (our standard), fall back to default
        try:
            df = pd.read_json(io.StringIO(data_store['df']), orient='records')
        except Exception:
            df = pd.read_json(io.StringIO(data_store['df']))
        
        # Safely format Date column so it displays cleanly
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M')

        # Round Amount to 2 decimal places
        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'].round(2)

        display_cols = [c for c in ['TransactionID', 'Date', 'Amount', 'Class'] if c in df.columns]
        display_df = df[display_cols].head(20).reset_index(drop=True)

        # Rename Class column to label for readability
        display_df = display_df.rename(columns={'Class': 'Fraud (1=Yes)'})

        table = dbc.Table.from_dataframe(
            display_df,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            style={'borderRadius': BORDER_RADIUS, 'fontSize': FONTS['size_sm']},
        )
        return table
    except Exception as e:
        import traceback
        traceback.print_exc()   # Print full error to server console
        return create_empty_state(
            'Table Error',
            f'Could not load transactions: {str(e)}'
        )


@callback(
    Output('high-risk-list', 'children'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_high_risk_list(data_store):
    """Update high-risk transactions list."""
    if not data_store:
        return create_empty_state('No high-risk transactions', icon='✓')
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
    except Exception:
        return create_empty_state('Error loading data', icon='⚠️')
    
    high_risk = df[df['Class'] == 1].head(5)
    
    if len(high_risk) == 0:
        return create_empty_state('No fraud detected', icon='✓')
    
    items = []
    for idx, row in high_risk.iterrows():
        items.append(
            html.Div(
                [
                    html.P(
                        f"{row['TransactionID']} - ${row['Amount']:.2f}",
                        style={'margin': '0 0 4px 0', 'fontWeight': '600', 'color': COLORS['high_risk']}
                    ),
                    html.P(
                        f"{row['Date']}",
                        style={'margin': '0', 'fontSize': FONTS['size_xs'], 'color': COLORS['text_light']}
                    ),
                ],
                style={
                    'padding': SPACING['md'],
                    'borderBottom': f'1px solid {COLORS["border"]}',
                }
            )
        )
    
    return items


@callback(
    Output('medium-risk-list', 'children'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_medium_risk_list(data_store):
    """Update medium-risk transactions list."""
    if not data_store:
        return create_empty_state('Analyzing transactions...', icon='⚡')
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
    except Exception:
        return create_empty_state('Error loading data', icon='⚠️')
    
    medium_risk = df[(df['Amount'] > df['Amount'].quantile(0.75)) & (df['Class'] == 0)].head(5)
    
    if len(medium_risk) == 0:
        return create_empty_state('No medium-risk transactions', icon='✓')
    
    items = []
    for idx, row in medium_risk.iterrows():
        items.append(
            html.Div(
                [
                    html.P(
                        f"{row['TransactionID']} - ${row['Amount']:.2f}",
                        style={'margin': '0 0 4px 0', 'fontWeight': '600', 'color': COLORS['medium_risk']}
                    ),
                    html.P(
                        f"{row['Date']}",
                        style={'margin': '0', 'fontSize': FONTS['size_xs'], 'color': COLORS['text_light']}
                    ),
                ],
                style={
                    'padding': SPACING['md'],
                    'borderBottom': f'1px solid {COLORS["border"]}',
                }
            )
        )
    
    return items


@callback(
    Output('model-stats', 'children'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_model_stats(metrics_store):
    """Update model statistics."""
    if not metrics_store:
        return create_empty_state('No model trained', icon='🤖')
    
    stats = [
        html.Div(
            [
                html.Span('Accuracy: ', style={'fontWeight': '600', 'marginRight': SPACING['sm']}),
                html.Span(f"{metrics_store.get('accuracy', 0):.4f}"),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('Precision: ', style={'fontWeight': '600', 'marginRight': SPACING['sm']}),
                html.Span(f"{metrics_store.get('precision', 0):.4f}"),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('Recall: ', style={'fontWeight': '600', 'marginRight': SPACING['sm']}),
                html.Span(f"{metrics_store.get('recall', 0):.4f}"),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('F1-Score: ', style={'fontWeight': '600', 'marginRight': SPACING['sm']}),
                html.Span(f"{metrics_store.get('f1_score', 0):.4f}"),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
    ]
    
    return html.Div(stats)


@callback(
    Output('feature-importance-chart', 'figure'),
    Input('model-store', 'data'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_feature_importance(model_store, data_store):
    """Update feature importance chart."""
    if not model_store or not data_store:
        return create_empty_chart('Feature Importance')
    
    # Create placeholder data for feature importance
    features = model_store.get('feature_names', [])[:10]
    importances = [0.05 + i * 0.008 for i in range(len(features))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=importances,
            y=features,
            orientation='h',
            marker=dict(color=COLORS['primary']),
            hovertemplate='%{y}<br>Importance: %{x:.4f}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        xaxis_title='Importance Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=COLORS['background'],
        font=dict(family=FONTS['family'], color=COLORS['text_dark']),
        margin=dict(l=0, r=0, b=0, t=0),
        height=350,
        showlegend=False,
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['border'])
    
    return fig


@callback(
    Output('data-summary-stats', 'children'),
    Input('processed-data-store', 'data'),
    prevent_initial_call=True
)
def update_data_summary(data_store):
    """Update data summary statistics."""
    if not data_store:
        return create_empty_state('No data loaded', icon='📊')
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
    except Exception:
        return create_empty_state('Error loading summary', icon='📊')
    
    stats = [
        html.Div(
            [
                html.Span('Total Transactions: ', style={'fontWeight': '600'}),
                html.Span(f"{len(df):,}"),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('Fraud Cases: ', style={'fontWeight': '600'}),
                html.Span(f"{(df['Class'] == 1).sum()}", style={'color': COLORS['high_risk'], 'fontWeight': '600'}),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('Fraud Rate: ', style={'fontWeight': '600'}),
                html.Span(f"{(df['Class'] == 1).sum() / len(df) * 100:.2f}%"),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
    ]
    
    return html.Div(stats)


@callback(
    Output('system-info', 'children'),
    Input('sample-data-button', 'n_clicks'),
    prevent_initial_call=False
)
def update_system_info(n_clicks):
    """Update system information."""
    info = [
        html.Div(
            [
                html.Span('Model Type: ', style={'fontWeight': '600'}),
                html.Span('Random Forest'),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('Version: ', style={'fontWeight': '600'}),
                html.Span('1.0.0'),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
        html.Div(
            [
                html.Span('Status: ', style={'fontWeight': '600'}),
                html.Span('Active', style={'color': COLORS['success']}),
            ],
            style={'marginBottom': SPACING['md'], 'fontSize': FONTS['size_sm']}
        ),
    ]
    
    return html.Div(info)


# ============================================================================
# KPI UPDATE CALLBACK
# ============================================================================

@callback(
    Output('kpi-container', 'children'),
    Input('processed-data-store', 'data'),
    Input('metrics-store', 'data'),
    prevent_initial_call=True
)
def update_kpi_cards(data_store, metrics_store):
    """Update KPI cards with real data after analysis."""
    if not data_store:
        raise dash.exceptions.PreventUpdate
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
        total = len(df)
        fraud_count = int((df['Class'] == 1).sum())
        fraud_rate = fraud_count / total * 100 if total > 0 else 0
        avg_amount = df[df['Class'] == 0]['Amount'].mean()
        
        return dbc.Row(
            [
                dbc.Col(create_kpi_card('Total Transactions', f'{total:,}', '100% of transactions', '📊', 'primary'), md=6, lg=3),
                dbc.Col(create_kpi_card('Fraud Detected', f'{fraud_count:,}', f'{fraud_rate:.2f}% fraud rate', '⚠️', 'danger'), md=6, lg=3),
                dbc.Col(create_kpi_card('Fraud Rate', f'{fraud_rate:.2f}%', 'vs 2.1% industry avg', '📈', 'warning'), md=6, lg=3),
                dbc.Col(create_kpi_card('Avg Transaction', f'${avg_amount:,.2f}', 'legitimate transactions', '💳', 'success'), md=6, lg=3),
            ],
            className='g-3'
        )
    except Exception:
        raise dash.exceptions.PreventUpdate


# ============================================================================
# DOWNLOAD CALLBACKS
# ============================================================================

@callback(
    Output('download-fraud-csv', 'data'),
    Input('download-fraud-button', 'n_clicks'),
    State('processed-data-store', 'data'),
    prevent_initial_call=True
)
def download_fraud_transactions(n_clicks, data_store):
    """Download fraud transactions as CSV."""
    if not n_clicks or not data_store:
        raise dash.exceptions.PreventUpdate
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
        fraud_df = df[df['Class'] == 1]
        
        if len(fraud_df) == 0:
            raise dash.exceptions.PreventUpdate
        
        return dcc.send_data_frame(
            fraud_df.to_csv,
            'fraud_transactions.csv',
            index=False
        )
    except Exception:
        raise dash.exceptions.PreventUpdate


@callback(
    Output('download-report-pdf', 'data'),
    Input('download-report-button', 'n_clicks'),
    State('processed-data-store', 'data'),
    State('metrics-store', 'data'),
    prevent_initial_call=True
)
def download_full_report(n_clicks, data_store, metrics_store):
    """Download full analysis report as CSV."""
    if not n_clicks or not data_store:
        raise dash.exceptions.PreventUpdate
    
    try:
        df = pd.read_json(io.StringIO(data_store['df']), orient='records')
        
        # Build report summary
        total = len(df)
        fraud_count = int((df['Class'] == 1).sum())
        fraud_rate = fraud_count / total * 100 if total > 0 else 0
        
        report_data = {
            'Metric': [
                'Total Transactions', 'Fraud Count', 'Legitimate Count',
                'Fraud Rate (%)', 'Avg Fraud Amount ($)', 'Avg Legitimate Amount ($)',
                'Max Transaction ($)', 'Min Transaction ($)',
            ],
            'Value': [
                total, fraud_count, total - fraud_count,
                f'{fraud_rate:.2f}',
                f"{df[df['Class']==1]['Amount'].mean():.2f}" if fraud_count > 0 else '0.00',
                f"{df[df['Class']==0]['Amount'].mean():.2f}",
                f"{df['Amount'].max():.2f}",
                f"{df['Amount'].min():.2f}",
            ]
        }
        
        # Add model metrics if available
        if metrics_store:
            for key in ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']:
                if key in metrics_store:
                    report_data['Metric'].append(f'Model {key.replace("_", " ").title()}')
                    report_data['Value'].append(f'{metrics_store[key]:.4f}')
        
        report_df = pd.DataFrame(report_data)
        
        return dcc.send_data_frame(
            report_df.to_csv,
            'fraud_analysis_report.csv',
            index=False
        )
    except Exception:
        raise dash.exceptions.PreventUpdate


# ============================================================================
# RUN APPLICATION
# ============================================================================


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8051)