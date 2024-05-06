import pandas as pd
import streamlit as st

# Define weightings for different criteria
weights = {
    'Industry': 0.5,
    'Stage': 1.0,
    'ARR': 1.5,
    'Number of Employees': 1.0,
    'Location': 0.2
}

# Hard-coded startup data
data = [
    ["ByteBank", "Fintech startup focused on payments", "Fintech", "Seed", 1200000, 15, "USA"],
    ["MediMatrix", "Healthcare startup specializing in diagnostics", "Healthcare", "Series A", 3000000, 50, "UK"],
    ["SynthiLogic", "AI startup with advanced analytics", "AI", "Series C", 10000000, 120, "Canada"],
    ["GreenSphere", "Healthcare startup improving patient care", "Healthcare", "Seed", 200000, 5, "Germany"],
    ["AetherAnalytics", "Fintech startup offering financial literacy", "Fintech", "Series B", 5000000, 90, "USA"],
    ["PulsePredict", "Healthcare startup optimizing telehealth", "Healthcare", "Pre-Seed", 9000, 1, "China"],
    ["LumenLoop", "AI startup disrupting marketing", "AI", "Series A", 50000, 5, "Canada"]
]

# Create DataFrame
columns = ['Startup Name', 'Description', 'Industry', 'Stage', 'ARR', 'Number of Employees', 'Location']
df = pd.DataFrame(data, columns=columns)

# Add a 'Criteria Met' column if it's not already present
if 'Criteria Met' not in df.columns:
    df['Criteria Met'] = 0

# Define criteria functions
def meets_industry_criteria(industry):
    acceptable_industries = ['Fintech', 'Healthcare', 'AI']
    return industry in acceptable_industries

def meets_stage_criteria(stage):
    acceptable_stages = ['Seed', 'Series A', 'Series B']
    return stage in acceptable_stages

def meets_arr_criteria(arr):
    try:
        arr_value = int(arr)
        return 20000 <= arr_value <= 10000000  # ARR between 20k and 10M
    except ValueError:
        return False

def meets_employees_criteria(employees):
    try:
        employees_value = int(employees)
        return 2 <= employees_value <= 25  # Employee count between 2 and 25
    except ValueError:
        return False

def meets_location_criteria(location):
    acceptable_locations = ['USA', 'Canada']
    return location in acceptable_locations

# Function to evaluate and update criteria
def evaluate_and_update(df):
    def evaluate_row(row):
        criteria_met = 0

        # Industry
        row['Industry Met'] = meets_industry_criteria(row['Industry'])
        criteria_met += weights['Industry'] if row['Industry Met'] else 0

        # Stage
        row['Stage Met'] = meets_stage_criteria(row['Stage'])
        criteria_met += weights['Stage'] if row['Stage Met'] else 0

        # ARR
        row['ARR Met'] = meets_arr_criteria(row['ARR'])
        criteria_met += weights['ARR'] if row['ARR Met'] else 0

        # Number of Employees
        row['Number of Employees Met'] = meets_employees_criteria(row['Number of Employees'])
        criteria_met += weights['Number of Employees'] if row['Number of Employees Met'] else 0

        # Location
        row['Location Met'] = meets_location_criteria(row['Location'])
        criteria_met += weights['Location'] if row['Location Met'] else 0

        row['Criteria Met'] = criteria_met
        return row

    df = df.apply(evaluate_row, axis=1)
    return df

# Apply evaluation and update the DataFrame
df = evaluate_and_update(df)

# Sort by Criteria Met
df = df.sort_values(by='Criteria Met', ascending=False)

# Streamlit App
st.title("Stack Ranked Startup Database")
st.write("A tool to rank startups based on your investment thesis")

# Allow user to adjust weights
st.sidebar.title("Adjust Criteria Weights")
weights['Industry'] = st.sidebar.slider("Industry Weight", 0.0, 2.0, weights['Industry'])
weights['Stage'] = st.sidebar.slider("Stage Weight", 0.0, 2.0, weights['Stage'])
weights['ARR'] = st.sidebar.slider("ARR Weight", 0.0, 2.0, weights['ARR'])
weights['Number of Employees'] = st.sidebar.slider("Number of Employees Weight", 0.0, 2.0, weights['Number of Employees'])
weights['Location'] = st.sidebar.slider("Location Weight", 0.0, 2.0, weights['Location'])

# Re-evaluate and display updated DataFrame
df = evaluate_and_update(df)
df = df.sort_values(by='Criteria Met', ascending=False)
st.write(df)