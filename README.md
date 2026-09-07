# HR Analytics: Employee Segmentation and Workforce Intelligence

An end-to-end HR analytics project that transforms employee activity and workforce data into actionable employee segments, attrition-risk signals, and intervention recommendations. The repository contains the original Google Colab analysis, the trained clustering model, generated analytical outputs, SQL templates, and a Streamlit dashboard.

## Business Purpose

HR teams can use this project to:

- Understand the size and profile of each employee segment.
- Identify groups with elevated attrition risk.
- Compare salary, performance, engagement, workload, tenure, training, and absenteeism.
- Prioritize retention and workforce-development interventions by segment and department.
- Refresh an executive dashboard from the generated employee-level fact table.

## Current Findings

The generated dataset contains 14,999 employees across 10 departments. The clustering workflow evaluates four model clusters, which resolve to three effective business segments because two clusters share the `Stable Employees` label.

| Segment | Employees | Share | Attrition | Avg. satisfaction | Avg. overtime hours |
| --- | ---: | ---: | ---: | ---: | ---: |
| Emerging Talent | 9,368 | 62.5% | 17% | 6.52 | 189.61 |
| Needs Improvement | 4,224 | 28.2% | 45% | 5.15 | 226.88 |
| Stable Employees | 1,407 | 9.4% | 4% | 6.46 | 199.65 |

The highest-priority group is `Needs Improvement`: it combines the highest attrition rate, lowest satisfaction, and highest overtime level. Its recommended actions are retention interviews, compensation review, workload review, leadership development, and recognition programs.

## Repository Contents

```text
data/
	Employee_HR_data.csv                 Original employee dataset
models/
	employee_segmentation_model.pkl      Trained clustering model
results/
	employee_segmentation_results.csv    Streamlit-ready employee-level fact table
	cluster_profile.csv                  Cluster-level averages
	segment_details.csv                  Segment statistics
	segment_mapping.csv                  Cluster-to-segment labels
	attrition_risk_analysis.csv          Segment risk summary
	hr_recommendations.csv               Segment actions
	metadata.json                        Model and feature metadata
	*.png                                Exploratory and segmentation charts
sql/
	hr_analysis_queries.sql              Reusable analytical SQL queries
app.py                                  Streamlit HR analytics dashboard
requirements.txt                        Dashboard runtime dependencies
Employee_Segmentation.ipynb             Reproducible Google Colab workflow
```

## Analysis Workflow

1. Load and clean the employee dataset.
2. Engineer salary, workload, engagement, performance, tenure, and attrition features.
3. Detect outliers and use `RobustScaler` for clustering inputs.
4. Evaluate candidate K-Means cluster counts with inertia and silhouette score.
5. Train the final four-cluster K-Means model with `random_state=42`.
6. Map model clusters to business-friendly segment names.
7. Calculate segment profiles, attrition risk, recommendations, and PCA outputs.
8. Export the results consumed by the Streamlit dashboard.

The canonical dashboard source is `results/employee_segmentation_results.csv`, not the original raw CSV. It contains the engineered features and final `Segment` label required by the app.

## Streamlit Dashboard

Run the dashboard locally with:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app follows the supplied dashboard reference with a dark teal canvas, compact navigation rail, KPI tiles, segment distribution, attrition-risk analysis, department comparison, workload/performance analysis, filters, and an adaptive recommendations panel.

## Making the Dashboard Permanently Live

The simplest hosting option is Streamlit Community Cloud:

1. Push this repository to GitHub.
2. Open [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Select `rsdina/Employee_Segmentation`, branch `main`, and file `app.py`.
4. Deploy the app. Streamlit installs packages from `requirements.txt` and reads the committed result CSV.
5. Share the generated public or private app URL.

For a private production deployment, use Streamlit Community Cloud private sharing, Streamlit Enterprise, or deploy the same app to an organization-managed container platform. Employee-level HR data should not be exposed through a public URL.

The current app is a static snapshot of the committed analysis results. To refresh it, replace the result CSV through the analysis pipeline and push the updated file; Streamlit Cloud will redeploy from GitHub. For automated refresh, move the data source to a database or scheduled pipeline and update `app.py` to query it.

## Reproducing the Analysis

Open `Employee_Segmentation.ipynb` in Google Colab or VS Code with Python and run the cells in order. The notebook exports the generated files under `results/` and the model under `models/`.

Core Python packages:

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
```

## Data Notes

- `Attrition` is the engineered binary attrition field used for risk measures.
- `Employee_Satisfaction`, `Performance_Rating`, `Annual_Salary`, and other engineered fields are sourced from the transformed fact table.
- The source field names in `data/Employee_HR_data.csv` differ from the engineered names in the result table.
- The legacy SQL contains example segment names that do not all occur in the current generated output. Use the actual `Segment` values in `results/employee_segmentation_results.csv` when building the report.
- Employee-level HR data may contain sensitive information. Restrict repository, workspace, dataset, and report permissions accordingly.

## License and Ownership

This repository is maintained by `rsdina`. Add an explicit license before distributing the dataset or model outside the intended organization.
