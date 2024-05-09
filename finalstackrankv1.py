import pandas as pd
import streamlit as st

# Replace with the path to your company's logo
logo_path = "v5logo.png"

# Display the company logo
st.image(logo_path, width=200)  # Adjust width as per your logo size

# Define weightings for different criteria
weights = {
    'Industry': 0.5,
    'Stage': 1.0,
    'ARR': 1.5,
    'Number of Employees': 1.0,
    'Location': 0.2
}

# Initialize the company data list
initial_data = [
    ["ByteBank", "Fintech startup focused on payments", "Fintech", "Seed", 1200000, 15, "USA"],
    ["MediMatrix", "Healthcare startup specializing in diagnostics", "Healthcare", "Series A", 3000000, 50, "UK"],
    ["SynthiLogic", "AI startup with advanced analytics", "AI", "Series C", 10000000, 120, "Canada"],
    ["GreenSphere", "Healthcare startup improving patient care", "Healthcare", "Seed", 200000, 5, "Germany"],
    ["AetherAnalytics", "Fintech startup offering financial literacy", "Fintech", "Series B", 5000000, 90, "USA"],
    ["PulsePredict", "Healthcare startup optimizing telehealth", "Healthcare", "Pre-Seed", 9000, 1, "China"],
    ["LumenLoop", "AI startup disrupting marketing", "AI", "Series A", 50000, 5, "Canada"]
]

# Initialize the columns
columns = ['Startup Name', 'Description', 'Industry', 'Stage', 'ARR', 'Number of Employees', 'Location']

# Initialize or retrieve the DataFrame from session_state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(initial_data, columns=columns)

# Sidebar for investment criteria
st.sidebar.title("Select Investment Criteria")
acceptable_industries = st.sidebar.multiselect(
    "Select Acceptable Industries",
    ["Fintech", "Healthcare", "AI", "Crypto / Web3", "Enterprise", "Consumer", "Other"],
    default=["Fintech", "Healthcare", "AI"]
)

acceptable_stages = st.sidebar.multiselect(
    "Select Acceptable Stages",
    ["Pre-Seed", "Seed", "Series A", "Series B", "Series C"],
    default=["Seed", "Series A", "Series B"]
)

min_arr, max_arr = st.sidebar.slider(
    "Select ARR Range",
    min_value=0, max_value=20000000, value=(20000, 10000000)
)

min_employees, max_employees = st.sidebar.slider(
    "Select Employee Count Range",
    min_value=0, max_value=500, value=(2, 25)
)

acceptable_locations = st.sidebar.multiselect(
    "Select Acceptable Locations",
    ["USA", "Canada", "UK", "Germany", "China", "India", "Brazil", "France", "Spain", "Australia", "Netherlands", "South Africa", "Singapore", "Japan", "South Korea", "Mexico", "Other"],
    default=["USA", "Canada"]
)

# Allow user to adjust weights
st.sidebar.title("Adjust Criteria Weights")
weights['Industry'] = st.sidebar.slider("Industry Weight", 0.0, 10.0, weights['Industry'])
weights['Stage'] = st.sidebar.slider("Stage Weight", 0.0, 10.0, weights['Stage'])
weights['ARR'] = st.sidebar.slider("ARR Weight", 0.0, 10.0, weights['ARR'])
weights['Number of Employees'] = st.sidebar.slider("Number of Employees Weight", 0.0, 10.0, weights['Number of Employees'])
weights['Location'] = st.sidebar.slider("Location Weight", 0.0, 10.0, weights['Location'])

# Define criteria functions
def meets_industry_criteria(industry):
    return industry in acceptable_industries

def meets_stage_criteria(stage):
    return stage in acceptable_stages

def meets_arr_criteria(arr):
    try:
        arr_value = int(arr)
        return min_arr <= arr_value <= max_arr
    except ValueError:
        return False

def meets_employees_criteria(employees):
    try:
        employees_value = int(employees)
        return min_employees <= employees_value <= max_employees
    except ValueError:
        return False

def meets_location_criteria(location):
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

# Function to remove a selected startup
def remove_startup(df, startup_name):
    return df[df['Startup Name'] != startup_name]

# Function to add startups from a CSV file
def add_startups_from_csv(file):
    csv_df = pd.read_csv(file)
    required_columns = set(columns)
    if required_columns.issubset(csv_df.columns):
        return csv_df[columns]
    else:
        st.error(f"The uploaded CSV file must have the following columns: {columns}")
        return pd.DataFrame(columns=columns)

# Sidebar Form to add a new startup
st.sidebar.title("Add a New Startup")
with st.sidebar.form(key='add_startup_form'):
    startup_name = st.text_input("Startup Name")
    description = st.text_input("Description")
    industry = st.selectbox("Industry", ["Fintech", "Healthcare", "AI", "Crypto / Web3", "Enterprise", "Consumer", "Other"])
    stage = st.selectbox("Stage", ["Pre-Seed", "Seed", "Series A", "Series B", "Series C"])
    arr = st.number_input("ARR", min_value=0)
    num_employees = st.number_input("Number of Employees", min_value=0)
    location = st.selectbox("Location", ["USA", "Canada", "UK", "Germany", "China", "India", "Brazil", "France", "Spain", "Australia", "Netherlands", "South Africa", "Singapore", "Japan", "South Korea", "Mexico", "Other"])
    add_button = st.form_submit_button(label='Add Startup')

    if add_button and startup_name and description and industry and stage and arr and num_employees and location:
        new_data = [[startup_name, description, industry, stage, arr, num_employees, location]]
        new_df = pd.DataFrame(new_data, columns=columns)
        st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
        st.session_state.df = evaluate_and_update(st.session_state.df)
        st.session_state.df = st.session_state.df.sort_values(by='Criteria Met', ascending=False)

# File uploader to add startups via CSV
uploaded_file = st.sidebar.file_uploader("Upload a CSV file to add startups", type=["csv"])
if uploaded_file:
    new_startups_df = add_startups_from_csv(uploaded_file)
    if not new_startups_df.empty:
        st.session_state.df = pd.concat([st.session_state.df, new_startups_df], ignore_index=True)
        st.session_state.df = evaluate_and_update(st.session_state.df)
        st.session_state.df = st.session_state.df.sort_values(by='Criteria Met', ascending=False)

# Sidebar Form to remove a startup
st.sidebar.title("Remove a Startup")
with st.sidebar.form(key='remove_startup_form'):
    startup_to_remove = st.selectbox("Select a Startup to Remove", st.session_state.df['Startup Name'].unique())
    remove_button = st.form_submit_button(label='Remove Startup')

    if remove_button and startup_to_remove:
        st.session_state.df = remove_startup(st.session_state.df, startup_to_remove)
        st.session_state.df = evaluate_and_update(st.session_state.df)
        st.session_state.df = st.session_state.df.sort_values(by='Criteria Met', ascending=False)

# Apply evaluation and update the DataFrame
st.session_state.df = evaluate_and_update(st.session_state.df)
st.session_state.df = st.session_state.df.sort_values(by='Criteria Met', ascending=False)

# Streamlit App
st.title("Stack Ranked Startup Database")
st.write("A tool to rank startups based on your investment thesis and criteria")

# Display the DataFrame
st.write(st.session_state.df)