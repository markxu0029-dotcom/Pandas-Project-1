""" Question:
1. Which stations show the greatest absolute and relative variability [coeff of variation]
in monthly TOTAL transport usage between July 2016 and October 2024?

2.What long-term trends, seasonal patterns and major disruptions,
are observable in monthly transport demand between July 2016 and October 2024?
""" 

import pandas as pd
# to see all the columns
pd.set_option("display.max_columns",None)
pd.set_option("display.width", 200)

transport = pd.read_csv("NSW_transport_201607_to_202410_clean.csv")#read the newfile

# make sure date are in correct format "%Y-%m"
transport["MonthYear"] = pd.to_datetime(
    transport["MonthYear"], format="%Y-%m")

# check the data being correctly interpreted in new file
print(transport.head())
print(transport.tail())
print(transport.shape)
print(transport.dtypes)
# extract col with "Trip"
# counts how many times each distinct vavlues occurs .value_counts()
# count the 1st 5 values .head()
print(transport["Trip"].value_counts().head()) 
""" Why use value_counts()?
prevent terating whole column as numeric: less than 50"""


# create a new column to see and change less than 50 to 25
# while leave original column unchanged
# .eq() rquals to ==
transport["Trip_Suppressed"] = (transport["Trip"].eq("Less than 50"))
# creates a new column showing True for less than 50, False for not

# main problem: 
transport["Trip_Numeric"] = pd.to_numeric(
    transport["Trip"].replace("Less than 50",25))
# inside bracket: replace less than 50 to numerical value 25!
# pd.to_numeric(: telling pandas to interpret thee values are num, not text
# .to_numeric() is a general function belonging to pandas library


# ---------
# check all the data in the new csv file

col = ["Trip", "Trip_Suppressed", "Trip_Numeric"]

# show the first twn columns side by side
print(transport[col].head(10))

# Confirm Trip_numeric, all numeric data type now
print("Trip_Numeric Data Type:", transport["Trip_Numeric"].dtypes)

# count how many values are suppressed
print("Trip_Suppressed:", transport["Trip_Suppressed"].value_counts())

# check and count any missing values- should be 0
print("Missing Numeric values:", transport["Trip_Numeric"].isna().sum())
#isna() used to detect missing or null values


# create a second DataFrame called station_month
station_month = (transport.groupby(
    ["MonthYear", "Station"], as_index = False)["Trip_Numeric"].sum())

# station_mean = (station_month.groupby("Station")["Total_Usage"].mean())
station_month = station_month.rename(columns={"Trip_Numeric": "Total_Usage"})

# check data again
print(station_month.head(14))
print(station_month.tail(14))

print("data type:", station_month.dtypes)
print("shape:", station_month.shape)

# check missing data
print("any missed values:", station_month["Total_Usage"].isna().sum())
print("columns:", station_month.columns.tolist())

# check any data appeared twice:
station_month_duplicates = station_month.duplicated(subset=["MonthYear", "Station"]).sum()
print(station_month_duplicates)

# calculating the mean for the entry+exit table: Total_Usage

# Computing the mean: each station's monthly total usage
""" station.month.mean() calculate the whole table, [monthyear datetime; station text;
total_usage number], which is not applicable; and it calculates overall
all stations, not individual stations respectively"""

station_mean = (station_month.groupby("Station")["Total_Usage"].mean())
print("station mean:", station_mean)
""".groupby("Station") put together all rows beloning into the same station
# ["Total_Usage"] within in each station group, choose the column we want to compute
# only want the average of total_usage, NOT date or time"""

# standard deviation
station_deviation = (station_month.groupby("Station")["Total_Usage"].std())
print("standard deviation", station_deviation)
# count how many months available for each station
station_month_count = (station_month.groupby("Station")["Total_Usage"].count())
print("station month count:", station_month_count)

# Compute the CV:
station_cv = station_deviation / station_mean
print("Station cv %:", station_cv)


# find the max standard deviation STATION NAME
max_station_abs_var_name = station_deviation.idxmax()
max_station_abs_variability = station_deviation.max()
print("Max Abs variabiltiy station name:", max_station_abs_var_name)
print(f"Max abs variability: {max_station_abs_variability:,.3f}")


# Fidn the max CV station NAME and VALUE
max_station_relativeVar_name = station_cv.idxmax()
max_station_relativeVar = station_cv.max()
print("Max station relative variability Name:", max_station_relativeVar_name)
print(f"Max value of relative variability: {max_station_relativeVar:,.3f}")

# --------------------------
# issue when coding: concat does not work well
""" use dictionary for table
# Create a table to construct: mean, standard deviation, cv, month count
station_summaryTable = pd.concat(
    [station_mean, station_deviation, station_cv, station_month_count], axis=1 ).reset_index()

# create a percentage version for easier interpretation: adding another column
station_summaryTable["CV_percent"] = (station_summaryTable["station_cv"] * 100)
print(station_summaryTable.head(7))

# rank absolute variabilityL largest standard deviation to smallest
absolute_ranking = station_summaryTable.sort_values(by="standard_deviation", ascending=False)

# show the top 10 stations
print("Top 10 stations by max absolute variability:")
print(absolute_ranking[
    "Station", "station_mean", "station_deviation", "station_cv", "station_month_count"])"""
#------------------------------------------------

# using dictionary to create the table
station_summaryTable = pd.DataFrame({
    "Mean_Usage": station_mean, "Standard_Deviation": station_deviation,
    "CV": station_cv, "Months_Observed": station_month_count}).reset_index()#braket for .reset_index!
# check the resulting column, and check first 7 rows
print(station_summaryTable.head(7))

# convert to cv ratio to percentage
station_summaryTable["CV_Percent"] = (station_summaryTable["CV"] * 100)
print(station_summaryTable[[
            "Station",
            "Mean_Usage",
            "Standard_Deviation",
            "CV",
            "CV_Percent",
            "Months_Observed"]].head(10))
                                                        
# absolute ranking:
absolute_ranking = station_summaryTable.sort_values(
    by="Standard_Deviation",
    ascending = False)


print("Top 10 stations by absolute ranking: ")
print(absolute_ranking[
    ["Station","Mean_Usage","Standard_Deviation","CV_Percent","Months_Observed"]].head(10))

# now for relative ranking, but using complete coverage for a more comparable ranking
complete_stations = station_summaryTable[station_summaryTable["Months_Observed"] == 100].copy()
relative_ranking_complete = (complete_stations
                             .sort_values(by="CV", ascending = False))
# need asking questions, complete means all 100 months having data? 
print("Top 10 stations by relative variability with 100 months of data:")
print(relative_ranking_complete[["Station","Mean_Usage","Standard_Deviation",
                                 "CV_Percent","Months_Observed"]].head(10))

#_---------------------------------------------------------------------
# ---------------------------------------------------------------------
# now we try to plot
import matplotlib.pyplot as plt

# Plot 1: absolute variability
top_absolute  = absolute_ranking.head(10).copy()

# reverse the order so largest bar appears at top in a horizontal bar chart
top_absolute = top_absolute.sort_values(
    by="Standard_Deviation", ascending = True)

plt.figure(figsize=(10,6))

plt.barh(top_absolute["Station"],top_absolute["Standard_Deviation"])

plt.xlabel("Standard deviation of monthly total usage")
plt.ylabel("Station")
plt.title("Top 10 stations by absolute variability")
# plt.title(f"Monthly total usage at {top_absolute}") dont want this, too messy
plt.tight_layout()
#plt.show() : put at the end of the projects

# ---------------------------------------------------------
# PLOT 2: RELATIVE VARIABILITY
# ---------------------------------------------------------

# Select the top 10 complete-coverage stations by CV percentage.
# These stations have the largest fluctuations relative to their average usage.
top_relative = relative_ranking_complete.head(10).copy()

# Reverse the order so the largest bar appears at the top
# in a horizontal bar chart.
top_relative = top_relative.sort_values(
    by="CV_Percent",
    ascending=True)

plt.figure(figsize=(10, 6))

plt.barh(top_relative["Station"],top_relative["CV_Percent"])

plt.xlabel("Coefficient of variation (%)")
plt.ylabel("Station")
plt.title(
    "Top 10 stations by relative variability\n"
    "Complete 100-month coverage")

plt.tight_layout()
#plt.show()

# check the suppressed stations

# count how many stations suppressed
station_suppressed_count = (transport.groupby("Station")["Trip_Suppressed"].sum())

# count total entry/exit record for each station
station_record_count = (transport.groupby("Station")["Trip_Suppressed"].count())

# compute the percentage of records that were supressed
station_suppressed_percent = (
    station_suppressed_count/station_record_count * 100)

# give the series a clear name before merging
station_suppressed_percent = station_suppressed_percent.rename("Suppressed_Percent")

# Add this information into station_summaryTable
station_summaryTable = station_summaryTable.merge(
    station_suppressed_percent,
    left_on="Station",
    right_index=True,
    how="left")

complete_stations = station_summaryTable[
    station_summaryTable["Months_Observed"] == 100
].copy()

relative_ranking_complete = complete_stations.sort_values(
    by="CV",
    ascending=False
)
# if you want the relative ranking table to include Suppressed_Percent,
# recompute complete_stations after the merge.
# ----------------------------------


# Check high CV stations together with suppression percentage
print(
    station_summaryTable
    .sort_values(by="CV", ascending=False)
    [
        [
            "Station",
            "Mean_Usage",
            "Standard_Deviation",
            "CV_Percent",
            "Months_Observed",
            "Suppressed_Percent"
        ]].head(15).to_string())

# plt.show()                   
""" Analysis
Coefficient of very low use stations can be unstable, the relative-variability ranking
restricted to the stations with 100-month coverage. Stations with high proportion of
'less than 50' values should be interpreted cautiously.

Relative variability shows the stations that flucatuate most strongly compared to their normal month level.
This ranking is more closely lead by the smaller stations with more specialised stations
with irregular demand patterns.

Absolute variability are dominated by the stations with largest amout of usage. They are in CBD -
such as Town Hall, Central, Circular Quay; and also in major hubs in suburbs like Chatswood and
Paramatta.
They have largest standard deviation cuz the monthly usage is very large ,
hence disruptions and also RECOVERIES resulted in large raw changes in trip numbers


"""



# ---------------------------------------------------------------------------------
# Q2:What long-term trends, seasonal patterns and major disruptions,
#are observable in monthly transport demand between July 2016 and October 2024?
# --------------------------------------------------------------------------------

# create a table to summarise: STATION USAGE WITHIN EACH MONTH
''' usage station_month cuz already summed up entry+exit'''
print('Station_month:')
print(station_month)
network_month = (station_month.groupby('MonthYear', as_index=False)["Total_Usage"].sum())
# qns: why do we need as_index=False

# rename the column to make the meaning clearer:
#change from Total_usage to Network_Total_Usage
network_month = network_month.rename(columns={"Total_Usage": "Network_Total_Usage"})
print(network_month.head()) # check the data
print(network_month.tail())
print(network_month.shape)
print(network_month.dtypes)



#---------------------------------------------------------------
# Plot Network month

plt.figure(figsize=(12,6))# make the size of the plot
# not plt.barh() here cuz we don't plot bar graph in q2
# x axis: MonthYear, y axis: Network_Total_Usage - print the table if seeing the structure!
plt.plot(network_month["MonthYear"], network_month["Network_Total_Usage"])
plt.xlabel("MonthYear")
plt.ylabel("NetWork_Total_Usage")
plt.title("Monthly total NSW station usage over time")
plt.tight_layout()



# ------------------------------------------------------
# compute the 12-month rolling average, and add this as a column!!
network_month["Rolling_12_Month_Average"] = (
    network_month["Network_Total_Usage"].rolling(window=12).mean())


plt.figure(figsize=(12,6))
plt.plot(network_month["MonthYear"], network_month["Network_Total_Usage"],
         label="Monthly total usage")

plt.plot(network_month["MonthYear"], network_month["Rolling_12_Month_Average"],
         label="Rolling 12 Months Usage")

plt.xlabel("Month")
plt.ylabel("Monthly total usage")
plt.title("Monthly network demand with 12-month ROLLING AVERAGE")
plt.legend() # pay attention to this command

""" Monthly line shows short term movement,
the 12 month rolling average smooths seasonal noise and highlight the broader trend"""

#-----------------------------------------------------
# Seasonal pattern by calendar month 
# extract month number from the date
network_month["Calendar_Month"] = (network_month["MonthYear"].dt.month)
# compute the average network demand for each calendar month
monthly_seasonality  = (
    network_month.groupby("Calendar_Month", as_index=False)["Network_Total_Usage"].mean())
#.groupby(.....: tells us Group by period, then average only the network total usage column.

print(monthly_seasonality)
""" This tell us on average:
Jan    Demand
Feb    Demand ......
Dec    Demand """

# ------
# Plot 6: average demand by calendar month
# bar graph!

plt.figure(figsize=(12,6))
plt.bar(monthly_seasonality["Calendar_Month"], monthly_seasonality["Network_Total_Usage"])
plt.xlabel("Calendar_Month")
plt.ylabel("Network_Total_Usage")
plt.title("Average NETWORK demand by calendar month")
plt.xticks(range(1,13))
plt.tight_layout()

# ------
# prediction of how to interpret the graph:
# this graph answers: are some months GENRALLY HAVE HIGHER OR LOWER TRAVEL DEMAND?
# possible interpretation: Dec and Jan maybe lower cuz of holidays, while demans higher in regular
# months , where work is dominant and holiday is limited
""" Draw the graph to conclude this!!!!!!!!!!!"""


# ---------------------------c
# MAJOR DISRUPTION PERIODS
# define a function , with the keydates as 2020-03-01 to 2022-01-01 as disruption of covid

def assign_period(date):
    if date < pd.Timestamp("2020-03-01"):
        return "Pre-disruption"
    elif date < pd.Timestamp("2022-01-01"):
        return "Disruption"
    else:
        return "Recovery"
    
# assign another part of the table
network_month["Period"] = network_month["MonthYear"].apply(assign_period)

print(network_month[["MonthYear", "Period"]].head())
print(network_month[["MonthYear", "Period"]].tail())

# summarise : compute average monthly demand in each period
period_summary = (network_month.groupby(
    "Period", as_index = False)["Network_Total_Usage"].mean())
# mistake: as_index=False)["Network_Total_Usage"].mean() 

# Optional: put periods in logical order
period_order = ["Pre-disruption","Disruption","Recovery"]

period_summary["Period"] = pd.Categorical(
    period_summary["Period"],
    categories=period_order,
    ordered=True)

period_summary = period_summary.sort_values("Period")

print(period_summary.to_string())

plt.figure(figsize=(8, 5))

plt.bar(period_summary["Period"], period_summary["Network_Total_Usage"])

plt.xlabel('Period')
plt.ylabel("Network_Total_Usage")
plt.title("Average monthly network demand by period")
plt.tight_layout()
# Answers: how different were demand levels before , during and after major disruptions?

plt.show() 



""" More Analysis of answering Q1 and Q2:

The top 10 stations with greatest variability is Town Hall, Central, Wynyard,
Circular Quay, Paramatta, North Sydney, Redfern, Bondi Junction, Chatswood
and Martin Place Station. 



