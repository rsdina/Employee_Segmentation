# HR Analytics: Employee Segmentation and Workforce Intelligence

An end-to-end HR analytics project that transforms employee activity and workforce data into actionable employee segments, attrition-risk signals, and intervention recommendations. The repository contains the original Google Colab analysis, the trained clustering model, generated analytical outputs, SQL templates, and a Power BI dashboard specification.

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
	employee_segmentation_results.csv    Power BI-ready employee-level fact table
	cluster_profile.csv                  Cluster-level averages
	segment_details.csv                  Segment statistics
	segment_mapping.csv                  Cluster-to-segment labels
	attrition_risk_analysis.csv          Segment risk summary
	hr_recommendations.csv               Segment actions
	metadata.json                        Model and feature metadata
	*.png                                Exploratory and segmentation charts
sql/
	hr_analysis_queries.sql              Reusable analytical SQL queries
powerbi/
	HR_Analytics_Dashboard_Spec.md       Page, visual, and DAX build specification
	HR_Analytics_Theme.json              Theme matching the supplied dashboard reference
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
8. Export the results consumed by Power BI.

The canonical dashboard source is `results/employee_segmentation_results.csv`, not the original raw CSV. It contains the engineered features and final `Segment` label required by the report.

## Power BI Dashboard

The dashboard implementation guide is in [powerbi/HR_Analytics_Dashboard_Spec.md](powerbi/HR_Analytics_Dashboard_Spec.md). It defines a single-page executive dashboard inspired by the supplied reference image:

- Dark teal workspace with a compact left navigation rail.
- KPI tiles for workforce size, attrition, average salary, and engagement.
- Segment distribution and attrition-risk visuals.
- Department comparison and workload/performance analysis.
- A recommendation panel that responds to the selected segment.
- Slicers for department, segment, attrition, and employee profile.

Import [powerbi/HR_Analytics_Theme.json](powerbi/HR_Analytics_Theme.json) in Power BI Desktop before creating visuals. Use `results/employee_segmentation_results.csv` as the main table and set `EmpId` to Text or Whole Number consistently across the model.

## Making the Dashboard Live

Power BI Desktop is required to create the report, and Power BI Service is required to keep it accessible online. A local path such as `D:\HR_Segmentation_result` cannot be used as a permanently refreshing cloud source by itself.

Recommended deployment:

1. Build the report in Power BI Desktop using the dashboard specification.
2. Publish the report and semantic model to a Power BI workspace backed by Power BI Pro, Premium Per User, or Fabric capacity.
3. Store the CSV in SharePoint/OneDrive or load it into a supported database for a cloud-stable source.
4. Configure dataset credentials and scheduled refresh in the Power BI Service.
5. Configure row-level security if the report will expose employee-level records.
6. Share the report through an app or workspace with the intended HR audience.
7. Pin the report to a dashboard or embed it in the organization portal.

For a static snapshot, publishing the imported dataset is sufficient. For ongoing updates, use SharePoint/OneDrive or a database; a local-file gateway is possible but requires a continuously available gateway machine and is less resilient.

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
