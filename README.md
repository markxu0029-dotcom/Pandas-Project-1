# NSW Transport Demand Analysis

## Project overview
Briefly explain the two research questions.

## Data source
Transport for NSW Open Data Hub, with attribution and access date.

## Research questions
1. Which stations show the greatest absolute and relative variability?
2. What long-term trends, seasonal patterns and major disruptions are observable?

## Methods
- combined CSV files
- cleaned station/category labels
- replaced "Less than 50" with 25 as an estimated midpoint
- aggregated Entry + Exit into monthly station totals
- calculated mean, standard deviation, CV
- calculated network-wide monthly totals and rolling averages

## Key findings
- Town Hall and Central had the greatest absolute variability
- smaller/specialised stations had high relative variability
- demand dropped sharply during disruption period and recovered later
- January/April appeared lower than some regular months

## Limitations
- "Less than 50" values were estimated as 25
- monthly data cannot show weekday/weekend or peak-hour patterns
- regional classification was not included
- disruption period affects seasonality

## How to run
Install requirements and run the Python script.

## Outputs
Show or link final charts.
