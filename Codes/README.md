# An end-to-end privacy preserving framework for user privacy, model reliability, and fair incentivization for federated learning based urban sensing system

This work validates the proposed framework for urban parameter modeling, leveraging synthetic data generated with the NoiseModelling GIS Tool. The tool incorporates building, land use, transportation network, and traffic information to produce environmental noise models. In this simulation, a 1km × 1.5km region in Lorient, north-western France, is chosen, utilizing the EPSG:2154 spatial reference system. Dynamic noise measurements are simulated over ten days, resulting in 30 parameter models. The project focuses on creating high granularity parameter models by interpolating measurements at probe stations using the IDW spatial interpolation technique.

The work uses the dataset file 'parameter_data.npz'. 

# Installation
This project requires Python3 (https://www.python.org/downloads/) to be installed on the machine.

# Prerequisites
Before running the code, make sure you have the following libraries installed:
  1) NumPy (https://numpy.org/)
  2) SciPy (https://www.scipy.org/)

# Main Files

1) 'parameter_data.npz': Contains the essential Numpy data with physical parameter information corresponding to specific latitudinal and longitudinal coordinates.
2) 'Main.py': Main file which contain code for implementation of the proposed framework on simulated data.
3) 'inverse_distance_weighting.py': This Python script executes geographically weighted inverse distance weighting, a crucial process in our modeling framework, enabling accurate spatial interpolation.
4) 'generate_simulated_sensing_data.py': The Python script responsible for generating simulated sensing data for participant positions, contributing to the realistic simulation of models.
5) 'non_malicious_model_update.py': Implements a non-malicious m-hop with m=3 application update model to generate physical parameter models from user data, emphasizing collaborative and non-malicious user contributions.
6) 'generate_malicious_contributions.py': Simulates the generation of malicious contributions from participants, enabling the study of the framework's robustness against intentional distortions.
7) 'generate_models_with_malicious_contributions_from_users.py': Simulates the generation of physical parameter models without correcting intentional malicious contributions from participants, employing the m-hop with m=3 application update model.
8) 'generate_models_with_statistics_based_anomaly_detection.py': Implements statistics-driven anomaly detection and correction for generating aggregated physical parameter models at the application server, enhancing the overall accuracy of the models.
9) 'generate_models_with_anamalous_contribution_and_user_detection.py': Implements detection of anomalous contributions and anomalous user detection at the user device, contributing to the framework's ability to identify and handle unexpected behaviors.
