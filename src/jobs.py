import csv, folium, uuid, os, json
from hotqueue import HotQueue
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from collections import Counter
from redis import Redis
import io

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host = redis_ip, port=6379, db=0)
q = HotQueue('queue', host = redis_ip, port = 6379, db=1)
rd2 = Redis(host = redis_ip, port=6379, db=2)

def get_launches_data() -> dict:
    '''
        This function pulls the full data csv from the current directory and formats
        it into json format for use in most other functions.

        Args:
            None
        Returns:
            data (dict) : A dictionary containing the key 'launches' that contains
            a list of dictionaries of each launch
    '''
    data = {}
    data['launches'] = []

    with open('mission_launches.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['launches'].append(dict(row))

    return(data)

# JOB HANDLING

def generate_jid() -> str:
    """
      Generate a pseudo-random identifier for a job and returns it.
      
      Returns:
          randomID (str): A random job ID.
    """
    
    randomID = str(uuid.uuid4())
    return randomID

def generate_job_key(jid):
    """
      Generate the redis key from the job id to be used when storing, retrieving or updating
      a job in the database.
      
      Returns:
          jid (str): The jobID to be used for the redis key.
    """
    return '{}'.format(jid)

def instantiate_job(jid, route, status):
    """
      Create the job object description as a python dictionary. Requires the job id, route, and status.
      
      Return:
          (dict): The job object description.
    """
    return {'id': jid,
            'route': route,
            'status': status
    }

def save_job(job_key, job_dict):
    """
    Save a job object in the rd Redis database.
    """
    rd.set(job_key, json.dumps(job_dict))

def queue_job(jid):
    """
    Adds a job id to the redis queue.
    """
    q.put(jid)

def add_job(route):
    """
    Fully creates the job ID and information regarding the job. Then it
    makes the status into submitted, and saves and queues the job. It returns the
    job ID so that it can be sent to the user during the success message.
    
    Returns:
        jid (str): The job ID.
    """
    jid = generate_jid()
    job_dict = instantiate_job(jid, route, "submitted")
    save_job(jid, job_dict)
    queue_job(jid)
    
    return jid

def update_job_status(jid, status):
    """
    Update the status of job with job id `jid` to status `status`.
    """

    job = json.loads(rd.get(jid))
    if job:
        job['status'] = status
        save_job(generate_job_key(jid), job)
    else:
        raise Exception()

def list_of_jobs():
    """
    This function creates a list of jobs that is in an easily returnable state.
    
    Returns:
        jobsList (list): The list of current jobs queued by the user.
    """
    jobsList = []
    for key in rd.keys():
        jobsList.append(json.loads(rd.get(key.decode('utf-8'))))
        
    return jobsList
        
# JOB RELATED

def get_data() -> dict:
    """
    This function returns the data from Redis, but only if it exists or is empty.
    Otherwise it will return a message saying that the data does not exist.

    Returns:
        redisData (dict): The entire gene data.
    """

    #try-except block that returns if the data doesn't exist and an error occurs because of it
    try:
        #un-seralizing the string into a dictionary
        redisData = json.loads(rd2.get('data'))
    except NameError:
        return 'The data does not exist.'
    except TypeError:
        return 'The data does not exist.'

    return redisData

def get_rocket_names_by_org(full_data_json:dict, org_name:str) -> list:
    '''
        This function gets a list of all the rockets launched by an organization.

        Args:
            full_data_json (dict) : The full data json from the database
            org_name (str) : The name of the desired organization
        Returns:
            rocket_names (list) : A list of strings of rocket names
    '''

    rocket_names = []
    for item in full_data_json['launches']:
        if item['Organisation'] == org_name:
            rocket_names.append(item['Detail'][:item['Detail'].index(" |")])

    return(rocket_names)

def get_total_cost_for_org(full_data_json:dict, org_name:str) -> float:
    '''
        This function calculates the total amount of money in millions USD that
        an organization has spent on all of their launches.

        Args:
            full_data_json (dict) : The full data json from the database
            org_name (str) : The name of the desired organization
        Returns:
            cost (float) : The total cost of all launches
    '''
    cost = 0
    for item in full_data_json['launches']:
        if item['Organisation'] == org_name:
            cost += item['Price']

    return(cost) # cost is in millions

# TODO
def get_success_rate_for_org(org_name:str) -> float:
    '''
        This function finds the mission success rate of an organization.
        
        Args:
            org_name (str) : This is the name of the desired organization
        Returns:
            success_rate (float) : This is the success rate as a ratio (between
            0.0 and 1.0)
    '''
    total_launches = 0
    successful_launches = 0
    for item in data['launches']:
        if item['Organisation'] == org_name:
            total_launces += 1
            if item['Mission_Status'] == 'Success':
                successful_launches += 1
    success_rate = success_launches / total_launches

    return(success_rate)

def list_active_rockets(full_data_json:dict) -> list:
    '''
        This function gets a list of all currently active rockets in the database.

        Args:
            full_data_json (dict) : The full data json from the database
        Returns:
            active_rockets (list) : A list of strings of all the names of the
            active rockets.
    '''
    active_rockets = []
    for item in full_data_json['launches']:
        if item['Rocket_Status'] == 'StatusActive':
            active_rockets.append(item['Detail'][:item['Detail'].index(" |")])
    active_rockets = list(set(active_rockets)) # remove duplicates from list
    return(active_rockets)

def geocode_address(address:str) -> tuple:
    '''
        This function takes the Location key value from a launche and geocodes
        it to get latitude and longitude coordinates.

        Args:
            address (str) : The Location key value from the database (ex. "New 
            Mexico, USA")
        Returns:
            coordinates (tuple) : A tuple containing the latitude and longitude
            of the country containing the address
    '''
    last_comma_index = address.rfind(",")
    country = address[last_comma_index + 1:]
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(country)
    
    
    coordinates = (location.latitude, location.longitude)
    return(coordinates)
    
def create_all_coords(full_data_json:dict) -> list:
    '''
        This function goes through the entire kaggle database and creates a list
        of coordinates for each rocket launch location.

        Args:
            full_data_json (dict) : The full data json from the database
        Returns:
            coordinate_list (list) : list of tuples containing the latitude and 
            longitudes of every launch
    '''
    
    coordinate_list = []
    count = 1
    for item in full_data_json['launches']:
        count += 1
        if count % 10 == 0:
            print(count)
        try:
            coords = geocode_address(item['Location'])
            coordinate_list.append(coords)
        except:
            continue
    return(coordinate_list)

def create_map(full_data_json:dict):
    '''
        This function creates a map of the world and places markers on each country
        that has launched spacebound rockets. These markers display how many launches
        each country has performed.

        Args:
            full_data_json (dict) : The full data json from the database
        
        Returns:
            map.html (file) : This is an html file of the map generated in the function
    '''
    coordinates = create_all_coords(full_data_json)
    coord_counts = Counter(coordinates)
    
    map_center = [0,0]
    world_map = folium.Map(location=map_center, zoom_start=2)
    for coord, count in coord_counts.items():
        lat, lon, = coord
        popup_text = f"Launches: {count}" 
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(world_map)

    map_html = world_map._repr_html_()
    return(map_html)

def country_spending_bar_graph(full_data_json:dict):
    '''
        This function searches through the database to find how much
        spending has gone into space launches in each country that we
        have data for. It returns a bar graph.

        Args:
            full_data_json (dict) : the full data json from the database
        Returns:
            spending_bar.png (png) : the .png file of the bar graph
    '''

    cost_data = {}
    for item in full_data_json['launches']: 
        address = item['Location']
        last_comma_index = address.rfind(",")
        country = address[last_comma_index + 2:]
        
        # Correct launch sites to the spending country
        if country == 'Gran Canaria':
            country = 'USA'
        elif country == 'Yellow Sea':
            country = 'China'
        elif country == 'Kazakhstan':
            country = 'Russia'
        elif country == 'Pacific Missile Range Facility':
            country = 'USA'

        # sort spending into countries. if country isnt in dict, add it
        if country in cost_data:
            try:
                cost_data[country] += float(item['Price'])
            except:
                continue
        else:
            try:
                cost_data[country] = float(item['Price'])
            except:
                continue
    countries = list(cost_data.keys())
    costs = list(cost_data.values())

    fig = plt.figure(figsize = (10, 5))

    plt.bar(countries, costs, color='maroon',width = 0.4)

    plt.xlabel('Countries')
    plt.ylabel('Total Space Launch Spending in Millions USD')
    plt.title('Total Space Launch Spending of Different Countries')

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')

    buffer.seek(0)
    plot_data = buffer.getvalue()

    return(plot_data)

def get_organization_list(full_data_json:dict) -> list:
    '''
        This function goes through the full data json and returns a list
        of all organizations in the database.

        Args:
            full_data_json (dict) : the full data json from the database
        Returns:
            organization_list (list) : list of all organizations in the database
    '''
    organization_list = []
    for item in full_data_json['launches']:
        organization_list.append(item['Organisation'])

    my_set = set(organization_list)
    organization_list = list(my_set)

    return(organization_list)






