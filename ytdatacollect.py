## Relevant libraies to import
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
from datetime import datetime

## Youtube API key & load API
## You can get a api key from google developers console to access the youtube v3 api, without it you won't be able to access any of the functions within here.
## You can get more information online, but after you get your key you can place it within the api key.
api_key = '[Insert your api key here]'
youtube = build('youtube', 'v3', developerKey = api_key)

## function which takes dates to collect information
def youtube_collect(dataFrame=None):
    
    #Empty lists of information that is collected for dataframe

    videoId = []
    statistics = []
    snippet = []
    tags = []

    #Collection of different lists, dictionaries used to compare input between possible inputs for potential errors
    month = {'january': 1, 'february': 2, 'march':3, 'april':4, 'may': 5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
    resource = ['channel','playlist','videos']
    order = ['date', 'rating','relevance','title','videocount','viewcount']
    
    # All error messages for invalid inputs
    date_error = 'Invalid Input. You must type a valid integer for the date'
    month_error = 'Invalid Input. You must type in a valid month'
    year_error = 'Invalid Input. You must type in a integer for the year'
    input_error = 'Invalid Input. Please reenter your input'

    print("Do you have any specific words you are looking for in your search?")

    # Will look for search terms to search for first, this can be optional since you do not necessarily need any search terms to query through
    user_error = True
    while user_error:
        yes_no_input = input()
        yes_no_input = yes_no_input.lower()

        if yes_no_input == 'y' or yes_no_input == 'yes':
            print('What are your search keywords?')
            print("[input words or None]")
            search_input = input()
            search_input = search_input.lower()
            if search_input != 'none':
                search_keywords = search_input
                user_error = False
            else:
                print('There may have been a slight mistake I guess. Let us continue')
                search_keywords = None
                user_error = False
        elif yes_no_input == 'n' or yes_no_input == 'no':
            search_keywords = None
            user_error = False
        else:
            print(input_error)

    print("")
    # Dates however, are not so optional. This will look through specific dates for the user. First, asking for year and then asking for month and days to look through
    date_time_check = True
    while date_time_check:
        user_error = True
        while user_error:
            print('Which year would you like to begin your search')
            year_input = input()
            year_input_split = year_input.split()
            if len(year_input_split) > 1:
                print(input_error)
            else:
                try: 
                    start_year = int(year_input)
                    print('Would you like to end your search up to another year?')
                    yes_no_input = input()
                    yes_no_input = another_year_yes_or_no_input.lower()
                    if yes_no_input == 'y' or yes_no_input == 'yes':
                        print('What year would you like to end your search on?')
                        another_year_input = input()
                        try:
                            another_year_input = int(another_year_input)
                            end_year = another_year_input
                            user_error = False
                        except ValueError:
                            print(year_error)
                    elif yes_no_input == 'n' or yes_no_input == 'no':
                        end_year = start_year
                        user_error = False
                    else:
                        print(input_error)
                except ValueError:
                    print(year_error)



        print('\nWhich month and which day would you like to start your search?')
        user_error = True
        while user_error:
            start_date_input = input()
            start_date_input = start_date_input.lower()
            start_date_input = start_date_input.split()
            if len(start_date_input) != 2:
                print(input_error)
            else:
                if start_date_input[0] in month:
                    start_month = month[start_date_input[0]]
                    try:
                        start_date = int(start_date_input[1])
                        user_error = False
                    except ValueError:
                        print(date_error)
                else:
                    print(month_error)

        print('Which month and which day would you like to search until to')
        print("NOTE: If searching up until the same month you can just put in the end date")
        user_error = True
        while user_error:
            end_date_input = input()
            end_date_input = end_date_input.lower()
            end_date_input = end_date_input.split()
            if len(end_date_input) > 1:
                if end_date_input[0] in month:
                    end_month = month[end_date_input[0]]
                    try:
                        end_date = int(end_date_input[1])
                        user_error = False
                    except ValueError:
                        print(date_error)
                else:
                    print(month_error)
            else:
                end_month = start_month
                try:
                    end_date = int(end_date_input[0])
                    user_error = False
                except ValueError:
                    print(date_error)

    ##Creates time frame from arguments in function
        try:
            start_time = datetime(year= start_year, month=start_month, day=start_date).strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            print("DATE ERROR [Start time]: Reenter date values")
        try:
            end_time = datetime(year= end_year, month=end_month, day=end_date).strftime('%Y-%m-%dT%H:%M:%SZ')
            date_time_check = False
        except ValueError:
            print("DATE ERROR [End time]: Reenter date values")


    ## Can search through different types, but I havent debugged it yet, so this is still a work in progress because I don't know how it will affect the search.
    print("\nWhere do you want to search?")
    print("[videos, channels, or playlists]")
    user_error = True
    while user_error:
        resource_input = input()
        resource_input = resource_input.lower()
        if resource_input not in resource:
            print(input_error)
        elif resource_input == 'videos':
            type_resource = 'video'
            user_error = False
        else:
            type_resource = resource_input
            user_error = False

    print("\nDid you want to adjust the results per page?")
    print("Default will return maximum value of 50")
    user_error = True
    while user_error:
        yes_no_input = input()
        yes_no_input = yes_no_input.lower()
        if yes_no_input == 'y' or yes_no_input == 'yes':
            print("How many results per page?")
            results_input = input()
            try:
                results_input = int(results_input)
            except ValueError:
                print(input_error)
        elif yes_no_input == 'n' or yes_no_input == 'no':
            print("Default value has been set to 50")
            results_input = 50
            user_error = False
        else:
            print(input_error)

    #Order of the query. Default is technically relevance, but I didn't want to code for any default values just prefer user to make their own choice.
    print("\nHow do you want to order your search?")
    print("[date, rating, relevance, title, videocount, or viewcount]")
    user_error = True
    while user_error:
        order_input = input()
        order_input = order_input.lower()
        if order_input not in order:
            print(input_error)
        elif order_input == 'videocount':
            order_select = 'videoCount'
            user_error = False
        elif order_input == 'viewcount':
            order_select = 'viewCount'
            user_error = False
        else:
            order_select = order_input
            user_error = False
    
    request = youtube.search().list(q = search_keywords, part='snippet',type = type_resource, publishedAfter=start_time, publishedBefore = end_time, order=order_select, maxResults = results_input, regionCode='US').execute()
    
    for i in range(0,len(request['items'])):
        snippet.append(request['items'][i]['snippet'])
        videoId.append(request['items'][i]['id']['videoId'])

    for vid in videoId:
        videoView = youtube.videos().list(id = vid, part='statistics').execute()
        idView =  youtube.videos().list(id = vid, part = 'snippet').execute()
        statistics.append(videoView['items'][0]['statistics'])
        try:
            tags.append(idView['items'][0]['snippet']['tags'])
        except KeyError:
            tags.append("None")
    
    df = pd.DataFrame(snippet)
    statistics_list = pd.DataFrame(statistics)
    collect_results = pd.concat([df, statistics_list], axis = 1)
    collect_results['tags'] = pd.Series(tags, dtype='object')
    
    user_input_choice = True
    nextPgToken = request['nextPageToken']
    while user_input_choice:
        print('Do you want to add more results?')
        user_input = input()
        user_input = user_input.lower()
        if user_input == 'y' or user_input == 'yes':
            
            videoId.clear()
            statistics.clear()
            tags.clear()
            snippet.clear()
            
            request_two = youtube.search().list(part='snippet',type ='video', publishedAfter=start_time, publishedBefore = end_time, order='viewCount', maxResults = 50, regionCode='US', pageToken = nextPgToken).execute()
            nextPgToken = request_two['nextPageToken']
            if len(request_two['items']) == 0:
                print("There isn't any items here to add")
                user_input_choice = False
                
            for i in range(0,len(request_two['items'])):
                snippet.append(request_two['items'][i]['snippet'])
                videoId.append(request_two['items'][i]['id']['videoId'])

            for vid in videoId:
                videoView = youtube.videos().list(id = vid, part='statistics').execute()
                idView =  youtube.videos().list(id = vid, part = 'snippet').execute()
                statistics.append(videoView['items'][0]['statistics'])
                try: 
                    tags.append(idView['items'][0]['snippet']['tags'])
                except KeyError:
                    tags.append("None")

            next_df = pd.DataFrame(snippet)
            next_statistics_list = pd.DataFrame(statistics)
            next_results = pd.concat([next_df, statistics_list], axis = 1)
            next_results['tags'] = pd.Series(tags, dtype='object')
            collect_results = pd.concat([collect_results, next_results], axis = 0, ignore_index = True)
                        
        elif user_input == 'n' or user_input == 'no':
            user_input_choice = False
        
        else:
            print(input_error)
        
    collect_results = collect_results.dropna(subset=['title', 'description'], how='any')
    
    if dataFrame is None:
        print('Search Complete')
        return collect_results
    else:
        new_dataFrame = pd.concat([dataFrame, collect_results], axis = 0, ignore_index=True)
        print('Search Complete')
        return new_dataFrame

if __name__ == '__main__':
    print("Hello, this is my Youtube Data Collector. All the relevant code and information is found within my github")
    print("If you were curious as to how this program may function, or if you have suggestions to how I can be improved definitely let me know.")
    print("If you need to run this program multiple times, I suggest importing this file and calling the relevant methods within instead of directly loading the file")
    print("\n\n\n")
    print("Do you want to start a new search or add to a previous one?")
    print("[new, add]")

    user_error = True
    while user_error:
        choice = input()
        choice = choice.lower()
        if choice == 'new':
            new_collect = youtube_collect()
            user_dataframe = youtube_collect()
            new_user = True
            user_error = False
        elif choice == 'add':
            load_error = True:
            while load_error:
                print("Input the path for the file")
                print("Path is case sensitive")
                path = input()
                try:
                    previous_dataframe = open_dataframe(path)
                    user_dataframe = youtube_collect(previous_dataframe)
                    add_user = True
                    load_error = False
                    user_error = False

                except NameError:
                    print("Path is not valid. Reenter valid path")
        else:
            print('Invalid input, please choose either [new file, load file]')

    if new_user:
        youtube_data = user_dataframe
    else:
        add_user:
        youtube_data = user_dataframe

    user_choice = True
    print("Would you like to continue and search for another time, keywords")
    while user_choice:
        yes_no_input = input()
        yes_no_input = yes_no_input.lower()
        if yes_no_input == 'yes' or yes_no_input = 'y':
            youtube_data = youtube_collect(youtube_data)
            print("Would you like to continue and search for another time, keywords?")
        elif yes_no_input == 'no' or yes_no_input = 'n':
            user_choice = False
        else:
            print(input_error)

    print("Where do you want to save your information?")
