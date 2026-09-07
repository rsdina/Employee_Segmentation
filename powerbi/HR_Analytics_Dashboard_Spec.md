# HR Analytics Dashboard Specification

This specification turns the generated employee segmentation results into a Power BI report styled after the supplied dashboard reference. It is deliberately implementation-ready: the table, measures, visual types, filters, interactions, and deployment choices are defined below.

## 1. Data Model

Use Import mode with one primary table:

- Table: `EmployeeSegmentation`
- Source: `results/employee_segmentation_results.csv`
- Grain: one row per employee
- Key: `EmpId`
- Numeric fields: `Annual_Salary`, `Employee_Satisfaction`, `Performance_Rating`, `Company_Tenure`, `Overtime_Hours`, `Attrition`, `Age`, `Training_Hours`, `Absenteeism_Days`, `Engagement_Index`, `Performance_Index`, `number_of_projects`
- Categories: `Department`, `Segment`, `Cluster`, `Promotion`, `work_accident`

Set `EmpId` to Text or Whole Number consistently. Mark `EmpId` as Do not summarize. Set `Attrition` to Decimal Number and format the attrition measures as percentages.

The result table contains three business segments:

- `Emerging Talent`
- `Needs Improvement`
- `Stable Employees`

The model has four clusters, but clusters 0 and 2 both map to `Stable Employees`. Use `Segment` for executive visuals and `Cluster` only for model diagnostics.

## 2. DAX Measures

Create these measures in `EmployeeSegmentation`:

```DAX
Employee Count =
DISTINCTCOUNT ( EmployeeSegmentation[EmpId] )

Attrition Rate =
AVERAGE ( EmployeeSegmentation[Attrition] )

Average Salary =
AVERAGE ( EmployeeSegmentation[Annual_Salary] )

Average Satisfaction =
AVERAGE ( EmployeeSegmentation[Employee_Satisfaction] )

Average Performance =
AVERAGE ( EmployeeSegmentation[Performance_Rating] )

Average Overtime Hours =
AVERAGE ( EmployeeSegmentation[Overtime_Hours] )

Average Tenure =
AVERAGE ( EmployeeSegmentation[Company_Tenure] )

Average Absenteeism =
AVERAGE ( EmployeeSegmentation[Absenteeism_Days] )

At Risk Employees =
CALCULATE (
    [Employee Count],
    EmployeeSegmentation[Attrition] = 1
)

Segment Share =
DIVIDE (
    [Employee Count],
    CALCULATE ( [Employee Count], ALLSELECTED ( EmployeeSegmentation[Segment] ) )
)

Risk Score =
VAR AttritionComponent = [Attrition Rate] * 10
VAR SatisfactionComponent = DIVIDE ( 10 - [Average Satisfaction], 10 ) * 3
VAR OvertimeComponent = DIVIDE ( [Average Overtime Hours], 310 ) * 2
VAR AbsenteeismComponent = DIVIDE ( [Average Absenteeism], 4 ) * 1
RETURN
    ROUND (
        AttritionComponent
            + SatisfactionComponent
            + OvertimeComponent
            + AbsenteeismComponent,
        2
    )

Priority Label =
VAR CurrentRisk = [Risk Score]
RETURN
    SWITCH (
        TRUE (),
        CurrentRisk >= 7, "Immediate intervention",
        CurrentRisk >= 5, "Monitor and support",
        "Stable"
    )
```

Recommended formats:

- `Employee Count`, `At Risk Employees`: `#,##0`
- `Attrition Rate`, `Segment Share`: `0.0%`
- `Average Salary`: currency with zero decimals
- `Average Satisfaction`, `Average Performance`: `0.00`
- `Average Overtime Hours`, `Average Tenure`, `Average Absenteeism`: `0.0`
- `Risk Score`: `0.00`

## 3. Executive Page Layout

Use a 16:9 page with a dark teal background (`#102E3A`) and a thin magenta accent (`#B72D8C`). Import `HR_Analytics_Theme.json` first.

### Header

- Left: `HR ANALYTICS` in uppercase with a small subtitle `WORKFORCE INTELLIGENCE`.
- Center: page title `Employee Segmentation Overview`.
- Right: refresh date and a compact report-status indicator.

### Left Navigation Rail

Create a narrow, unframed vertical rail with these page buttons:

- Overview
- Segments
- Attrition Risk
- Departments
- Recommendations

Use page navigator buttons, not decorative text. Keep the rail visually quiet so the report remains usable on smaller screens.

### KPI Tiles

Place four equal tiles across the top content area:

1. `Employee Count` with `[Employee Count]`.
2. `Attrition Rate` with `[Attrition Rate]` and bad-color conditional formatting.
3. `Average Salary` with `[Average Salary]`.
4. `Average Satisfaction` with `[Average Satisfaction]`.

Use small labels, large callout numbers, and a 2 px cyan top border. Avoid rounded cards inside other cards.

### Main Visuals

Place these visuals below the KPI row:

- **Segment distribution:** donut chart with `Segment` as legend and `[Employee Count]` as values. Use cyan, coral, and magenta in that order.
- **Attrition risk by segment:** clustered bar chart with `Segment` on the axis and `[Attrition Rate]` as values. Sort descending and use conditional colors: green below 15%, amber from 15% to 25%, coral above 25%.
- **Department workforce:** horizontal bar chart with `Department` and `[Employee Count]`, with `Segment` as a small-multiple or legend option.
- **Workload versus performance:** scatter chart with `Average Overtime Hours` on X, `Average Performance` on Y, `[Employee Count]` as size, and `Segment` as legend.
- **Segment profile:** matrix with `Segment` as rows and `[Employee Count]`, `[Average Salary]`, `[Average Satisfaction]`, `[Average Performance]`, `[Attrition Rate]`, and `[Risk Score]` as values.

### Recommendations Panel

Use a narrow right-side panel with a selected segment card:

- Selected segment name.
- `[Priority Label]`.
- `[Risk Score]`.
- `[Average Overtime Hours]` and `[Average Satisfaction]`.
- A text box populated from `results/hr_recommendations.csv` or a small related recommendations table.

For the initial default view, select `Needs Improvement` so the report opens on the highest-priority intervention group.

## 4. Slicers and Interactions

Add compact slicers at the top or in a collapsible filter pane:

- `Department`
- `Segment`
- `Cluster`
- `Attrition`
- `Age`
- `Company_Tenure`

Enable cross-filtering from the segment donut, attrition bar, department bar, and matrix. Use a Reset Filters bookmark. Keep drill-through to a detail page on `EmpId` available only to authorized HR users.

## 5. Optional Detail Pages

### Segment Detail

Use a segment slicer and show:

- Segment profile cards.
- Salary, satisfaction, performance, overtime, and absenteeism comparisons.
- A department-by-segment matrix.
- A scatter chart of satisfaction versus performance.

### Attrition Risk

Show:

- Risk score by segment.
- Attrition rate by department.
- At-risk employee count.
- Overtime and absenteeism comparison.
- A recommendation table.

### Employee Detail

Show a searchable table with `EmpId`, `Department`, `Segment`, `Annual_Salary`, `Performance_Rating`, `Employee_Satisfaction`, `Overtime_Hours`, `Absenteeism_Days`, and `Attrition`. Apply row-level security before sharing this page.

## 6. Refresh and Permanent Availability

A report is permanently viewable only when it is published to Power BI Service and hosted in a licensed workspace. For durable refresh:

1. Put the CSV and any recommendation lookup table in SharePoint/OneDrive, or load them into a database.
2. Replace the local file path with that cloud or database source in Power Query.
3. Publish the report to a workspace backed by Pro, Premium Per User, or Fabric capacity.
4. Configure credentials, refresh frequency, failure notifications, and ownership.
5. Use a workspace app or secure embed link for HR consumers.
6. Add row-level security if employee-level details are exposed.

A local `D:` drive is acceptable for a one-time import but is not a permanent cloud refresh source unless a continuously available on-premises gateway is configured.

## 7. Acceptance Checklist

- [ ] Theme imported and report background matches the reference palette.
- [ ] Main table loads 14,999 rows.
- [ ] KPI cards show 14,999 employees and approximately 24% attrition before filters.
- [ ] `Needs Improvement` shows approximately 45% attrition and 226.88 average overtime hours.
- [ ] Segment and department slicers cross-filter every main visual.
- [ ] Reset Filters bookmark works.
- [ ] Recommendations update with the selected segment.
- [ ] Report is published to Power BI Service.
- [ ] Refresh succeeds from a cloud-stable source.
- [ ] Access permissions and row-level security are reviewed by the HR data owner.
