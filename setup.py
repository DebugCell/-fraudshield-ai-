# ============================================================================
# FraudShield AI - Setup Configuration
# ============================================================================
# Installation configuration for pip install

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fraudshield-ai",
    version="1.0.0",
    author="FraudShield AI Team",
    author_email="dev@fraudshield.ai",
    description="Enterprise Credit Card Fraud Detection & Risk Analytics Dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fraudshield-ai/fraud-detection-dashboard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dash>=2.14.2",
        "plotly>=5.18.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.3.0",
        "imbalanced-learn>=0.11.0",
        "dash-bootstrap-components>=1.5.0",
        "gunicorn>=21.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fraudshield=run:main",
        ],
    },
    project_urls={
        "Documentation": "https://github.com/fraudshield-ai/fraud-detection-dashboard",
        "Source": "https://github.com/fraudshield-ai/fraud-detection-dashboard",
        "Tracker": "https://github.com/fraudshield-ai/fraud-detection-dashboard/issues",
    },
)
