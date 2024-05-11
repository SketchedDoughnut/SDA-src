all_releases = 'https://api.github.com/repos/SketchedDoughnut/development/releases?page=1&per_page=10000'

import requests

# get requests json
all_response = requests.get(all_releases).json()

# setup var(s)
release_data = []

# parse response_data
c = 0
for response in all_response:
    label = response['body'].split()[0]
    mode = response['body'].split()[1]
    try:
        bounds = response['body'].split()[2]
        release_data.append([label, mode, bounds])
    except Exception as e:
        #print('bounds error:', e)
        #print('count:', c)
        #print(response['tag_name'])
        c += 1
        pass
print('----------------------------')
print('Loaded releases parsed')
print('Total skips:', c)






def find_data(current_in: str):
    # Tcurrent_mode = ''
    # Tcurrent_state = ''
    #print('current mode', current_in)

    # check if current_in (label) is in list 
    for data in release_data:
        if data[0] == current_in:
            within = True
            break
        else:
            within = False

    # default data if not within list
    if not within:
        print('It appears you have an invalid or outdated label. Defaulting to full, forced')
        return 'full', 'forced'

    # go through list, find mode of current label
    for i in release_data:
        #print('looping', i)
        if i[0] == current_in:
            print('Mode found:', i[1])
            try:
                Tcurrent_mode = i[1]
                Tcurrent_state = i[2]
                break
            except Exception as e:
                print('Error assigning variables:', e)
                print('This is likely due to an outdated system.')
                print('Due to this, your update will be defaulted to full, forced')
                return 'full', 'forced'
    try:
        return Tcurrent_mode, Tcurrent_state
    except Exception as e:
        print('Return error:', e)
        input('Enter anything to exit: ')
        exit()

def eval_modes(current: str):
    # get mode based off of current
    print('Evaluating...')
    print('----------------------------')
    print('Getting mode and state based off of label...')
    current_mode, state = find_data(current)
    #find_data(current)
    new_mode = current_mode

    l = 0

    # measure
    ran = False

    for rd in release_data:
        if rd[0] == current: # if labels equal
            print('Scan has returned to previous, finishing.')
            print('Looped:', l)
            break
        else:
            l += 1
            if new_mode == 'game_data':
                if rd[1] == 'top':
                    #print(f'- promoting {current_mode} to {rd[1]}')
                    #new_mode = rd[1] #####################################

                    # full broken, force to full
                    print(f'- promoting {current_mode} to full')
                    new_mode = 'full'
                    ran = True
                elif rd[1] == 'full':
                    print(f'- promoting {current_mode} to {rd[1]}')
                    new_mode = rd[1]
                    ran = True
            elif new_mode == 'top':
                if rd[1] == 'full':
                    print(f'- promoting {current_mode} to {rd[1]}')
                    new_mode = rd[1]
                    ran = True

    print('----------------------------')
    print('Mode promoted to:', new_mode)
    return current_mode, new_mode, state, ran

#current_mode, m_detect = eval_modes()
#print('Mode promoted to:', current_mode)
