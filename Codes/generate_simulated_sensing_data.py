import numpy as np
from scipy.spatial.distance import cdist

def simulated_sensing_data(latitude_lim,longitude_lim,no_of_models, no_of_participants_each_model, timestamp_max,parameter,latitude_all,longitude_all):
    # Generating participatory sensed data from participants
    speed_x_min = 60
    speed_x_max = 100
    speed_y_min = 60
    speed_y_max = 100
    latitude_length = latitude_lim[1] - latitude_lim[0]
    y_length = longitude_lim[1] - longitude_lim[0]
    participant_position_measurement = np.full((no_of_models, no_of_participants_each_model, timestamp_max, 3), np.nan)
    
    for random_iter_no in range(no_of_models):
        start_time = np.random.randint(timestamp_max, size=no_of_participants_each_model)
        sensing_time = np.random.randint(timestamp_max, size=no_of_participants_each_model)
        end_time = start_time + sensing_time
        end_time[end_time > timestamp_max] = timestamp_max
        
        # movement direction: 0=+ve, 1=-ve;
        direction_x = np.random.randint(0, 2, size=no_of_participants_each_model)
        direction_y = np.random.randint(0, 2, size=no_of_participants_each_model)
        
        for i in range(no_of_participants_each_model):
            this_starting_position_x = latitude_lim[0] + np.random.rand() * (latitude_lim[1] - latitude_lim[0])
            this_starting_position_y = longitude_lim[0] + np.random.rand() * (longitude_lim[1] - longitude_lim[0])
            this_starting_time = start_time[i]
            this_ending_time = end_time[i]
            
            participant_position_measurement[random_iter_no, i, this_starting_time, 0] = this_starting_position_x
            participant_position_measurement[random_iter_no, i, this_starting_time, 1] = this_starting_position_y
            
            parameter_all = parameter[:, :, this_starting_time].flatten()
            D = cdist(np.column_stack((latitude_all, longitude_all)), np.array([[this_starting_position_x, this_starting_position_y]]))
            idx = np.argmin(D)
            participant_position_measurement[random_iter_no, i, this_starting_time, 2] = parameter_all[idx]
            
            for j in range(this_starting_time + 1, this_ending_time):
                x_change = speed_x_min + np.random.rand() * (speed_x_max - speed_x_min)
                y_change = speed_y_min + np.random.rand() * (speed_y_max - speed_y_min)
                this_x = 0
                this_y = 0
                
                while not (latitude_lim[0] < this_x < latitude_lim[1] and longitude_lim[0] < this_y < longitude_lim[1]):
                    if direction_x[i] == 0:
                        this_x = participant_position_measurement[random_iter_no, i, j - 1, 0] + x_change
                    else:
                        this_x = participant_position_measurement[random_iter_no, i, j - 1, 0] - x_change
                    
                    if direction_y[i] == 0:
                        this_y = participant_position_measurement[random_iter_no, i, j - 1, 1] + y_change
                    else:
                        this_y = participant_position_measurement[random_iter_no, i, j - 1, 1] - y_change
                    
                    if this_x < latitude_lim[0]:
                        direction_x[i] = 0
                    if this_x > latitude_lim[1]:
                        direction_x[i] = 1
                    if this_y < longitude_lim[0]:
                        direction_y[i] = 0
                    if this_y > longitude_lim[1]:
                        direction_y[i] = 1
                
                participant_position_measurement[random_iter_no, i, j, 0] = this_x
                participant_position_measurement[random_iter_no, i, j, 1] = this_y
                
                parameter_all = parameter[:, :, j].flatten()
                D = cdist(np.column_stack((latitude_all, longitude_all)), np.array([[this_x, this_y]]))
                idx = np.argmin(D)
                participant_position_measurement[random_iter_no, i, j, 2] = parameter_all[idx]
                
    return participant_position_measurement