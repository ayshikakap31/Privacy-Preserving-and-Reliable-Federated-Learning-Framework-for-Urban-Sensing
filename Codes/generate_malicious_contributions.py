import numpy as np

def simulate_malicious_contributions(participant_position_measurement,no_of_models,malicious_user_percent,no_of_participants_each_model):
    min_percent_change = 20
    max_percent_change = 100
    participant_position_measurement_malicious = participant_position_measurement.copy()
    
    for i1 in range(no_of_models):
        no_of_malicious_users = int(np.floor((malicious_user_percent * no_of_participants_each_model) / 100))
        malicious_users = np.random.choice(no_of_participants_each_model, no_of_malicious_users, replace=False)
        
        for i in range(len(malicious_users)):
            this_malicious_user = malicious_users[i]
            this_malicious_user_data = np.empty((1,1,30))
            this_malicious_user_data[:,:,:] = participant_position_measurement_malicious[i1, this_malicious_user, :, 2]
            wrong_data_direction = np.random.randint(0, 2, size=this_malicious_user_data.shape)
            data_change_percent = np.random.rand(*this_malicious_user_data.shape) * (max_percent_change - min_percent_change) + min_percent_change
            data_change = (data_change_percent * this_malicious_user_data) / 100
            this_malicious_user_data_changed = np.zeros_like(this_malicious_user_data) + np.nan
            a, _, c = this_malicious_user_data.shape
            
            for j in range(a):
                for k in range(c):
                    if wrong_data_direction[j, 0, k] == 0:
                        this_malicious_user_data_changed[j, 0, k] = this_malicious_user_data[j, 0, k] - data_change[j, 0, k]
                    else:
                        this_malicious_user_data_changed[j, 0, k] = this_malicious_user_data[j, 0, k] + data_change[j, 0, k]
            
            participant_position_measurement_malicious[i1, this_malicious_user, :, 2] = this_malicious_user_data_changed
            
    return participant_position_measurement_malicious, no_of_malicious_users