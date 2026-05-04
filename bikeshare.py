import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_name = input("Please Choose a city [chicago, new york city, washington]: ").strip().lower()

        if city_name in CITY_DATA:
            break
        else:
            print("Oops! Invalid city. Try again.")
            
    # TO DO: get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march','april', 'may', 'june']
    while True:
        chosen_month = input("\nEnter a month name from January to June or type 'all': ").strip().lower()
        if chosen_month in valid_months:
            break
        else:
            print("Invalid month entered. Please try again.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday']
    while True:
        selected_day = input("\nEnter a weekday name or type 'all': ").strip().lower()
        if selected_day in valid_days:
            break
        else:
            print("Invalid day entered. Please try again.")
    city = city_name
    month = chosen_month
    day = selected_day
  
    print('\n','```*'*20)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    bike_data = pd.read_csv(CITY_DATA[city])

    bike_data['Start Time'] = pd.to_datetime(bike_data['Start Time'])
    bike_data['travel_month'] = bike_data['Start Time'].dt.month
    bike_data['travel_day'] = bike_data['Start Time'].dt.day_name()
    bike_data['travel_hour'] = bike_data['Start Time'].dt.hour

    available_months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all':
        month_index = available_months.index(month) + 1
        bike_data = bike_data[bike_data['travel_month'] == month_index]
    if day != 'all':
        bike_data = bike_data[bike_data['travel_day'].str.lower() == day]

    return bike_data

def time_stats(df):
    """Shows the busiest travel timings from the dataset."""

    print('\nLets Go.. Here are travel time insights...\n')

    timer_start = time.time()

    popular_month = df['travel_month'].mode()[0]
    print(f"Most active month number: {popular_month}")

    popular_day = df['travel_day'].mode()[0]
    print(f"On this day most travellers are busy : {popular_day}")

    peak_hour = df['travel_hour'].mode()[0]
    print(f"Busiest hour for rides: {peak_hour}")

    elapsed_time = time.time() - timer_start

    print(f"\nAnalysis completed in {elapsed_time:.4f} seconds.")
    print('\n','```*' * 20)

def station_stats(df):
    """Shows station popularity and common trip routes."""
    print('\nWant to know perfect station for you ? \nHere is the station activity...\n')
    timing_start = time.time()
    busiest_start = df['Start Station'].mode()[0]
    print(f"Top starting station: {busiest_start}")

    busiest_end = df['End Station'].mode()[0]
    print(f"Top destination station: {busiest_end}")
    
    df['route_pair'] = (df['Start Station'] + "  →  " + df['End Station'])
    frequent_route = df['route_pair'].mode()[0]
    print(f"Most repeated trip route: {frequent_route}")
    total_duration = time.time() - timing_start

    print(f"\nCompleted in {total_duration:.4f} seconds.")
    print('\n','```*' * 20)


def trip_duration_stats(df):
    """Displays ride duration summaries."""
    print('\nReviewing trip duration details...\n')

    process_start = time.time()
    total_ride_time = ( df['Trip Duration'].sum() )/ 3600
    print(f"Combined travel time: {total_ride_time} seconds")

    average_ride_time = df['Trip Duration'].mean()
    print(f"Average trip duration: {average_ride_time:.2f} seconds")
    
    execution_time = time.time() - process_start
    print(f"\nFinished in {execution_time:.4f} seconds.")
    print('\n','```*' * 20)

def user_stats(df):
    """Displays rider category and demographic details."""

    print('\nReviewing user information...\n')

    stats_timer = time.time()

    rider_types = df['User Type'].value_counts()

    print("User category counts:")
    print(rider_types)
    print('\nGender distribution:')

    if 'Gender' in df.columns:
        gender_breakdown = df['Gender'].value_counts()
        print(gender_breakdown)
    else:
        print("Gender information is unavailable for this dataset.")

    print('\nBirth year statistics:')

    if 'Birth Year' in df.columns:

        oldest_birth = int(df['Birth Year'].min())
        latest_birth = int(df['Birth Year'].max())
        frequent_birth = int(df['Birth Year'].mode()[0])

        print(f"Earliest birth year: {oldest_birth}")
        print(f"Most recent birth year: {latest_birth}")
        print(f"Most common birth year: {frequent_birth}")

    else:
        print("Birth year data is unavailable for this dataset.")

    total_runtime = time.time() - stats_timer

    print(f"\nCompleted in {total_runtime:.4f} seconds.")
    print('\n','```*' * 20)

def display_raw_data(df):
    """Displays raw dataset rows in batches of five."""
    row_position = 0
    while True:
        user_choice = input("\nAt last would you like to view raw trip data? (yes/no): ").strip().lower()
        if user_choice != 'yes':
            break
        print(df.iloc[row_position:row_position + 5])
        row_position += 5
        if row_position >= len(df):
            print("\nNo more data available to display.")
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nThank you for exploring US bikeshare data!")
            break

if __name__ == "__main__":
	main()
