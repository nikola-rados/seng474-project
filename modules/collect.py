import json
import requests
import time
from process import read_file


def collect_data(key, outfile, match_id, num_matches):
    '''Collects DotA 2 match data using a Steam API key

    This function outputs match data to a file. The function runs `get_match`
    a specified number of times and appends `]` to close the list. Outputs data
    to a temporary data file, which must be appended to training_data.json.

    Since we are iterating using some starting ID there is a chance that there
    are invalid responses.  In this case we simply tally the instances and
    display this to the user.

    Parameters
    ----------
    key : string
        Steam API key, we keep ours private.  If you want one you'll have to
        generate it yourself.
    outfile : string
        Name of the file you wish the data to output to
    match_id : int
        Match ID
    num_matches : int
        Number of matches to collect
    '''
    print('Start Collecting')
    invalid_ids = 0
    valid_ids = 0
    count = 1

    for i in range(num_matches):
        result = get_match(key, match_id, count, outfile, valid_ids)

        # we can't overwhelm the API
        time.sleep(2)
        match_id += 1
        count += 1

        # tally invalid cases
        if not result:
            invalid_ids += 1
        else:
            valid_ids += 1

    with open(outfile, 'a') as file:
        file.write(']')

    data = read_file(outfile)
    print('Matches loaded: {}'.format(len(data)))
    print('Invalid match IDs: {}'.format(invalid_ids))


def get_match(key, match_id, count, outfile, valid_ids):
    '''Helper function to collect individual matches

    This function appends a comma followed by a match dictionary to the json
    file.

    Parameters
    ----------
    key : string
        Steam API key, we keep ours private.  If you want one you'll have to
        generate it yourself.
    match_id : int
        Match ID
    count : int
        Classifies which loop attempt we are on

    Returns
    -------
    bool
        True if the data was collect, False if request was invalid
    '''
    api = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/'
    api_suffix = '?match_id={}&key={}'.format(match_id, key)
    data_request = requests.get(api + api_suffix)
    print('Response {}: {}'.format(count, data_request))

    # data_request is a requests.model.Response object. See link for its
    # methods:
    #   https://github.com/psf/requests/blob/master/requests/models.py#L587
    if 'Too Many Requests' in data_request.text:
        print(data_request.headers)
        print(data_request.text)

    match_data = data_request.json()

    # TODO: make new function for the code below here
    # Check if match ID returns a match
    try:
        if 'error' in match_data['result'].keys():
            # match_id returns invalid match
            print('\t{}'.format(match_data['result']['error']))
            return False
        else:
            # valid match is appended to json file
            with open(outfile, 'a+') as file:
                if valid_ids == 0:
                    file.write('[')
                    json.dump(match_data, file)

                else:
                    file.write(', ')
                    json.dump(match_data, file)
            return True

    except KeyError:
        print('KeyError: {}'.format(match_id))
        return False


def combine_data(curr_data_file, new_data_file):
    '''Combine file containing newly mined data with current dataset

       Step 1) Read both files and load them json style
       Step 2) Combine them as you would a list in Python and write it to file
       Step 3) Clean up the file to make it json readable

       Look into step 2... line 141 might be redundant since we clean then write
       in step 3.

       Parameters
       ----------
       curr_data_file : json file
       new_data_file : json file
    '''
    # TODO: look at https://docs.python.org/2/library/tempfile.html
    # Step 1
    with open(curr_data_file, 'r') as file:
        curr_data = json.load(file)

    with open(new_data_file, 'r') as file:
        new_data = json.load(file)

    print('Current data size: {}'.format(len(curr_data)))
    print('New data size: {}'.format(len(new_data)))

    # Step 2
    combined_data = curr_data + new_data

    print('Combined data size: {}'.format(len(combined_data)))

    with open(curr_data_file, 'w') as file:
        file.write(str(combined_data))

    # Step 3
    with open(curr_data_file, 'r') as file:
        clean_data = file.read()

    clean_data = data.replace('\'', '\"')
    clean_data = data.replace('True', 'true')
    clean_data = data.replace('False', 'false')

    with open(curr_data_file, 'w') as file:
        file.write(data)

    with open(new_data_file, 'w') as file:
        # delete contents of new_data_file
        file.truncate()
