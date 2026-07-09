# Sydney Transport Demand Analysis

## Overview

This project analyses monthly station entry/exit data from the NSW Opal-enabled rail/metro network between July 2016 and October 2024.

The project explores two questions:

1. Which stations show the greatest absolute and relative variability in monthly total usage?
2. What long-term trends, seasonal patterns and major disruptions are observable in monthly transport demand?

## Tools

- Python
- pandas
- matplotlib

## Data preparation

The workflow includes:

- reading and combining multiple CSV files;
- cleaning column names and station/category labels;
- converting monthly date values into datetime format;
- handling "Less than 50" values by estimating them as 25;
- preserving suppressed values using a Boolean flag;
- aggregating Entry and Exit records into monthly station-level total usage.

## Methods

For station-level variability, the project calculates:

- mean monthly total usage;
- standard deviation, used as absolute variability;
- coefficient of variation, used as relative variability;
- number of observed months per station.

For network-level demand, the project calculates:

- monthly total usage across all stations;
- 12-month rolling average;
- average demand by calendar month;
- average demand across broad pre-disruption, disruption and recovery periods.

## Key findings

- Major high-volume stations such as Town Hall, Central and Wynyard showed the greatest absolute variability in monthly total usage.
- Relative variability highlighted smaller or more specialised stations whose usage fluctuated strongly compared with their own average usage.
- Network-wide monthly demand fell sharply during the disruption period and gradually recovered from 2022 onward.
- Calendar-month averages suggest seasonal variation, although these patterns should be interpreted cautiously because the dataset includes major disruption years.

## Limitations

- Values reported as "Less than 50" were estimated as 25, which may affect low-usage stations.
- The analysis uses monthly data, so it cannot identify weekday/weekend patterns, peak-hour demand, or individual event effects.
- The dataset focuses on Opal-enabled station entry/exit data and does not represent all NSW transport modes or all regional rail services.
- The period classification is approximate and intended for exploratory analysis.

## How to run

Install the required packages:

```bash
pip install -r requirements.txt
