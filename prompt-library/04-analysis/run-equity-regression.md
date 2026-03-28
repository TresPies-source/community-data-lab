# Prompt: Run Equity Regression Analysis

## When to Use
When answering a research question of the form "Does X predict Y after controlling for income?"

## Context Block
```
I'm answering Research Question [number]: "[full question text]"

Data files available:
- data/[demographics].json — tract-level demographics keyed by GEOID
- data/[domain_data].json — tract-level [domain] data keyed by GEOID
- data/[outcome].json — [school/tract]-level outcome data

The independent variable is: [name] from [file] (field: [field_name])
The dependent variable is: [name] from [file] (field: [field_name])
The control variable is: median_income from [file] (field: median_income)
```

## Instruction Block
```
Write a Python script (stdlib only — use the math module for calculations) that:

1. Loads the data files and joins them on census tract GEOID
2. Filters out tracts with missing values for any of the three variables
3. Runs a 2-predictor OLS regression:
   - Y = a + b1*[independent_variable] + b2*median_income + error
4. Also computes:
   - Pearson correlation (r) between each pair of variables
   - Sample size (n tracts with complete data)
   - R-squared for the full model
   - R-squared for income-only model (to show what the independent variable adds)

5. Outputs a JSON file (data/rq_[name].json) containing:
   {
     "research_question": "[full text]",
     "method": "OLS two-predictor regression",
     "n_tracts": [number],
     "independent_variable": "[name]",
     "dependent_variable": "[name]",
     "control_variable": "median_income",
     "coefficients": {
       "intercept": [value],
       "independent": [value],
       "income": [value]
     },
     "r_squared_full": [value],
     "r_squared_income_only": [value],
     "r_squared_added": [value],  // what IV adds beyond income
     "correlations": {
       "iv_dv": [value],
       "income_dv": [value],
       "iv_income": [value]
     },
     "interpretation": "[1-2 sentence plain-English interpretation]",
     "policy_implication": "[what this means for the policy decision]"
   }

6. Includes a header comment documenting the RQ, data sources, and methodology

Constraints:
- Python stdlib only (math module for sqrt, sum operations)
- Implement OLS from scratch using normal equations: B = (X'X)^(-1) X'Y
- For 2x2 matrix inverse, direct formula is fine (no numpy needed)
- Report results honestly — a null finding (IV doesn't predict DV after income control) is a valid result
- If R-squared added is < 0.02, explicitly state that the independent variable has minimal additional explanatory power
```

## Quality Check
- Does the interpretation match the coefficients? (positive coefficient = positive relationship)
- Is the sample size sufficient? (< 30 tracts = underpowered, flag it)
- Is multicollinearity an issue? (if IV and income are correlated > 0.7, note this)
- Does the interpretation avoid causal language? (say "predicts" not "causes")
