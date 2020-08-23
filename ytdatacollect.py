## Relevant libraies to import
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
from datetime import datetime

## Youtube API key & load API
api_key = '[Insert your api key here]'
youtube = build('youtube', 'v3', developerKey = api_key)

## function which takes dates to collect information
def youtube_collect_by_date(year, month, end_month, start_day, end_day, dataFrame=None):
    
    ##Empty lists of information that is collected for dataframe
    title = []
    description = []
    videoId = []
    publishTime = []
    statistics = []
    channelTitle = []
    tags = []

    #Collection of different lists, dictionaries used to compare input between possible inputs for potential errors
    month = {'january': 1, 'february': 2, 'march':3, 'april':4, 'may': 5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
    resource = ['channel','playlist','video']
    order = ['date', 'rating','relevance','title','videocount','viewcount']
    
    # All error messages for invalid inputs
    date_error = 'Invalid Input. You must type an integer for the date'
    month_error = 'Invalid Input. You must type in a valid month'
    year_error = 'Invalid Input. You must type in a integer for the year'
    input_error = 'Invalid Input. Please reenter your input'


    print("Hello, I'm the youtube collector. I'm going to ask a lot of specific questions to help you with your search")
    print("First, Do you have any specific words you are looking for in your search? (Y/N)")

    # Will look for search terms to search for first, this can be optional since you do not necessarily need any search terms to query through
    user_error = True
    while user_error:
        yes_no_input = input()
        yes_no_input = yes_no_input.lower()

        if yes_no_input == 'y':
            print('What are your search keywords? (input words or None)')
            search_input = input()
            search_input = search_input.lower()
                if search_input != 'none':
                    search_keywords = search_input
                    user_error = False
                else:
                    print('There may have been a slight mistake I guess. Let us continue')
                    user_error = False
        elif yes_no_input == 'n':
            print("Okay we will just continue on.")
            user_error = False
        else:
            print(input_error)

    print("Next, let's go through some dates together. First, I want to know the years you want to search through")

    # Dates however, are not so optional. This will look through specific dates for the user. First, asking for year and then asking for month and days to look through
    user_error = True
    while user_error:
        print('Which year would you like to begin your search')
        year_input = input()
        if len(year_input) > 1:
            print('Invalid input. You must ONLY type in the year')
        else:
            try: 
                start_year = int(year_input)
                print('Would you like to end your search up to another year? (Y/N)')
                another_year_yes_or_no_input = input()
                another_year_yes_or_no_input = another_year_yes_or_no_input.lower()
                if another_year_yes_or_no_input == 'y':
                    print('What year would you like to end your search on?')
                    another_year_input = input()
                    try:
                        another_year_input = int(another_year_input)
                        end_year = another_year_input
                        user_error = False
                    except ValueError:
                        print(year_error)
                elif another_year_yes_or_no_input == 'n':
                    end_year = year
                    print("Okay let's continue on")
                    user_error = False
                else:
                    print(input_error)
            except ValueError:
                print(year_error)

    print("Let's now discuss specific months and dates. Remember to type in the month like January or March and then with a space type in the date you want as well as a number like 30 or 10")
    
    print('Which month and which day would you like to start your search?')
    user_error = True
    while user_error:
        start_date_input = input()
        start_date_input = month_input.lower()
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
    ##start_time = datetime(year= year, month=month, day=start_day).strftime('%Y-%m-%dT%H:%M:%SZ')
    ##end_time = datetime(year= year, month=end_month, day=end_day).strftime('%Y-%m-%dT%H:%M:%SZ')    
    
    start_time = datetime(year= start_year, month=start_month, day=start_date).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime(year= end_year, month=end_month, day=end_date).strftime('%Y-%m-%dT%H:%M:%SZ')

    ## Can search through different types, but I havent debugged it yet, so this is still a work in progress because I don't know how it will affect the search.
    print("Since we have the dates, let's now figure out if you are searching for videos, channels, or playlists")
    user_error = True
    while user_error:
        resource_input = input()
        resource_input = resource_input.lower()
        if resource_input not in resource:
            print(input_error)
        else:
            type_resource = resource_input
            user_error = False


    #Order of the query. Default is technically relevance, but I didn't want to code for any default values just prefer user to make their own choice.
    print("Finally, I want to figure out the order you want to search")
    print("You can only order your search by: date, rating, relevance, title, videocount, or viewcount")
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

    request = youtube.search().list(part='snippet',type ='video', publishedAfter=start_time, publishedBefore = end_time, order='viewCount', maxResults = 50, regionCode='US').execute()
    
    for i in range(0,len(request['items'])):
        title.append(request['items'][i]['snippet']['title'])
        description.append(request['items'][i]['snippet']['description'])
        videoId.append(request['items'][i]['id']['videoId'])
        publishTime.append(request['items'][i]['snippet']['publishTime'])

    ##df = pd.DataFrame({'title':title,'description':description,'videoId':videoId, 'publishTime':publishTime})

    ##for vid in df['videoId']:
    for vid in videoId:
        videoView = youtube.videos().list(id = vid, part='statistics').execute()
        idView =  youtube.videos().list(id = vid, part = 'snippet').execute()
        statistics.append(videoView['items'][0]['statistics'])
        tags.append(idView['items'][0]['snippet']['tags'])
        channelTitle.append(idView['items'][0]['snippet']['channelTitle'])
    
    df = pd.DataFrame({'title': title, 'description': description, 'videoId': videoId, 'publishTime':publishTime, 'tags': tags, 'channelTitle' : channelTitle})
    
    statistics_list = pd.DataFrame(statistics)
    collect_results = pd.concat([df, statistics_list], axis = 1)
    #collect_results['tags'] = pd.Series(tags, dtype='object')
    #collect_results['channeltitle'] = pd.Series(channelTitle, dtype='object')
    
    user_input_choice = True
    nextPgToken = request['nextPageToken']
    while user_input_choice:
        print('Do you want to add more results? Y/N')
        user_input = input()
        user_input = user_input.lower()
        if user_input == 'y':
            
            title.clear()
            description.clear()
            videoId.clear()
            publishTime.clear()
            statistics.clear()
            channelTitle.clear()
            tags.clear()
            
            request_two = youtube.search().list(part='snippet',type ='video', publishedAfter=start_time, publishedBefore = end_time, order='viewCount', maxResults = 50, regionCode='US', pageToken = nextPgToken).execute()
            nextPgToken = request_two['nextPageToken']
            if len(request_two['items']) == 0:
                print("There isn't any items here to add")
                user_input_choice = False
                
            for i in range(0,len(request_two['items'])):
                title.append(request_two['items'][i]['snippet']['title'])
                description.append(request_two['items'][i]['snippet']['description'])
                videoId.append(request_two['items'][i]['id']['videoId'])
                publishTime.append(request_two['items'][i]['snippet']['publishTime'])

            ##next_df = pd.DataFrame({'title':title,'description':description,'videoId':videoId, 'publishTime':publishTime})

            ##for vid in next_df['videoId']:
            for vid in videoId:
                videoView = youtube.videos().list(id = vid, part='statistics').execute()
                idView =  youtube.videos().list(id = vid, part = 'snippet').execute()
                statistics.append(videoView['items'][0]['statistics'])
                if len(idView['items'][0]['snippet']['tags']) != 0:
                    tags.append(idView['items'][0]['snippet']['tags'])
                else:
                    tags.append('None')
                channelTitle.append(idView['items'][0]['snippet']['channelTitle'])

            next_df = pd.DataFrame({'title': title, 'description': description, 'videoId': videoId, 'publishTime':publishTime, 'tags': tags, 'channelTitle' : channelTitle})

            next_statistics_list = pd.DataFrame(statistics)
            next_results = pd.concat([next_df, statistics_list], axis = 1)
            #next_results['tags'] = pd.Series(tags, dtype='object')
            #next_results['channeltitle'] = pd.Series(channelTitle, dtype='object')
            collect_results = pd.concat([collect_results, next_results], axis = 0, ignore_index = True)
                        
        elif user_input == 'n':
            user_input_choice = False
        
        else:
            print('You must choose only y or n')
    
    if dataFrame is None:
        print('Search Complete')
        return collect_results
    else:
        new_dataFrame = pd.concat([dataFrame, collect_results], axis = 0, ignore_index=True)
        print('Search Complete')
        return new_dataFrame