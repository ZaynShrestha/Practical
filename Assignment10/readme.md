# 🧩 Feature Engineering & Preprocessing Experiments

This repository documents a series of machine learning preprocessing and feature engineering experiments (Task‑1 to Task‑4). Each task demonstrates a different aspect of preparing data for modeling, with code, decisions, and results.

---

## 📌 Task‑1: Full Feature Preparation Pipeline
**Goal:** Apply a complete preprocessing pipeline to a dataset with mixed types and nulls.

### Steps
1. **Drop low‑value columns** (IDs, timestamps) → no predictive value.
2. **Impute missing values**  
   - Numerics → median (robust to outliers)  
   - Categoricals → mode (most frequent)
3. **Encode categoricals**  
   - Nominal → One‑Hot Encoding  
   - Ordinal → Ordinal Encoding
4. **Scale numerics** → StandardScaler (mean=0, variance=1).
5. **Train‑test split** → 80/20 with stratification.

### Output
- Clean `X_train`, `X_test`, `y_train`, `y_test`
- Documented justification for each decision.

---

## 📌 Task‑2: Feature Engineering Challenge
**Goal:** Engineer new features from a datetime‑rich dataset and compare model accuracy before vs after.

### Engineered Features
- `day_of_week`, `hour`, `is_weekend` (from timestamp)
- `fare_per_km` (ratio), `fare_x_duration` (interaction)
- `log_fare` (log transform of skewed numeric)
- `distance_bin` (binned continuous variable)

### Results
- Baseline Logistic Regression trained on raw features.  
- Accuracy improved after adding engineered features.  
- **Takeaway:** Engineered features capture hidden temporal and behavioral patterns, boosting predictive power.

---

## 📌 Task‑3: Encoding Strategy Comparison
**Goal:** Compare Label Encoding, One‑Hot Encoding, and Ordinal Encoding on categorical columns of varying cardinality.

### Experiment
- Dataset with low, medium, and high cardinality categorical features.
- Logistic Regression trained on each encoding strategy.
- Metrics: Accuracy, training time, feature count.

### Results
| Strategy          | Accuracy | Train Time | Feature Count |
|-------------------|----------|------------|---------------|
| Label Encoding    | Lower    | Fast       | Few features  |
| One‑Hot Encoding  | Highest  | Moderate   | Many features |
| Ordinal Encoding  | Moderate | Fast       | Few features  |

**Recommendation:**  
Use **One‑Hot Encoding** for low/medium cardinality features to maximize accuracy. For very high cardinality, consider target encoding or embeddings to avoid feature explosion.

---

## 📌 Task‑4: Scaler Sensitivity Experiment
**Goal:** Test KNN and SVM performance with different scalers, before and after injecting outliers.

### Scalers Tested
- None (raw data)
- StandardScaler
- MinMaxScaler
- RobustScaler

### Results
- Without scaling → poor accuracy (large‑scale features dominate).
- StandardScaler & MinMaxScaler → improved accuracy but sensitive to outliers.
- RobustScaler → stable accuracy even after injecting extreme outliers.

### Visualization
Grouped bar charts show accuracy by scaler for both baseline and outlier datasets.

### Conclusion
Scaling is essential for KNN and SVM.  
- **RobustScaler** is most resilient to outliers.  
- **StandardScaler/MinMaxScaler** work well when outliers are rare or pre‑handled.  
- Always test multiple scalers to find the best fit for your dataset.

---

## 🚀 Practical Takeaways
- **Task‑1:** Build a systematic preprocessing pipeline.  
- **Task‑2:** Engineer features to capture hidden patterns.  
- **Task‑3:** Choose encoding strategies based on cardinality.  
- **Task‑4:** Select scalers carefully, especially with outliers.

---

## 📂 Repository Structure
- `task1_pipeline.ipynb` → Full preprocessing pipeline  
- `task2_feature_engineering.ipynb` → Feature engineering challenge  
- `task3_encoding_comparison.ipynb` → Encoding strategies comparison  
- `task4_scaler_experiment.ipynb` → Scaler sensitivity experiment  

---

## 📝 Author
Developed by Simran, Kathmandu, Nepal.  
Focused on **data preprocessing, feature engineering, and ML experimentation**.
