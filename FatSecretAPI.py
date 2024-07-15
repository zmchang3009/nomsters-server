import requests
import asyncio
import aiohttp
import time  # Import time module for timestamp handling
import re


accesstoken = 'placeholder'
last_update_timestamp = 0  # Initialize to 0 indicating the token has never been updated
clientId =  'placeholder' 
clientsecret =  'placeholder'

# run this function to get the access token, expires eevery 24 hours
def get_access_token_from_fatsecret():
    global accesstoken, last_update_timestamp  # Use global variables
    url = 'https://oauth.fatsecret.com/connect/token'
    response = requests.post(url, auth=(clientId, clientsecret), data={'grant_type': 'client_credentials', 'scope': 'basic'}, params={'format': 'json'})
    if response.status_code == 200:
        print("API request successful!")
        accesstoken = response.json()['access_token']  # Update the access token
        last_update_timestamp = time.time()  # Update the timestamp to current time
        print(response.text)
    else:
        print('API request failed')
        print(response.text)

def check_token_expiry_and_refresh():
    global last_update_timestamp
    current_time = time.time()
    if current_time - last_update_timestamp > 86400:  # Check if more than 86400 seconds have passed
        get_access_token_from_fatsecret()  # Refresh the token


def extract_calorie_count(json_obj):
    res = []
    if 'foods' in json_obj and 'food' in json_obj['foods']:
        food_list = json_obj['foods']['food']
        if isinstance(food_list, dict):
            food_list = [food_list]
        print(food_list)
        for food in food_list:
            calorie_count = None
            food_name = None
            portion_size = None
            if 'food_description' in food:
                description = food['food_description']
                # Match the calorie count
                calorie_match = re.search(r'Calories:\s+(\d+)', description)
                portion_match = re.search(r'Per\s+([^-]+)-', description)
                
                if calorie_match and portion_match:
                    calorie_count = int(calorie_match.group(1))
                    portion_size = portion_match.group(1).strip()
                    food_name = food['food_name']
                    res.append({'portion_size': portion_size, 'calorie_count':calorie_count, 'food_name':food_name})
    return res

def find_reasonable_portion(dictionaries):
                print('finding reasonable portion')
                reasonable_portion = None
                for dictionary in dictionaries:
                    portion_size = dictionary.get('portion_size')
                    if portion_size:
                        if ' serving' in portion_size:
                            print("serving")
                            try:
                                serving = int(portion_size.split(' serving')[0])
                                if serving < 2:
                                    reasonable_portion = dictionary
                                    break
                            except ValueError:
                                print('serving parse error ')
                        if 'g' in portion_size and any(char.isdigit() for char in portion_size.split('g')[0]):
                            print("g")
                            try:
                                weight = int(portion_size.split('g')[0])
                                if weight < 300:
                                    reasonable_portion = dictionary
                                    break
                            except ValueError:
                                print('g parse error ')
                        if 'oz' in portion_size and any(char.isdigit() for char in portion_size.split('oz')[0]):
                            print("oz")
                            try:
                                weight = int(portion_size.split('oz')[0])
                                if weight < 10:
                                    reasonable_portion = dictionary
                                    break
                            except ValueError:
                                print('oz parse error ')
                        if ' cup' in portion_size:
                            print("cup")
                            try:
                                numCups = int(portion_size.split(' cup')[0])
                                if numCups < 2:
                                    reasonable_portion = dictionary
                                    break
                            except ValueError:
                                print('cup parse error ')
                        if ' bowl' in portion_size:
                            print("bowl")
                            try:
                                numBowls = int(portion_size.split(' bowl')[0])
                                if numBowls < 2:
                                    reasonable_portion = dictionary
                                    break
                            except ValueError:
                                print('bowl parse error ')
                        else:
                            print("default")
                            reasonable_portion = dictionary
                            break
                if len(dictionaries) > 0 and reasonable_portion == None:
                    print("no reasonable portion found:", dictionaries, reasonable_portion)
                return reasonable_portion

async def make_API_call_to_fatsecret(label, accesstoken):
    # Send a GET request to the API with parameters
    url = 'https://platform.fatsecret.com/rest/server.api'
    async with aiohttp.ClientSession() as session:
        print('making request')
        async with session.get(url, params={'method': 'foods.search', 'max_results': '5', 'search_expression': label, 'format': 'json', 'region': 'SG', 'flag_default_serving': 'true'}, headers={'Authorization': 'Bearer ' + accesstoken}) as response:
            if response.status == 200:
                foods = await response.json()
            else:
                foods = None
            return foods

async def main(labels):
    tasks = []
    # labels = ["sweet and sour pork", "chicken soup", "fried rice", 'bubble tea', 'fried chicken', 'chicken breast', 'nasi lemak', 'curry']  # Example labels, modify as needed
    # labels = dishes[1:5]

    for label in labels:
        task = asyncio.create_task(make_API_call_to_fatsecret(label, accesstoken))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    ret = []
    for result in results:
        if result is not None:
            print("API request successful!")
            print(result)
            calArray = extract_calorie_count(result)
            bestGuess = find_reasonable_portion(calArray)
            print(bestGuess, len(calArray)) 
            print('\n')
            ret.append(bestGuess)
        else:
            print("API request failed")
            ret.append(None)
    return ret

def fetch_calorie_data(labels):   
    try:
        # Try to get the existing event loop
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            # If the loop is closed, create a new loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError as e:
        # If no current event loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Now, run your main function with the (possibly new) event loop
    check_token_expiry_and_refresh()
    result = loop.run_until_complete(main(labels=labels))
    return result
