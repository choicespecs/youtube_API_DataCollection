from googleapiclient.discovery import build
import pandas as pd
import numpy as np
from datetime import datetime
api_key = '[Insert your api key here]'
youtube = build('youtube', 'v3', developerKey = api_key)

def youtube_collect_by_date(year, month, start_day, end_day, dataFrame=None):
	title = []
	description = []
	videoId = []
	publishTime = []
	statistics = []

	start_time = datetime(year= year, month=month, day=start_day).strftime('%Y-%m-%dT%H:%M:%SZ')
	end_time = datetime(year= year, month=month, day=end_day).strftime('%Y-%m-%dT%H:%M:%SZ')	
	request = youtube.search().list(part='snippet',type ='video', publishedAfter=start_time, publishedBefore = end_time, order='viewCount', maxResults = 50, regionCode='US').execute()

	for i in range(0,len(request['items'])):
		title.append(request['items'][i]['snippet']['title'])
		description.append(request['items'][i]['snippet']['description'])
		videoId.append(request['items'][i]['id']['videoId'])
		publishTime.append(request['items'][i]['snippet']['publishTime'])

	df = pd.DataFrame({'title':title,'description':description,'videoId':videoId, 'publishTime':publishTime})

	for vid in df['videoId']:
		videoView = youtube.videos().list(id = vid, part='statistics').execute()
		statistics.append(videoView['items'][0]['statistics'])

	statistics_list = pd.DataFrame(statistics)
	collect_results = pd.concat([df, statistics_list], axis = 1)
	
	if dataFrame is None:
		return collect_results

	else:
		new_dataFrame = pd.concat([dataFrame, collect_results], axis = 0, ignore_index=True)
		return new_dataFrame
