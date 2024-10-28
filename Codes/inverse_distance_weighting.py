import numpy as np

def inverse_distance_weighting(Xc, Yc, Vc, Xi, Yi, w, r1, r2):
    if len(Xc) != len(Yc) or len(Xc) != len(Vc):
        raise ValueError('Vectors Xc, Yc, and Vc are incorrectly sized!')
    elif len(Xi) != len(Yi):
        raise ValueError('Vectors Xi and Yi are incorrectly sized!')
    elif len(Xi) < 6:
        raise ValueError('Uncorrect number of inputs!')
    
    if len(Xi) != 8:
        if len(Xi) < 7:
            r1 = 'n'
            r2 = len(Xc)
        elif len(Xi) == 7 and r1 == 'n':
            r2 = len(Xc)
        elif len(Xi) == 7 and r1 == 'r':
            X1, X2 = np.meshgrid(Xc)
            Y1, Y2 = np.meshgrid(Yc)
            D1 = np.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)
            r2 = np.max(D1)
            X1, X2, Y1, Y2, D1 = None, None, None, None, None
    else:
        if r1 not in ['r', 'n']:
            raise ValueError('Parameter r1 ("' + r1 + '") not properly defined!')
    
    Vi = np.zeros((len(Xi), len(Xi[0])))
    D = []
    Vcc = []
    
    if r1 == 'r':
        if r2 <= 0:
            raise ValueError('Radius must be positive!')
        for i in range(len(Xi)):
            D = np.sqrt((Xi[i] - Xc)**2 + (Yi[i] - Yc)**2)
            Vcc = Vc[D < r2]
            D = D[D < r2]
            if len(D) == 0:
                Vi[i] = np.nan
            else:
                if np.sum(D == 0) > 0:
                    Vi[i] = Vcc[D == 0]
                else:
                    Vi[i] = np.sum(Vcc * (D**w)) / np.sum(D**w)
    elif r1 == 'n':
        if r2 > len(Vc) or r2 < 1:
            raise ValueError('Number of neighbours not congruent with data')
        for i in range(len(Xi)):
            D = np.sqrt((Xi[i] - Xc)**2 + (Yi[i] - Yc)**2)
            I = np.argsort(D)
            D = D[I]
            Vcc = Vc[I]
            if D[0] == 0:
                Vi[i] = Vcc[0]
            else:
                Vi[i] = np.sum(Vcc[:r2] * (D[:r2]**w)) / np.sum(D[:r2]**w)
    
    return Vi

