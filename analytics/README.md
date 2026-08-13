# Analytics Module

This module contains the EDA and machine learning analysis of the Titanic dataset.

## Files

- `01_eda.ipynb` - Data cleaning, analysis, charts and written interpretations
- `02_modeling.ipynb` - Preprocessing, machine learning models and evaluation
- `titanic.csv` - Offline copy of the dataset
- `best_model_pipeline.joblib` - Saved complete model pipeline

## Data Cleaning

Missing values found:

| Column | Missing % | Action |
|---|---:|---|
| age | 19.87% | Median imputation |
| embarked | 0.22% | Dropped rows |
| deck | 77.22% | Dropped column |
| embark_town | 0.22% | Dropped rows |

After cleaning, the dataset contains **889 rows and 14 columns**.

## EDA

The analysis showed that female passengers had higher survival rates than males, and first-class passengers had better survival rates than lower classes. Fare was right-skewed, with a small number of passengers paying much higher fares.

The notebooks contain the required charts, correlation analysis, outlier analysis, standardization check, and written interpretations for the multivariate data story.

## Classification

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.781 | 0.754 | 0.632 | 0.688 | 0.826 |
| Decision Tree | 0.770 | 0.714 | 0.662 | 0.687 | 0.741 |
| Random Forest | 0.803 | 0.780 | 0.676 | 0.724 | 0.826 |

Random Forest gave the best overall classification result.

The tuned Random Forest achieved an **OOB score of 0.807**.

## Imbalance Handling

Normal, balanced class weights and SMOTE were compared. The balanced approach gave the highest F1 score of **0.727** among the three approaches.

## Regression

Linear Regression was used to predict fare.

- MAE: **18.374**
- RMSE: **41.292**
- R²: **0.361**
- Adjusted R²: **0.297**

The residual plot showed a larger spread at higher predicted fares, suggesting **heteroscedasticity**.

## Final Recommendation

Random Forest was selected as the final classifier because it achieved the highest test accuracy (**0.803**) and F1 score (**0.724**). The complete preprocessing and model pipeline was saved as `best_model_pipeline.joblib` and successfully reloaded and tested.