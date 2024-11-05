import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and preprocess data
data = pd.read_csv('FilePath.csv')
data['EVENT_DATETIME'] = pd.to_datetime(data['EVENT_DATETIME'], errors='coerce')
data = data.dropna(subset=['EVENT_DATETIME']).sort_values(by=['FORM_NAME', 'SESSION_ID', 'EVENT_DATETIME']).reset_index(drop=True)

# Filter to only 'Form' events for each 'FORM_NAME'
form_data = data[(data['EVENTTYPE'] == 'Form')]

# Define a function to calculate duration within a session based on 'Started' and 'Completed' events
def calculate_duration(session):
    if 'Started' in session['EVENTACTION'].values and 'Completed' in session['EVENTACTION'].values:
        start_time = session.loc[session['EVENTACTION'] == 'Started', 'EVENT_DATETIME'].iloc[0]
        end_time = session.loc[session['EVENTACTION'] == 'Completed', 'EVENT_DATETIME'].iloc[-1]
        return (end_time - start_time).total_seconds() / 86400  # Convert to Days
    else:
        return None

# Group by FORM_NAME and SESSION_ID, then calculate duration only for valid sessions
form_durations = form_data.groupby(['FORM_NAME', 'SESSION_ID']).apply(calculate_duration).reset_index(name='duration')
form_durations = form_durations.dropna(subset=['duration'])  # Drop rows where duration could not be calculated

# Plot distribution of form completion times in Days by FORM_NAME
plt.figure(figsize=(12, 6))
sns.boxplot(data=form_durations, x='FORM_NAME', y='duration')
plt.xticks(rotation=45)
plt.title('Time Taken to Complete Each Form Type (in Days)')
plt.ylabel('Duration (Days)')
plt.xlabel('Form Type')
plt.show()


#######################

# Plot histogram for session durations (completed forms)
plt.figure(figsize=(12, 6))
sns.histplot(form_durations['duration'], bins=30, kde=True)
plt.title('Distribution of Form Completion Times')
plt.xlabel('Duration (Days)')
plt.ylabel('Frequency')
plt.show()

#########################

# Check if patients have multiple sessions per form
multiple_sessions_per_form = data.groupby(['SESSION_ID', 'FORM_NAME'])['EVENT_DATETIME'].nunique() > 1
revisits = multiple_sessions_per_form[multiple_sessions_per_form].reset_index().groupby('FORM_NAME').size()

# Bar plot of revisited form counts
plt.figure(figsize=(12, 6))
revisits.plot(kind='bar', color='skyblue')
plt.title('Forms with Multiple Sessions')
plt.ylabel('Number of Revisits')
plt.xlabel('Form Name')
plt.xticks(rotation=45)
plt.show()


#############################

# Filter to only 'Form' events
form_data = data[data['EVENTTYPE'] == 'Form']

# Define a function to calculate abandonment rate per form
def calculate_abandonment_rate(group):
    total_sessions = len(group['SESSION_ID'].unique())  # Total unique sessions per form
    completed_sessions = group[group['EVENTACTION'] == 'Completed']['SESSION_ID'].nunique()  # Sessions that completed
    abandoned_sessions = total_sessions - completed_sessions  # Sessions that did not complete
    abandonment_rate_percentage = (abandoned_sessions / total_sessions) * 100  # Convert to percentage
    return abandonment_rate_percentage

# Calculate abandonment rate by FORM_NAME
abandonment_rate = form_data.groupby('FORM_NAME').apply(calculate_abandonment_rate).reset_index(name='abandonment_rate (%)')

print(abandonment_rate)

# Plot Abandonment rate per form
sns.barplot(data=abandonment_rate, x='FORM_NAME', y='abandonment_rate (%)', palette="viridis")
plt.xticks(rotation=45, ha='right')
plt.title('Abandonment Rate by Form Type')
plt.ylabel('Abandonment Rate (%)')
plt.xlabel('Form Name')
plt.show()



#########################

# Calculate abandonment rate for each question group
# Filter to only 'Question-Group' events
form_data = data[data['EVENTTYPE'] == 'Question-Group']

# Define a function to calculate abandonment rate per form
def calculate_abandonment_rate(group):
    total_sessions = len(group['SESSION_ID'].unique())  # Total unique sessions per form
    completed_sessions = group[group['EVENTACTION'] == 'Completed']['SESSION_ID'].nunique()  # Sessions that completed
    abandoned_sessions = total_sessions - completed_sessions  # Sessions that did not complete
    abandonment_rate_percentage = (abandoned_sessions / total_sessions) * 100  # Convert to percentage
    return abandonment_rate_percentage

# Calculate abandonment rate by QUESTION_GROUP_NAME
abandonment_question_rate = form_data.groupby('QUESTION_GROUP_NAME').apply(calculate_abandonment_rate).reset_index(name='abandonment_rate (%)')

print(abandonment_question_rate)

# Plot Abandonment rate per QUESTION_GROUP_NAME
sns.barplot(data=abandonment_question_rate, x='QUESTION_GROUP_NAME', y='abandonment_rate (%)', palette="pastel")
plt.xticks(rotation=45, ha='right')
plt.title('Abandonment Rate by Question Group')
plt.ylabel('Abandonment Rate (%)')
plt.xlabel('Question Group')
plt.show()



