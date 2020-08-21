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
    title = []
    description = []
    videoId = []
    publishTime = []
    statistics = []
    channelTitle = []
    tags = []
    
    start_time = datetime(year= year, month=month, day=start_day).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime(year= year, month=end_month, day=end_day).strftime('%Y-%m-%dT%H:%M:%SZ')	
    request = youtube.search().list(part='snippet',type ='video', publishedAfter=start_time, publishedBefore = end_time, order='viewCount', maxResults = 50, regionCode='US').execute()
    
    ## Will create original dataframe for first results
    for i in range(0,len(request['items'])):
        title.append(request['items'][i]['snippet']['title'])
        description.append(request['items'][i]['snippet']['description'])
        videoId.append(request['items'][i]['id']['videoId'])
        publishTime.append(request['items'][i]['snippet']['publishTime'])

    df = pd.DataFrame({'title':title,'description':description,'videoId':videoId, 'publishTime':publishTime})

    for vid in df['videoId']:
        videoView = youtube.videos().list(id = vid, part='statistics').execute()
        idView =  youtube.videos().list(id = vid, part = 'snippet').execute()
        statistics.append(videoView['items'][0]['statistics'])
        tags.append(idView['items'][0]['snippet']['tags'])
        channelTitle.append(idView['items'][0]['snippet']['channelTitle'])
        
    statistics_list = pd.DataFrame(statistics)
    collect_results = pd.concat([df, statistics_list], axis = 1)
    collect_results['tags'] = tags
    collect_results['channeltitle'] = channelTitle
    
    print('Do you want to add more results? Y/N')
    user_input_choice = True
    nextPgToken = request['nextPageToken']
    while user_input_choice:
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

            next_df = pd.DataFrame({'title':title,'description':description,'videoId':videoId, 'publishTime':publishTime})

            for vid in next_df['videoId']:
                videoView = youtube.videos().list(id = vid, part='statistics').execute()
                idView =  youtube.videos().list(id = vid, part = 'snippet').execute()
                statistics.append(videoView['items'][0]['statistics'])
                if len(idView['items'][0]['snippet']['tags']) != 0:
                    tags.append(idView['items'][0]['snippet']['tags'])
                else:
                    tags.append('None')
                channelTitle.append(idView['items'][0]['snippet']['channelTitle'])
        
            next_statistics_list = pd.DataFrame(statistics)
            next_results = pd.concat([next_df, statistics_list], axis = 1)
            next_results['tags'] = tags
            next_results['channeltitle'] = channelTitle
            collect_results = pd.concat([collect_results, next_results], axis = 0, ignore_index = True)
            
            print("Do you want to add more results? Y/N")
            
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