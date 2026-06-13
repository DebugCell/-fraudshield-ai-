# ============================================================================
# FraudShield AI - Reusable Dash Components
# ============================================================================
# Professional UI components with corporate styling

import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State
import plotly.graph_objects as go
from config import COLORS, FONTS, SPACING, SHADOW, BORDER_RADIUS

# ============================================================================
# KPI CARD COMPONENT
# ============================================================================

def create_kpi_card(title, value, subtitle="", icon="📊", color="primary", trend=None):
    """
    Create a professional KPI card component.
    
    Args:
        title (str): Card title
        value (str): Main metric value
        subtitle (str): Additional text
        icon (str): Icon/emoji
        color (str): Color key from COLORS config
        trend (str): Trend indicator (↑ or ↓)
        
    Returns:
        dbc.Card: Styled KPI card
    """
    card_color = COLORS.get(color, COLORS['primary'])
    
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            icon,
                            style={
                                'fontSize': '32px',
                                'marginBottom': SPACING['sm'],
                            }
                        ),
                        html.H4(
                            title,
                            style={
                                'color': COLORS['text_light'],
                                'fontSize': FONTS['size_sm'],
                                'fontWeight': '500',
                                'margin': '0 0 12px 0',
                                'letterSpacing': '0.5px',
                            }
                        ),
                        html.H2(
                            value,
                            style={
                                'color': COLORS['text_dark'],
                                'fontSize': FONTS['size_3xl'],
                                'fontWeight': '700',
                                'margin': '0 0 8px 0',
                            }
                        ),
                        html.Div(
                            [
                                html.Span(
                                    subtitle,
                                    style={
                                        'color': COLORS['text_lighter'],
                                        'fontSize': FONTS['size_xs'],
                                    }
                                ),
                                html.Span(
                                    f" {trend}" if trend else "",
                                    style={
                                        'color': card_color,
                                        'marginLeft': SPACING['sm'],
                                        'fontWeight': 'bold',
                                    }
                                ),
                            ]
                        ),
                    ],
                    style={
                        'padding': SPACING['lg'],
                    }
                )
            ],
            style={'padding': '0'}
        ),
        style={
            'border': 'none',
            'borderRadius': BORDER_RADIUS,
            'boxShadow': SHADOW['md'],
            'backgroundColor': COLORS['background'],
            'marginBottom': SPACING['lg'],
            'transition': 'all 0.3s ease',
            'borderLeft': f'4px solid {card_color}',
        },
        className='kpi-card-hover'
    )


# ============================================================================
# METRIC BADGE COMPONENT
# ============================================================================

def create_metric_badge(label, value, unit="", color="info"):
    """
    Create a small metric badge.
    
    Args:
        label (str): Badge label
        value (float): Metric value
        unit (str): Unit suffix
        color (str): Color key
        
    Returns:
        dbc.Badge: Styled badge
    """
    badge_color = COLORS.get(color, COLORS['info'])
    
    return html.Div(
        [
            html.Span(
                label,
                style={
                    'display': 'block',
                    'fontSize': FONTS['size_xs'],
                    'color': COLORS['text_light'],
                    'marginBottom': SPACING['xs'],
                }
            ),
            html.Span(
                f"{value:.2f}{unit}",
                style={
                    'display': 'block',
                    'fontSize': FONTS['size_lg'],
                    'fontWeight': '700',
                    'color': badge_color,
                }
            ),
        ],
        style={
            'padding': SPACING['md'],
            'backgroundColor': COLORS['surface'],
            'borderRadius': BORDER_RADIUS,
            'textAlign': 'center',
            'border': f'1px solid {COLORS["border"]}',
        }
    )


# ============================================================================
# SECTION HEADER COMPONENT
# ============================================================================

def create_section_header(title, subtitle="", action_button=None):
    """
    Create a professional section header.
    
    Args:
        title (str): Section title
        subtitle (str): Section subtitle
        action_button: Optional action button component
        
    Returns:
        dbc.Row: Section header
    """
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H3(
                        title,
                        style={
                            'color': COLORS['text_dark'],
                            'fontSize': FONTS['size_2xl'],
                            'fontWeight': '700',
                            'margin': f'0 0 {SPACING["sm"]} 0',
                        }
                    ),
                    html.P(
                        subtitle,
                        style={
                            'color': COLORS['text_light'],
                            'fontSize': FONTS['size_sm'],
                            'margin': '0',
                        }
                    ) if subtitle else None,
                ],
                md=8
            ),
            dbc.Col(
                action_button if action_button else html.Div(),
                md=4,
                className='text-end'
            ) if action_button else None,
        ],
        className='section-header',
        style={
            'marginBottom': SPACING['xl'],
            'paddingBottom': SPACING['lg'],
            'borderBottom': f'2px solid {COLORS["border"]}',
        }
    )


# ============================================================================
# UPLOAD COMPONENT
# ============================================================================

def create_upload_component():
    """
    Create a professional drag-and-drop upload component.
    
    Returns:
        dbc.Card: Upload area card
    """
    return dbc.Card(
        dbc.CardBody(
            dcc.Upload(
                id='csv-upload',
                children=html.Div(
                    [
                        html.Div(
                            '📤',
                            style={
                                'fontSize': '48px',
                                'marginBottom': SPACING['md'],
                            }
                        ),
                        html.H5(
                            'Drag and Drop CSV File Here',
                            style={
                                'color': COLORS['text_dark'],
                                'fontWeight': '600',
                                'margin': f'{SPACING["sm"]} 0',
                            }
                        ),
                        html.P(
                            'or click to select file',
                            style={
                                'color': COLORS['text_light'],
                                'margin': f'{SPACING["sm"]} 0 {SPACING["lg"]} 0',
                            }
                        ),
                        html.P(
                            'Supported format: CSV with transaction data',
                            style={
                                'color': COLORS['text_lighter'],
                                'fontSize': FONTS['size_xs'],
                                'margin': '0',
                            }
                        ),
                    ],
                    style={
                        'textAlign': 'center',
                        'padding': SPACING['xl'],
                    }
                ),
                style={
                    'width': '100%',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderColor': COLORS['border'],
                    'borderRadius': BORDER_RADIUS,
                    'textAlign': 'center',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease',
                },
                multiple=False,
            ),
            style={'padding': '0'}
        ),
        style={
            'border': 'none',
            'borderRadius': BORDER_RADIUS,
            'backgroundColor': COLORS['surface'],
            'transition': 'all 0.3s ease',
        },
        className='upload-card-hover'
    )


# ============================================================================
# RISK INDICATOR COMPONENT
# ============================================================================

def create_risk_indicator(risk_score, risk_level):
    """
    Create a professional risk level indicator.
    
    Args:
        risk_score (float): Risk score 0-100
        risk_level (str): Risk level (HIGH, MEDIUM, LOW)
        
    Returns:
        html.Div: Risk indicator
    """
    risk_colors = {
        'HIGH': COLORS['high_risk'],
        'MEDIUM': COLORS['medium_risk'],
        'LOW': COLORS['low_risk'],
    }
    
    risk_icons = {
        'HIGH': '⚠️',
        'MEDIUM': '⚡',
        'LOW': '✓',
    }
    
    color = risk_colors.get(risk_level, COLORS['text_light'])
    icon = risk_icons.get(risk_level, '•')
    
    return html.Div(
        [
            html.Span(
                icon,
                style={
                    'marginRight': SPACING['sm'],
                    'fontSize': '16px',
                }
            ),
            html.Span(
                f"{risk_level} - {int(risk_score)}",
                style={
                    'fontWeight': '600',
                    'color': color,
                }
            ),
        ],
        style={
            'display': 'flex',
            'alignItems': 'center',
            'padding': f'{SPACING["sm"]} {SPACING["md"]}',
            'backgroundColor': f'{color}15',  # 5% opacity
            'borderRadius': '8px',
            'border': f'1px solid {color}30',  # 20% opacity
            'width': 'fit-content',
        }
    )


# ============================================================================
# METRIC SUMMARY COMPONENT
# ============================================================================

def create_metric_summary(metrics_dict):
    """
    Create a summary metrics display panel.
    
    Args:
        metrics_dict (dict): Dictionary of metrics
        
    Returns:
        dbc.Row: Metrics summary row
    """
    cards = []
    metric_labels = {
        'accuracy': ('Accuracy', '%'),
        'precision': ('Precision', '%'),
        'recall': ('Recall', '%'),
        'f1_score': ('F1 Score', '%'),
        'roc_auc': ('ROC-AUC', ''),
    }
    
    for key, (label, unit) in metric_labels.items():
        if key in metrics_dict:
            value = metrics_dict[key]
            # Convert to percentage if needed
            display_value = f"{value*100:.2f}" if isinstance(value, float) and value <= 1 else f"{value:.4f}"
            
            cards.append(
                dbc.Col(
                    create_metric_badge(label, float(display_value.replace('%', '')), unit, 'info'),
                    md=6, lg=2, className='mb-3'
                )
            )
    
    return dbc.Row(cards, className='g-3')


# ============================================================================
# STATUS BADGE COMPONENT
# ============================================================================

def create_status_badge(status, label=""):
    """
    Create a status badge.
    
    Args:
        status (str): Status type (active, inactive, processing)
        label (str): Custom label
        
    Returns:
        html.Div: Status badge
    """
    status_colors = {
        'active': COLORS['success'],
        'inactive': COLORS['text_lighter'],
        'processing': COLORS['warning'],
        'fraud': COLORS['high_risk'],
        'legitimate': COLORS['low_risk'],
    }
    
    status_icons = {
        'active': '●',
        'inactive': '●',
        'processing': '⟳',
        'fraud': '⚠',
        'legitimate': '✓',
    }
    
    color = status_colors.get(status, COLORS['text_light'])
    icon = status_icons.get(status, '•')
    text = label if label else status.upper()
    
    return html.Span(
        [
            html.Span(icon, style={'marginRight': SPACING['xs'], 'color': color}),
            text,
        ],
        style={
            'color': color,
            'fontSize': FONTS['size_sm'],
            'fontWeight': '600',
        }
    )


# ============================================================================
# EMPTY STATE COMPONENT
# ============================================================================

def create_empty_state(title="No Data Available", subtitle="", icon="📊"):
    """
    Create an empty state placeholder.
    
    Args:
        title (str): Empty state title
        subtitle (str): Empty state subtitle
        icon (str): Icon/emoji
        
    Returns:
        html.Div: Empty state
    """
    return html.Div(
        [
            html.Div(
                icon,
                style={
                    'fontSize': '64px',
                    'marginBottom': SPACING['lg'],
                    'opacity': '0.5',
                }
            ),
            html.H4(
                title,
                style={
                    'color': COLORS['text_light'],
                    'fontWeight': '600',
                    'marginBottom': SPACING['sm'],
                }
            ),
            html.P(
                subtitle,
                style={
                    'color': COLORS['text_lighter'],
                    'fontSize': FONTS['size_sm'],
                }
            ),
        ],
        style={
            'textAlign': 'center',
            'padding': SPACING['2xl'],
            'backgroundColor': COLORS['surface'],
            'borderRadius': BORDER_RADIUS,
            'border': f'2px dashed {COLORS["border"]}',
        }
    )


# ============================================================================
# CUSTOM CSS STYLES
# ============================================================================

def get_custom_styles():
    """
    Get custom CSS styles for the application.
    
    Returns:
        str: CSS stylesheet
    """
    return """
    :root {
        --primary-color: """ + COLORS['primary'] + """;
        --text-dark: """ + COLORS['text_dark'] + """;
        --text-light: """ + COLORS['text_light'] + """;
        --background: """ + COLORS['background'] + """;
        --surface: """ + COLORS['surface'] + """;
        --border: """ + COLORS['border'] + """;
        --shadow-md: """ + SHADOW['md'] + """;
    }
    
    * {
        font-family: """ + FONTS['family'] + """;
    }
    
    body {
        background-color: """ + COLORS['surface'] + """;
        color: """ + COLORS['text_dark'] + """;
        margin: 0;
        padding: 0;
    }
    
    .kpi-card-hover:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
    }
    
    .upload-card-hover:hover {
        border-color: """ + COLORS['primary'] + """ !important;
        background-color: """ + COLORS['primary_light'] + """ !important;
    }
    
    .section-header {
        animation: slideInDown 0.3s ease;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .table-hover tbody tr:hover {
        background-color: """ + COLORS['primary_light'] + """ !important;
    }
    
    .btn-primary {
        background-color: """ + COLORS['primary'] + """;
        border-color: """ + COLORS['primary'] + """;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        background-color: """ + COLORS['primary_dark'] + """;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 82, 204, 0.3);
    }
    
    .btn-outline-primary {
        color: """ + COLORS['primary'] + """;
        border-color: """ + COLORS['border'] + """;
    }
    
    .btn-outline-primary:hover {
        background-color: """ + COLORS['primary_light'] + """;
        border-color: """ + COLORS['primary'] + """;
    }
    
    .alert-info {
        background-color: """ + COLORS['primary_light'] + """;
        border-color: """ + COLORS['primary'] + """;
        color: """ + COLORS['primary_dark'] + """;
    }
    
    .alert-success {
        background-color: """ + COLORS['secondary_light'] + """;
        border-color: """ + COLORS['secondary'] + """;
    }
    
    .alert-danger {
        background-color: rgba(198, 40, 40, 0.1);
        border-color: """ + COLORS['high_risk'] + """;
    }
    
    .text-muted {
        color: """ + COLORS['text_light'] + """ !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: """ + COLORS['text_dark'] + """;
        font-weight: 700;
    }
    
    .card {
        border: none;
        box-shadow: """ + SHADOW['md'] + """;
        border-radius: """ + BORDER_RADIUS + """;
        transition: all 0.3s ease;
    }
    
    .datatable-container {
        border: 1px solid """ + COLORS['border'] + """;
        border-radius: """ + BORDER_RADIUS + """;
        overflow: hidden;
    }
    """
