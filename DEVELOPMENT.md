# 🛠️ Development Guide

## Local Development Setup

### Prerequisites
- Python 3.9+
- Git
- Virtual environment manager (venv recommended)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/customer_churn_prediction.git
cd customer_churn_prediction
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Development Server
```bash
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## Project Structure

```
customer_churn_prediction/
├── app.py                    # Main Streamlit application (700+ lines)
├── create_model.py          # Model creation/training script
├── churn_model.pkl          # Trained Random Forest model
├── model_columns.pkl        # Feature column names/order
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker containerization
├── docker-compose.yml       # Docker Compose configuration
├── .streamlit/
│   ├── config.toml         # Streamlit configuration
│   ├── secrets.toml.example # Secrets template (DO NOT COMMIT)
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── DEPLOYMENT.md           # Deployment guide
└── DEVELOPMENT.md          # This file
```

---

## Code Structure (app.py)

### Section 1: Configuration & Imports
- Page config setup
- Model loading with caching
- Data loading utilities

### Section 2: Sidebar Navigation
- Page selection radio button
- Model metrics display
- Navigation styling

### Section 3: Home Page
- Platform overview
- Feature highlights
- Quick start guide
- KPI cards

### Section 4: Customer Prediction Page
- Input form with 18+ fields
- Categorical/numeric inputs
- Prediction logic
- Results visualization
- Business recommendations

### Section 5: Analytics Dashboard
- KPI metrics
- Churn distribution chart
- Contract vs Churn analysis
- Payment method analysis
- Monthly charges distribution
- Feature importance ranking

### Section 6: Business Insights
- Top churn drivers
- Key findings
- Strategic recommendations
- Business impact analysis

### Section 7: About Project
- Dataset information
- Preprocessing details
- Model specifications
- Technology stack
- Deployment info

---

## Adding New Features

### Example 1: Add a New Analytics Chart

```python
# In Analytics Dashboard section
with col1:
    st.markdown("### 📊 New Chart Title")
    
    # Your data preparation
    data = sample_df.groupby('category').size()
    
    # Create visualization
    fig = px.bar(x=data.index, y=data.values)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
```

### Example 2: Add a New Prediction Input

```python
# In Customer Prediction section
with col1:
    new_feature = st.selectbox(
        "New Feature Label",
        ["Option1", "Option2", "Option3"],
        key="unique_key"
    )
    
# In prediction preparation
input_data['new_feature'] = 1 if new_feature == "Option1" else 0
```

### Example 3: Add Database Integration

```python
import sqlite3

@st.cache_resource
def get_db_connection():
    return sqlite3.connect('predictions.db')

# Save prediction
conn = get_db_connection()
conn.execute("""
    INSERT INTO predictions (customer_id, probability, timestamp)
    VALUES (?, ?, ?)
""", (customer_id, probability, datetime.now()))
conn.commit()
```

---

## Model Development

### Retraining the Model

1. **Prepare Training Data**
   ```python
   # Load your telco dataset (CSV format)
   data = pd.read_csv('telco_churn_data.csv')
   ```

2. **Preprocessing**
   ```python
   from sklearn.preprocessing import StandardScaler, LabelEncoder
   from imblearn.over_sampling import SMOTE
   
   # Encode categorical features
   le = LabelEncoder()
   data['gender'] = le.fit_transform(data['gender'])
   
   # Scale numerical features
   scaler = StandardScaler()
   numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
   data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
   
   # Handle imbalance
   smote = SMOTE(random_state=42)
   X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
   ```

3. **Train Model**
   ```python
   from sklearn.ensemble import RandomForestClassifier
   
   model = RandomForestClassifier(
       n_estimators=100,
       max_depth=15,
       random_state=42,
       class_weight='balanced',
       n_jobs=-1
   )
   
   model.fit(X_resampled, y_resampled)
   ```

4. **Evaluate**
   ```python
   from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
   
   y_pred = model.predict(X_test)
   
   print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
   print(f"Precision: {precision_score(y_test, y_pred):.2%}")
   print(f"Recall: {recall_score(y_test, y_pred):.2%}")
   print(f"F1-Score: {f1_score(y_test, y_pred):.2%}")
   ```

5. **Save Model**
   ```python
   import joblib
   
   joblib.dump(model, 'churn_model.pkl')
   joblib.dump(X_train.columns.tolist(), 'model_columns.pkl')
   ```

---

## Testing

### Manual Testing Checklist

#### Home Page
- [ ] Page loads without errors
- [ ] All KPI cards display correctly
- [ ] Links in Quick Start work
- [ ] Layout is responsive

#### Customer Prediction
- [ ] All 18+ input fields are accessible
- [ ] Form validation works
- [ ] Prediction generates results
- [ ] Risk level colors are correct
- [ ] Recommendation displays properly

#### Analytics Dashboard
- [ ] All charts render correctly
- [ ] KPI metrics display accurately
- [ ] Charts are interactive
- [ ] Performance is acceptable

#### Business Insights
- [ ] All insights display properly
- [ ] Formatting is correct
- [ ] Recommendations are clear

#### About Project
- [ ] All information is accurate
- [ ] Links work properly
- [ ] Technical details are clear

### Automated Testing

```python
# tests/test_app.py
import streamlit as st
from streamlit.testing.v1 import AppTest

def test_home_page():
    at = AppTest.from_file("app.py").run()
    assert "Customer Churn Prediction" in at.title

def test_prediction():
    at = AppTest.from_file("app.py").run()
    # Simulate user input
    assert at.success  # No errors
```

---

## Performance Optimization

### Caching Strategies

```python
# Best: Cache entire session
@st.cache_resource
def load_model_and_columns():
    model = joblib.load("churn_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

# Good: Cache data for duration of session
@st.cache_data
def load_sample_data():
    return pd.read_csv("sample_data.csv")

# Use: Cache with parameters
@st.cache_data
def process_customer_data(customer_id: int):
    return fetch_and_process(customer_id)
```

### Performance Profiling

```bash
# Install profiler
pip install streamlit-profiler

# Use in app
import streamlit_profiler
streamlit_profiler.profile_this()
```

---

## Styling & Customization

### Streamlit Theming

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#31333f"
font = "sans serif"
```

### Custom CSS (Markdown HTML)

```python
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)
```

---

## Debugging

### Enable Debug Mode
```bash
# Run with debug logging
streamlit run app.py --logger.level=debug
```

### Use Print Statements (Viewer Console)
```python
print(f"DEBUG: variable_name = {variable_name}")
# Check browser console for output
```

### Use st.write() for Inspection
```python
st.write("DEBUG:", df.head())
st.write("Shape:", df.shape)
```

---

## Dependencies Management

### Update Dependencies
```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade pandas

# Update all
pip install --upgrade -r requirements.txt

# Save new requirements
pip freeze > requirements.txt
```

### Managing Conflicting Dependencies
```bash
# Check dependency tree
pip install pipdeptree
pipdeptree

# Resolve conflicts
pip install -r requirements.txt --force-reinstall
```

---

## Git Workflow

### Feature Development
```bash
# Create feature branch
git checkout -b feature/new-analytics-chart

# Make changes
git add .
git commit -m "Add new analytics chart for contract analysis"

# Push to GitHub
git push origin feature/new-analytics-chart

# Create pull request on GitHub
```

### Commit Message Guidelines
```
feat: Add new customer segmentation feature
fix: Correct churn probability calculation
docs: Update API documentation
style: Format code with black
refactor: Simplify prediction logic
test: Add unit tests for preprocessing
chore: Update dependencies
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

---

## Common Issues & Solutions

### Issue: Cache Not Clearing
```python
# Clear cache
st.cache_data.clear()
st.cache_resource.clear()

# Or: Clear browser cache
# Settings > Privacy > Clear Browsing Data
```

### Issue: Model Predictions Not Changing
```python
# Check if input data is being mapped correctly
st.write("DEBUG: input_df =", input_df)

# Verify column order matches training
st.write("Expected columns:", model_columns)
st.write("Provided columns:", input_df.columns.tolist())
```

### Issue: Charts Not Displaying
```python
# Use st.plotly_chart with use_container_width=True
st.plotly_chart(fig, use_container_width=True)

# Check for empty data
if df.empty:
    st.warning("No data available for chart")
else:
    st.plotly_chart(fig)
```

---

## Resources for Developers

- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Plotly Documentation](https://plotly.com/python/)
- [Scikit-learn Guide](https://scikit-learn.org/stable/user_guide.html)
- [Python Best Practices](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Code Style

### Format Code with Black
```bash
pip install black
black app.py

# Or check without modifying
black --check app.py
```

### Lint with Pylint
```bash
pip install pylint
pylint app.py
```

---

## Documentation Standards

### Function Documentation
```python
def make_prediction(input_df: pd.DataFrame) -> tuple:
    """
    Make churn prediction for a customer.
    
    Args:
        input_df: DataFrame with customer features
        
    Returns:
        Tuple of (prediction, probability)
        
    Raises:
        ValueError: If input data is invalid
    """
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]
    return prediction, probability
```

---

<div align="center">

**Happy Developing! 🚀**

Questions? Open an issue or start a discussion!

</div>
