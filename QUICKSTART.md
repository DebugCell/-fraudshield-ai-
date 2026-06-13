# 🚀 FraudShield AI - Quick Start Guide

## For the Impatient (5 Minutes Setup)

### Option 1: Direct Python (Easiest)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py

# 3. Open browser and go to:
# http://localhost:8050
```

### Option 2: Using the Launcher Script

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run launcher
python run.py

# 3. Open browser to: http://localhost:8050
```

### Option 3: Docker (Best for Production)

```bash
# 1. Build Docker image
docker build -t fraudshield-ai .

# 2. Run container
docker run -p 8050:8050 fraudshield-ai

# 3. Open browser to: http://localhost:8050
```

### Option 4: Docker Compose (Recommended)

```bash
# 1. Start everything
docker-compose up -d

# 2. View logs (optional)
docker-compose logs -f

# 3. Open browser to: http://localhost:8050

# Stop when done
docker-compose down
```

---

## First Steps in the Dashboard

1. **Load Sample Data**
   - Click "🔄 Load Sample Data" button
   - Wait for model training (may take 30-60 seconds)
   - Watch the dashboard populate automatically

2. **Explore Analytics**
   - View KPI cards at the top
   - Scroll through analytics charts
   - Check fraud distribution
   - Review transaction details

3. **Analyze Transactions**
   - Search transactions by ID
   - View risk scores
   - See high-risk transactions in Risk Intelligence panel

4. **Check Model Performance**
   - View accuracy, precision, recall metrics
   - Check ROC curve
   - Review feature importance

5. **Export Results**
   - Download fraud transactions as CSV
   - Download full analysis report

---

## Troubleshooting

### Port 8050 Already in Use?
```bash
# Windows
netstat -ano | findstr :8050
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8050
kill -9 <PID>
```

### Missing Dependencies?
```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt
```

### Docker Issues?
```bash
# Clean up Docker
docker system prune -a
docker-compose down -v

# Rebuild
docker-compose up --build
```

---

## Features You Can Try

✅ **Upload Your Own Data**
   - CSV format with 31 columns (Time, V1-V28, Amount, Class)
   - Click upload zone to select file

✅ **Real-time Predictions**
   - Transactions scored automatically
   - Risk levels (HIGH, MEDIUM, LOW)
   - Confidence scores 0-100

✅ **Interactive Charts**
   - Hover over any chart for details
   - Download chart as PNG
   - Zoom and pan capabilities

✅ **Transaction Search**
   - Find transactions by ID
   - Filter by amount or date
   - Sort by risk score

✅ **Export Analysis**
   - CSV of fraud transactions
   - PDF report generation
   - Summary statistics

---

## System Requirements

- **Python**: 3.8+
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB
- **Browser**: Chrome, Firefox, Safari, Edge (modern versions)

---

## Performance Tips

- **Faster Loading**: Use smaller datasets (< 100K rows)
- **Better Performance**: Increase RAM for large datasets
- **Smooth UI**: Use modern browser with hardware acceleration

---

## Need More Help?

1. Check **README.md** for detailed documentation
2. Review **config.py** to customize colors/styling
3. Edit **utils.py** to change ML model parameters
4. Modify **components.py** to adjust UI elements

---

## Production Deployment

For production use:

```bash
# Use Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8050 app:server

# Or with Docker Compose
docker-compose up -d

# Monitor logs
docker-compose logs -f
```

---

**Enjoy FraudShield AI!** 🛡️

Questions? Check the documentation or review the code comments.
