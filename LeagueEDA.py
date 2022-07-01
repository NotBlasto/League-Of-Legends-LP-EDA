#Importing required libraries
import requests 
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import numpy as np
import secret

#Function to pull the Summonername of users that are currently have a True HotStreak value (Consecutively winning).
def pullSummoners(repetition, api_key):
    #List to store Summoners(Players) that are on a HotStreak
    summoners_with_hot_streak = []
    for o in range(repetition):
        o+=1
        url = "https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page="+str(o)+"&api_key="+api_key
        url_response = requests.get(url).json()
        #Looping through our initial response for summoners with a True HotStreak value and appending to list
        for summoners in url_response:
            hot_streak = summoners['hotStreak']
            summoner_name = summoners['summonerName']
            if hot_streak == True:
                summoners_with_hot_streak.append(summoner_name)
    return summoners_with_hot_streak

#Function to webdrive pulled Summonernames into U.gg. 
def getData(summoners_with_hot_streak):
    # Creating Master Dataframe
    df = pd.DataFrame(columns=['Username','LP','VictoryStatus']) 
    #Providing additional options to our webdriver for error handling
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery");
    options.add_argument("--start-maximized")
    options = Options()
    #Creating webdriver
    browser = webdriver.Chrome(r'C:\Users\justi\OneDrive\Desktop\Chromedriver\chromedriver.exe', options=options)
    #Providing initial website url to webdriver
    url = 'https://u.gg/'
    browser.get(url)
    for i in range(len(summoners_with_hot_streak)):
        time.sleep(25) #Program sleeps for allotted time to allow web elements to load, and increase query time.
        search_bar = browser.find_element(by=By.NAME, value="query")#Finding search bar element
        if search_bar.is_displayed(): #Ensuring search bar element is displayed
            search_bar.send_keys(summoners_with_hot_streak[i], Keys.ENTER) #Sending usernames to searchbar
            time.sleep(5) # allowing time to load
        else:
            browser.get(url)
            time.sleep(15) 
            search_bar.send_keys(summoners_with_hot_streak[i], Keys.ENTER)
            time.sleep(5) # allowing time to load


        #Assigning VictoryStatus and LP values to browser elements.
        player_LP = browser.find_elements(by=By.XPATH, value='//span[@class="lp-value"]')
        player_victory_status = browser.find_elements(by=By.XPATH, value='//div[@class="victory-status"]')

        #Loops to retrieve VictoryStatus and LP values
        player_lp_list = []
        for p in range(len(player_LP)):
            player_lp_list.append(player_LP[p].text)

        victory_status_list = []
        for v in range(len(player_victory_status)):
            victory_status_list.append(player_victory_status[v].text)
        browser.refresh() #Refreshing the page to clear the Searchbar, allowing a new username to be sent.

        data_tuples = list(zip(player_lp_list,victory_status_list)) # List pairing the VictoryStatus to the Amount of LP to understand if the LP was gained or lost.
        temp_df = pd.DataFrame(data_tuples, columns=['LP','VictoryStatus']) # Creates dataframe of each tuple in list
        temp_df['Username'] = summoners_with_hot_streak[i] #Adds the username associated with each game
        #print(data_tuples)
        df = pd.concat([temp_df,df]) #Appends to master dataframe
        df=(df.replace(r'^\s*$', np.nan, regex=True)) #replacing all empty spaces with NaN values
        df = df.replace(to_replace =["? LP"], value =np.nan) #replacing all ?LP with NaN values
        df = df.dropna() #Dropping rows with all NaN values
    print ('Successfully pulled ' + str(df.VictoryStatus.count()) + ' games from ' + str((len(summoners_with_hot_streak))) + ' summoners')
    browser.close() #Closes browser
    return df
#Sorting pulled user matches into games won consecutively and nonconsecutively and creating dataframes for each.
def sortData(df):
    index_counter = 1
    victory_counter = 0
    win_counter = 0
    consecutive_win = []
    consecutive_win_name = []
    normal_win_loss = []
    normal_win_loss_name = []

    for eachusername in df.Username:
        if index_counter < (len(df.Username)):
            next_username = df.iloc[index_counter].at['Username']
            win = df.iloc[victory_counter].at['VictoryStatus']
            lp = df.iloc[victory_counter].at['LP']
            index_counter+=1
            victory_counter+=1
            if eachusername == next_username:
                if win == 'WIN':
                    win_counter+=1
                    if win_counter >= 2:
                        consecutive_win.append(lp)
                        consecutive_win_name.append(eachusername)
                    else:
                        normal_win_loss.append(lp)
                        normal_win_loss_name.append(eachusername)
                elif win == 'LOSS':
                    win_counter = 0
            elif eachusername != next_username:
                if win == 'WIN':
                    win_counter+=1
                    if win_counter>=2:
                        consecutive_win.append(lp)
                        consecutive_win_name.append(eachusername)
                        win_counter = 0
                    else:
                        normal_win_loss.append(lp)
                        normal_win_loss_name.append(eachusername)
                        win_counter = 0
                elif win == 'LOSS':
                    win_counter = 0 
    final_consecutive_win = list(zip(consecutive_win, consecutive_win_name))
    final_normalwinloss = list(zip(normal_win_loss,normal_win_loss_name))
    consecutive_win_df = pd.DataFrame(final_consecutive_win, columns=['LP of Consecutive Wins', 'Username'])
    consecutive_win_df["LP of Consecutive Wins"] = consecutive_win_df["LP of Consecutive Wins"].str[:2]
    consecutive_win_df["LP of Consecutive Wins"] = consecutive_win_df["LP of Consecutive Wins"].astype(int)
    consecutive_win_df['AVG LP Gained of Consecutive Wins'] = consecutive_win_df["LP of Consecutive Wins"].mean()
    normal_win_loss_df = pd.DataFrame(final_normalwinloss, columns=['LP of Nonconsecutive Wins', 'Username'])
    normal_win_loss_df["LP of Nonconsecutive Wins"] = normal_win_loss_df["LP of Nonconsecutive Wins"].str[:2]
    normal_win_loss_df["LP of Nonconsecutive Wins"] = normal_win_loss_df["LP of Nonconsecutive Wins"].astype(int)
    normal_win_loss_df['AVG LP Gained of Nonconsecutive Wins'] = normal_win_loss_df["LP of Nonconsecutive Wins"].mean()
    return consecutive_win_df, normal_win_loss_df

#Function to export dataframes to csv files.
def toCSV(df, consecutive_win_df, normal_win_loss_df):
    consecutive_win_df.to_csv('ConsecutiveWins.csv')
    normal_win_loss_df.to_csv('NonConsecutiveWins.csv')
    df.to_csv('AllGameData.csv')
    print ('Dataframes successfully exported.')

#Main 
def main():
    api_key = secret.api_key
    data = getData(pullSummoners(3,api_key))
    data2, data3 = sortData(data)
    toCSV(data, data2, data3)

main()
