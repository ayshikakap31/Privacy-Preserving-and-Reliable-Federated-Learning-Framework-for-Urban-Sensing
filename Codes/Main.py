# Import libraries
import numpy as np
from scipy.spatial.distance import cdist
from generate_simulated_sensing_data import simulated_sensing_data
from non_malicious_model_update import models_with_non_malicious_users
from generate_malicious_contributions import simulate_malicious_contributions
from generate_models_with_malicious_contributions_from_users import models_with_malicious_contributions
from generate_models_with_statistics_based_anomaly_detection import models_with_detected_anomalies_and_correction
from generate_models_with_anamalous_contribution_and_user_detection import detect_anomalous_contribution_and_user
from inverse_distance_weighting import inverse_distance_weighting
# Set a random seed for reproducibility
np.random.seed(0)

# Load ground truth data of physical parameter levels
# X: x-axis latitude, Y: y-axis longitude, Z: Parameter value levels
data = np.load('parameter_data.npz')
latitude = data['X'][:, :105]
longitude = data['Y'][:, :105]
parameter = data['Z'][:, :105,:]

# Extract dimensions of the data
length, width = latitude.shape

# Flatten latitude and longitude arrays for further processing
latitude_all = latitude.flatten()
longitude_all = longitude.flatten()

# Define geographical limits
latitude_lim = [223460, 224540]
longitude_lim = [6757130, 6758700]

# Set the maximum timestamp value
timestamp_max = 30

# Parameter settings
total_no_of_users = 5000
no_of_models = 10
no_of_participants_each_model = total_no_of_users // no_of_models
m_hop = 3
malicious_user_percent = 5
sigma_factor = 2

# Inverse Distance Weighting (IDW) parameters
power = -2
dmax = 100

# To generate simulated sensing data for participant positions
participant_position_measurement = simulated_sensing_data(latitude_lim,longitude_lim,no_of_models, no_of_participants_each_model, timestamp_max,parameter,latitude_all,longitude_all)

# Utilising a non-malicious m-hop with m=3 application update model to create physical parameter models from user data
v_point_no_malicious_average = models_with_non_malicious_users(participant_position_measurement,length, width, timestamp_max, no_of_models,latitude, longitude, m_hop,dmax,power)

# Simulating the generation of malicious contributions from participants
participant_position_measurement_malicious, no_of_malicious_users = simulate_malicious_contributions(participant_position_measurement,no_of_models,malicious_user_percent,no_of_participants_each_model)

# Simulating the generation of physical parameter models without correcting for intentional malicious contributions from participants
# using the m-hop with m=3 application update model.
v_point_malicious_average, v_point_malicious, Xi, Yi = models_with_malicious_contributions(participant_position_measurement_malicious,length, width, timestamp_max, no_of_models,latitude,longitude,m_hop, dmax, power)

# Implementing statistics-driven anomaly detection and correction for generating aggregated physical parameter models at the application server.
v_point_malicious_anomalies_removed, v_point_malicious_average_remove_anomaly = models_with_detected_anomalies_and_correction(v_point_malicious, sigma_factor)

# Implementing detection of anomalous contributions and anomalous user detection at the user device
top_anomalous_users, top_anomalous_user_score = detect_anomalous_contribution_and_user(participant_position_measurement_malicious,no_of_models, no_of_participants_each_model, 
                                                                                       timestamp_max,length, width, Xi, Yi, dmax, power, v_point_malicious_anomalies_removed, no_of_malicious_users)

