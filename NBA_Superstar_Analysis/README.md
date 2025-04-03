# NBA Superstar Impact Analysis

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
  - [Required Libraries](#required-libraries)
- [How It Works](#how-it-works)
  - [1. Data Retrieval](#1-data-retrieval)
  - [2. Data Processing](#2-data-processing)
  - [3. Statistical Analysis (T-Test)](#3-statistical-analysis-t-test)
  - [4. Results Storage](#4-results-storage)
  - [5. Combining Results for Multiple Players](#5-combining-results-for-multiple-players)
- [Example of Generated CSV Output](#example-of-generated-csv-output)
- [Instructions for Use](#instructions-for-use)
  - [1. Setting Up the Script](#1-setting-up-the-script)
  - [2. Run the Script](#2-run-the-script)
  - [3. Combining Results for Multiple Players](#3-combining-results-for-multiple-players)
  - [4. Visualize the Results](#4-visualize-the-results)
- [Sample CSV Files](#sample-csv-files)
- [Conclusion](#conclusion)

---

## Overview

This project analyzes the impact of an NBA superstar joining a team using historical game data. The analysis compares various team metrics (win percentage, plus/minus, and points made) for a specific NBA team before and after the addition of a superstar. The statistical method used to assess the impact is an **A/B Test** via **t-tests**, to determine whether there is a significant difference in the team's performance after the superstar's arrival.

---

## Prerequisites

### Required Libraries

To run this analysis, the following Python libraries are required:

- **nba_api**: To access NBA game data via the NBA API.
- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical operations.
- **scipy**: For statistical analysis (t-tests).

To install the necessary libraries, run the following:

```bash
pip install nba_api pandas numpy scipy
```

## How It Works

The script is designed to analyze the impact of an NBA superstar joining a team over a specified period. The process can be broken down into several key steps:

### 1. Data Retrieval

- **NBA Team ID**: The script uses the `nba_api` library to retrieve the NBA team ID based on the team name.
- **Game Schedule**: It retrieves the historical game schedule for a specified time frame (e.g., 1995-1997) using the `LeagueGameFinder` endpoint.
- **Opponent Score**: The opponent's score for each game is retrieved by filtering the games using the `GAME_ID` and the team's abbreviation.

### 2. Data Processing

The script categorizes games into two groups: **Pre-Superstar** and **Post-Superstar**. This categorization is based on the player's join date (e.g., for Shaquille O'Neal, it is 1996-07-18).

For each group, the script calculates several metrics:
- **Win Percentage**: The ratio of wins to total games played.
- **Plus/Minus**: The point differential (team’s points minus opponent’s points).
- **Team Points Made**: The total points scored by the team in each game.

### 3. Statistical Analysis (T-Test)

For each of the metrics (win percentage, plus/minus, and team points made), a **t-test** is performed to determine if there is a significant difference between the **Pre-Superstar** and **Post-Superstar** groups.

- **T-statistic**: This value measures the magnitude of the difference between the two groups relative to their variance.
- **P-value**: This value determines the probability that the observed difference is due to random chance. A low p-value (typically less than 0.05) indicates that the difference is statistically significant.

### 4. Results Storage

The script stores the results of the statistical tests (t-statistics, p-values, and significance) in a **DataFrame** and then exports this DataFrame to a **CSV file** for further analysis or visualization.

### 5. Combining Results for Multiple Players

After running the analysis for a specific player (e.g., Shaquille O'Neal), the script can be used to analyze other players (e.g., LeBron James, Kyrie Irving, Donovan Mitchell, etc.).

The results for all players are combined into a single DataFrame and exported to a CSV file for use in visualization tools like **Power BI**.

---

## Example of Generated CSV Output

For each player, the output includes the following columns:

| Metric                | Pre-Superstar Mean | Post-Superstar Mean | T-statistic | P-value | Significance |
|-----------------------|--------------------|---------------------|-------------|---------|--------------|
| Win Percentage        | 60%                | 75%                 | 2.1         | 0.03    | Significant  |
| Plus/Minus            | +5                 | +6.5                | 1.8         | 0.05    | Significant  |
| Team Points Made      | 110                | 115                 | 3.0         | 0.01    | Significant  |

---

## Instructions for Use

### 1. Setting Up the Script

To run the script:
- Define the **NBA superstar** and **team** (e.g., Shaquille O'Neal and the Los Angeles Lakers).
- Set the **join date** of the player (e.g., 1996-07-18 for Shaquille O'Neal).
- Define the **season** and the **start and end seasons** of the analysis.

### 2. Run the Script

The script will automatically:
- Pull the necessary game data for the team.
- Add the opponent’s score to the dataset.
- Categorize games as pre or post-superstar addition based on the player's join date.
- Perform t-tests to analyze whether there is a significant change in team performance after the superstar's arrival.
- Output the results to a CSV file for further analysis or visualization.

### 3. Combining Results for Multiple Players

If you wish to analyze the impact of multiple superstars (e.g., LeBron James, Kyrie Irving), simply repeat the process for each player and combine the results into a single CSV file using the provided code at the end of the script.

### 4. Visualize the Results

You can use tools like **Power BI** or **Tableau** to load the CSV files and visualize the results:
- Create bar charts, line charts, and tables to compare the pre- and post-superstar performance metrics for each player.
- Use significance flags (e.g., Significant or Not Significant) to highlight the important changes in performance.
- In this case, I have used **Power BI** to give a sample visualization of the results, 'NBA_Superstar_Impact_Visualization.pbix' and 'NBA_Superstar_Impact_Visualization_Screenshot.png'

---

## Sample CSV Files

- `LeBron James_join_LAL_analysis_results.csv`
- `Kyrie Irving_join_BOS_analysis_results.csv`
- `Donovan Mitchell_join_CLE_analysis_results.csv`
- `James Harden_join_HOU_analysis_results.csv`

These CSV files contain the analysis results for different players and can be combined for comparison. Example of this is as follows: `Combined_Player_analysis_results.csv`

*Note: This project can be optimized more to have less hard-coded inputs, ability to add multiple inputs at once

---

## Conclusion

This project provides insights into the impact of a superstar joining an NBA team, with a focus on key performance metrics. The statistical analysis through **t-tests** helps determine whether the changes in team performance (such as win percentage, plus/minus, and points made) are statistically significant. The resulting data can be used for in-depth visual analysis in **Power BI**, providing a clear understanding of the impact of star players on team performance.
