import numpy as np

def models_with_malicious_contributions(participant_position_measurement_malicious,length, width, timestamp_max, no_of_models,latitude,longitude,m_hop, dmax, power):
    v_point_malicious = np.zeros((length, width, timestamp_max, no_of_models))
    for i in range(no_of_models):
        for time_instance in range(timestamp_max):
            Xc = participant_position_measurement_malicious[i, :, time_instance, 0]
            Yc = participant_position_measurement_malicious[i, :, time_instance, 1]
            Vc = participant_position_measurement_malicious[i, :, time_instance, 2]
            Xi = latitude.reshape(1, -1)
            Yi = longitude.reshape(1, -1)
            rand_perm = np.random.permutation(len(Xc))
            Xc = Xc[rand_perm]
            Yc = Yc[rand_perm]
            Vc = Vc[rand_perm]
            m_partitions = np.zeros((len(Xc) // m_hop, 2))
            m_partitions[:, 0] = np.arange(0, len(Xc), m_hop)[:len(Xc) // m_hop]
            m_partitions[:, 1] = np.arange(m_hop, len(Xc), m_hop)[:len(Xc) // m_hop]
            m_partitions[-1, 1] = len(Xc)
            m_partitions_num, _ = m_partitions.shape
            Vi = np.zeros((length, width))
            Wi = np.zeros((length, width))
            for j in range(m_partitions_num):
                for k1 in range(int(m_partitions[j, 0]), int(m_partitions[j, 1])):
                    weighted_sum = Vi * Wi
                    weighted_sum[np.isnan(weighted_sum)] = 0
                    D = np.sqrt((Xi - Xc[k1]) ** 2 + (Yi - Yc[k1]) ** 2)
                    D = D.reshape(length, width)
                    idx_1, idx_2 = np.where(D < dmax)
                    for k in range(len(idx_1)):
                        weighted_sum[idx_1[k], idx_2[k]] += Vc[k1] * (D[idx_1[k], idx_2[k]] ** power)
                        Wi[idx_1[k], idx_2[k]] += D[idx_1[k], idx_2[k]] ** power
                    Vi = weighted_sum / Wi
            v_point_malicious[:, :, time_instance, i] = Vi
    
    v_point_malicious_average = np.nanmean(v_point_malicious, axis=3)
    
    return v_point_malicious_average, v_point_malicious, Xi, Yi