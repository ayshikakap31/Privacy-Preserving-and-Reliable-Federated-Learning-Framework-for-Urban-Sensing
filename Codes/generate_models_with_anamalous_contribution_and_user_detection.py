import numpy as np

def detect_anomalous_contribution_and_user(participant_position_measurement_malicious,no_of_models, no_of_participants_each_model, timestamp_max,length, width, Xi, Yi, dmax, power, v_point_malicious_anomalies_removed, no_of_malicious_users):
    each_user_each_contribution_anomaly_score = np.zeros((no_of_models, no_of_participants_each_model, timestamp_max)) + np.nan
    for time_instance in range(1, timestamp_max+1):
        for i1 in range(1, no_of_models+1):
            for i2 in range(1, no_of_participants_each_model+1):
                Xc = participant_position_measurement_malicious[i1-1, i2-1, time_instance-1, 0]
                Yc = participant_position_measurement_malicious[i1-1, i2-1, time_instance-1, 1]
                Vc = participant_position_measurement_malicious[i1-1, i2-1, time_instance-1, 2]
                xc_this = Xc
                yc_this = Yc
                vc_this = Vc
                if not np.isnan(vc_this):
                    Wi_this_model = np.zeros((length, width))
                    weighted_sum = np.zeros((length, width))
                    D = np.sqrt((Xi-xc_this)**2 + (Yi-yc_this)**2)
                    D = D.reshape(length, width)
                    idx_1, idx_2 = np.where(D < dmax)
                    for k in range(len(idx_1)):
                        weighted_sum[idx_1[k], idx_2[k]] = vc_this * (D[idx_1[k], idx_2[k]]**power)
                        Wi_this_model[idx_1[k], idx_2[k]] = D[idx_1[k], idx_2[k]]**power
                    this_model = weighted_sum / Wi_this_model
                    this_model[np.isnan(this_model)] = 0
                    each_user_each_contribution_anomaly_score[i1-1, i2-1, time_instance-1] = np.nanmean(np.nanmean(np.abs(this_model * (this_model - v_point_malicious_anomalies_removed[:,:,time_instance-1,1]))))
                    
    each_user_anomaly_score = np.nanmean(each_user_each_contribution_anomaly_score, axis=2)
    top_anomalous_users = np.zeros((no_of_models, no_of_malicious_users))
    top_anomalous_user_score = np.zeros((no_of_models, no_of_malicious_users))
    for i in range(no_of_models):
        idx = np.argsort(each_user_anomaly_score[i, :])[::-1]
        top_anomalous_user_score[i, :] = each_user_anomaly_score[i, idx][:no_of_malicious_users]
        top_anomalous_users[i, :] = idx[:no_of_malicious_users]
    return top_anomalous_users, top_anomalous_user_score