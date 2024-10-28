import numpy as np

def models_with_detected_anomalies_and_correction(v_point_malicious, sigma_factor):
    v_point_malicious_anomalies_removed = v_point_malicious.copy()
    a, b, c, d = v_point_malicious_anomalies_removed.shape
    v_point_malicious_entries = np.zeros((a, b, c, d))
    
    for i in range(a):
        for j in range(b):
            for j1 in range(c):
                this_data = np.reshape(v_point_malicious_anomalies_removed[i, j, j1, :], (1, d))
                this_data_mean = np.nanmean(this_data)
                this_data_std = np.nanstd(this_data)
                idx = np.where((this_data > (this_data_mean + sigma_factor * this_data_std)) | (this_data < (this_data_mean - sigma_factor * this_data_std)))
                if len(idx[0]) > 0:
                    for k in range(len(idx[0])):
                        v_point_malicious_entries[i, j, j1, idx[0][k]] = 1
                        v_point_malicious_anomalies_removed[i, j, j1, idx[0][k]] = np.nan
    
    v_point_malicious_average_remove_anomaly = np.nanmean(v_point_malicious_anomalies_removed, axis=3)
    
    return v_point_malicious_anomalies_removed, v_point_malicious_average_remove_anomaly