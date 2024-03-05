import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

file_path = 'data.xlsx'
columns_to_read = ['date_range_start', 'date_range_end', 'location_name', 'visits_by_day', 'visits_by_each_hour']

# Read the Excel file into a pandas DataFrame, specifying the columns to read
df = pd.read_excel(file_path, usecols=columns_to_read)

######################################################################################################################
def generate_date_range(start_date, end_date):
    current_date = start_date
    date_range = []
    while current_date <= end_date - timedelta(days=1):  # Corrected line
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return date_range


def get_season(date_str):
    """
    Get the season for a given date.
    """
    date = datetime.strptime(date_str, '%Y-%m-%d')
    month = date.month
    day = date.day
    
    if month == 3:
        return 'Spring' if day >= 1 else 'Winter'
    elif month in [4, 5]:
        return 'Spring'
    elif month == 6:
        return 'Summer' if day >= 1 else 'Spring'
    elif month in [7, 8]:
        return 'Summer'
    elif month == 9:
        return 'Fall' if day >= 1 else 'Summer'
    elif month in [10, 11]:
        return 'Fall'
    elif month == 12:
        return 'Winter' if day >= 1 else 'Fall'
    elif month in [1, 2]:
        return 'Winter'

    
# Loop through each row to generate the list of dates in given range
all_dates_list = []
for index, row in df.iterrows():
    all_dates_list.append(generate_date_range(row['date_range_start'], row['date_range_end']))

# Add the list of dates as a new column in the DataFrame
df['all_dates'] = all_dates_list
#df = df[['all_dates', 'location_name', 'visits_by_day', 'visits_by_each_hour']]


##################################################################################################
'''
    Get data for each season
'''
# Define lists to store data for each season
spring_data = []
summer_data = []
fall_data = []
winter_data = []

# Loop through each row in the DataFrame
for i, dates_list in enumerate(df['all_dates']):
    spring_check = summer_check = fall_check = winter_check = 0
    for date in dates_list:
        season = get_season(date)
        if season == 'Spring':
            spring_check += 1
        elif season == 'Summer':
            summer_check += 1
        elif season == 'Fall':
            fall_check += 1
        elif season == 'Winter':
            winter_check += 1
    
    if spring_check == 7:
        spring_info = {
            'date_range': dates_list,
            'location_name': df.loc[i, 'location_name'],
            'visits_by_day': df.loc[i, 'visits_by_day'],
            'visits_by_each_hour': df.loc[i, 'visits_by_each_hour']
        }
        spring_data.append(spring_info)
    
    if summer_check == 7:
        summer_info = {
            'date_range': dates_list,
            'location_name': df.loc[i, 'location_name'],
            'visits_by_day': df.loc[i, 'visits_by_day'],
            'visits_by_each_hour': df.loc[i, 'visits_by_each_hour']
        }
        summer_data.append(summer_info)
    
    if fall_check == 7:
        fall_info = {
            'date_range': dates_list,
            'location_name': df.loc[i, 'location_name'],
            'visits_by_day': df.loc[i, 'visits_by_day'],
            'visits_by_each_hour': df.loc[i, 'visits_by_each_hour']
        }
        fall_data.append(fall_info)
    
    if winter_check == 7:
        winter_info = {
            'date_range': dates_list,
            'location_name': df.loc[i, 'location_name'],
            'visits_by_day': df.loc[i, 'visits_by_day'],
            'visits_by_each_hour': df.loc[i, 'visits_by_each_hour']
        }
        winter_data.append(winter_info)

# Create DataFrames for each season
spring_df = pd.DataFrame(spring_data)
summer_df = pd.DataFrame(summer_data)
fall_df = pd.DataFrame(fall_data)
winter_df = pd.DataFrame(winter_data)

# Convert lists to tuples
spring_df['date_range'] = spring_df['date_range'].apply(tuple)
summer_df['date_range'] = summer_df['date_range'].apply(tuple)
fall_df['date_range'] = fall_df['date_range'].apply(tuple)
winter_df['date_range'] = winter_df['date_range'].apply(tuple)

# Drop duplicates
spring_df = spring_df.drop_duplicates(subset=['date_range', 'location_name'], keep='first')
summer_df = summer_df.drop_duplicates(subset=['date_range', 'location_name'], keep='first')
fall_df = fall_df.drop_duplicates(subset=['date_range', 'location_name'], keep='first')
winter_df = winter_df.drop_duplicates(subset=['date_range', 'location_name'], keep='first')

# Print or use the created DataFrames
# print(spring_df.head())
# print(summer_df.head())
# print(fall_df.head())
# print(winter_df.head())



#################################################################################################

def calculate_peak_hours(df):
    locations = []
    arr_max_visits_per_day = []
    arr_peak_hours_per_day = []
    all_visits = []

    for index, row in df.iterrows():
        location = row['location_name']
        visits_by_day = row['visits_by_day']
        visits_by_each_hour = row['visits_by_each_hour']

        # Calculate total visits for all days
        total_visits = 0
        visits_list = list(map(int, visits_by_day.strip("[]").split(',')))  # Convert string data to a list
        total_visits += sum(visits_list)

        hour_visits_list = list(map(int, visits_by_each_hour.strip("[]").split(',')))  # Convert string data to a list
        daily_hour_visits = [hour_visits_list[i:i+24] for i in range(0, len(hour_visits_list), 24)]

        max_visits_per_day = []
        peak_hours_per_day = []
        for daily in daily_hour_visits:
            max_visits = max(daily)
            peak_hours = [i + 1 for i, visits in enumerate(daily) if visits == max_visits]
            max_visits_per_day.append(max_visits)
            peak_hours_per_day.append(peak_hours) if max_visits != 0 else peak_hours_per_day.append([0])

        locations.append(location)
        arr_max_visits_per_day.append(max_visits_per_day)
        arr_peak_hours_per_day.append(peak_hours_per_day)
        all_visits.append(total_visits)

    return locations, arr_max_visits_per_day, arr_peak_hours_per_day, all_visits

# Calculate peak hours for each season
winter_locations, winter_max_visits, winter_peak_hours, winter_visits = calculate_peak_hours(winter_df)
spring_locations, spring_max_visits, spring_peak_hours, spring_visits = calculate_peak_hours(spring_df)
summer_locations, summer_max_visits, summer_peak_hours, summer_visits = calculate_peak_hours(summer_df)
fall_locations, fall_max_visits, fall_peak_hours, fall_visits = calculate_peak_hours(fall_df)

# Print data for Winter season
# print("Winter Locations:", winter_locations[:5])
# print("Winter Maximum Visits per Day:", winter_max_visits[:5])
# print("Winter Peak Hours per Day:", winter_peak_hours[:5])
# print("Total Winter Visits:", winter_visits[:5])

# # Print data for Spring season
# print("Spring Locations:", spring_locations[:5])
# print("Spring Maximum Visits per Day:", spring_max_visits[:5])
# print("Spring Peak Hours per Day:", spring_peak_hours[:5])
# print("Total Spring Visits:", spring_visits[:5])

# # Print data for Summer season
# print("Summer Locations:", summer_locations[:5])
# print("Summer Maximum Visits per Day:", summer_max_visits[:5])
# print("Summer Peak Hours per Day:", summer_peak_hours[:5])
# print("Total Summer Visits:", summer_visits[:5])

# # Print data for Fall season
# print("Fall Locations:", fall_locations[:5])
# print("Fall Maximum Visits per Day:", fall_max_visits[:5])
# print("Fall Peak Hours per Day:", fall_peak_hours[:5])
# print("Total Fall Visits:", fall_visits[:5])



# Store all seasons' data
all_seasons = [winter_df, spring_df, summer_df, fall_df]

# Initialize 2D array storing the temporal distribution of park usage (storing a season and an hour)
temporal_distribution = np.zeros((len(all_seasons), 24))

# Loop through each season's DataFrame
for season_index, season_df in enumerate(all_seasons):
    locations = []
    arr_max_visits_per_day = []
    arr_peak_hours_per_day = []
    all_visits = []
    
    # Loop through each row in the DataFrame
    for index, row in season_df.iterrows():
        location = row['location_name']
        visits_by_day = row['visits_by_day']
        visits_by_each_hour = row['visits_by_each_hour']
        
        # Calculate total visits for all days
        total_visits = sum(map(int, visits_by_day.strip("[]").split(',')))
        
        # Convert visits by each hour to list
        hour_visits_list = list(map(int, visits_by_each_hour.strip("[]").split(',')))
        
        # Initialize a list to store the 7 tuples of 24 hours each
        daily_hour_visits = [hour_visits_list[i:i+24] for i in range(0, len(hour_visits_list), 24)]
        
        max_visits_per_day = []
        peak_hours_per_day = []
        
        # Loop through each day's peak hours
        for daily in daily_hour_visits:
            max_visits = max(daily)
            peak_hours = [i + 1 for i, visits in enumerate(daily) if visits == max_visits]
            max_visits_per_day.append(max_visits) 
            peak_hours_per_day.append(peak_hours) if max_visits != 0 else peak_hours_per_day.append([0])
        
        # Store data for each location
        locations.append(location)
        arr_max_visits_per_day.append(max_visits_per_day)
        arr_peak_hours_per_day.append(peak_hours_per_day)
        all_visits.append(total_visits)
        
    ''' 
        Loop through each parks's data of each season and increment corresponding hour in 2D array when 
        found peak hours of visitation for each park
    '''
    # Iterate over each park
    for i, park in enumerate(arr_peak_hours_per_day):
        # Iterate over each day's peak hours
        for day in park:
            # Increment the corresponding hours in the temporal distribution array
            for hour_range in day:
                if isinstance(hour_range, int):  # Check if hour_range is an integer
                    temporal_distribution[season_index][hour_range % 24] += 1
                else:  
                    # Loop through the range if its a list
                    for hour in range(hour_range[0], hour_range[-1] + 1):
                        temporal_distribution[season_index][hour % 24] += 1

# Normalize the temporal distribution
temporal_distribution /= len(all_seasons)



# Assuming temporal_distribution contains the normalized temporal distribution
# Divide the day into sections
sections = ['Midnight', 'Morning', 'Afternoon', 'Evening']
section_hours = [(0, 6), (6, 12), (12, 18), (18, 24)]  # Start and end hours for each section

# Initialize arrays to store aggregated visitation counts for each section
seasonal_section_visits = np.zeros((len(all_seasons), len(sections)))

# Aggregate visitation counts for each section across all seasons
for season_index, season_visits in enumerate(temporal_distribution):
    for section_index, (start_hour, end_hour) in enumerate(section_hours):
        # Sum visitation counts for hours within the current section
        section_visits = np.sum(season_visits[start_hour:end_hour])
        seasonal_section_visits[season_index][section_index] = section_visits

# Plotting
plt.figure(figsize=(12, 8))
seasons = ['Winter', 'Spring', 'Summer', 'Fall']
bar_width = 0.15
for i in range(len(seasons)):
    plt.bar(np.arange(len(sections)) + i * bar_width, seasonal_section_visits[i], width=bar_width, label=seasons[i])

plt.title('Temporal Distribution of Park Usage for Peak Times During the Day (Seasonal)')
plt.xlabel('Time Section')
plt.ylabel('Average Number of Visits')
plt.xticks(np.arange(len(sections)) + bar_width * 1.5, sections)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


##################################################################################################################
# # Plotting
# plt.figure(figsize=(12, 8))
# seasons = ['Winter', 'Spring', 'Summer', 'Fall']
# for i in range(len(seasons)):
#     plt.bar(np.arange(24) + i * 0.2, temporal_distribution[i], width=0.2, label=seasons[i])

# plt.title('Temporal Distribution of Park Usage for Peak Times During the Day (Seasonal)')
# plt.xlabel('Hour of the Day')
# plt.ylabel('Average Number of Visits')
# plt.xticks(np.arange(24) + 0.3, range(24))
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()









