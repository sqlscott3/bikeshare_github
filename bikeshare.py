import time
import datetime as dt
import pandas as pd
import numpy as np
import calendar as cal

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
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nPlease Enter the City for which you want to see the Analysis (Chicago, New York City or Washington):\n").lower()
        if city not in CITY_DATA.keys():
            print("Sorry, that is not one of our Cities, please try again.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nPlease Enter the name of the Month to which you would like to filter the data (All for no filter, or Jan, Feb, ..., Jun):\n").lower()
        if month not in "all,jan,feb,mar,apr,may,jun":
            print("Sorry, that is not one of our Months, please try again.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease Enter Day of the Week for which you would like to filter the data (All for no filter, or Su, M, Tu, W, Th, F, Sa):\n").lower()
        if day not in "all,su,m,tu,w,th,f,sa":
            print("Sorry, that is not a valid Day of the Week, please try again.")
        else:
            break
    
    print('-'*40)
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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['su','m','tu','w','th','f','sa']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    print("\nThe most common Month is: ")
    print(cal.month_name[int(df['month'].mode())])

    # display the most common day of week
    print("\nThe most common Day of the Week is: ")
    print(cal.day_name[int(df['day_of_week'].mode())])


    # display the most common start hour
    print("\nThe most common Start Hour is: ")
    print(df['hour'].mode().to_string(index=False))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    print("\nThe most commonly used Start Station is: ")
    print(df['Start Station'].mode().to_string(index=False))


    # display most commonly used end station
    print("\nThe most commonly used End Station is: ")
    print(df['End Station'].mode().to_string(index=False))


    # display most frequent combination of start station and end station trip
    print("\nThe most frequent combination of Start Station and End Station per trip is: ")
    # wrong result --> print(df[['Start Station','End Station']].mode().to_string(index=False))
    # correction using GROUP BY
    dfgb = df.groupby(['Start Station','End Station']).size().to_frame('size')
    print(dfgb[dfgb['size'] == dfgb['size'].max()])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    print("\nThe Total travel time is: ")
    sec = int(df['Trip Duration'].sum())
    print(dt.timedelta(seconds =sec))


    # display mean travel time
    print("\nThe Mean travel time is: ")
    sec = int(df['Trip Duration'].mean())
    print(dt.timedelta(seconds =sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts by User Type: ")
    print(df['User Type'].value_counts())
    

    # Display counts of gender
    print("\nCounts by Gender: ")
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print("\tGender data not available.")


    # Display earliest, most recent, and most common year of birth
    print("\nYear of Birth Analysis:")
    
    if 'Birth Year' in df.columns:
        print("\nEarliest is: ")
        print(int(df['Birth Year'].min()))

        print("\nMost Recent is: ")
        print(int(df['Birth Year'].max()))

        print("\nMost Common is: ")
        print(df['Birth Year'].mode().to_string(index=False).replace(".0",""))
    else:
        print("\tBirth Year data is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw(df):
    """Displays 5 rows of raw data at a time."""
    currows = 0
    while True:
        while True:
            raw = input("\nWould you like to see (next) 5 lines of the raw data? Yes or No\n").lower()
            if not raw or raw not in "yes,no":
                print("Sorry, Yes or No, please try again.")
            else:
                break

        if raw == 'no':
            break
        print(df.iloc[currows : currows+5])
        currows += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if not restart or restart not in "yes,no":
                print("Sorry, Yes or No, please try again.")
            else:
                break
 
        if restart == 'no':
            break


if __name__ == "__main__":
	main()
