# Importation of liberies.
from matplotlib.pyplot import show, subplots
from numpy import append, argmax, linspace, median, where
from pandas import DataFrame
from scipy.interpolate import pchip_interpolate
from scipy.signal import correlate, correlation_lags

# Functions.
# _______________________________________________________________________________


def Plot_Data(data, test, phase):
    """
    This fuction plot the Roll, Pitch and Yaw data.
    """
    fig, ((ax1, axa), (ax2, axb), (ax3, axc)
          ) = subplots(3, 2, figsize=(9.6, 5.5))
    for i in data:
        s = data[i]
        ax1.plot(s['TimeStamp'], s['Roll'], label=i)
        ax2.plot(s['TimeStamp'], s['Pitch'], label=i)
        ax3.plot(s['TimeStamp'], s['Yaw'], label=i)
        axa.plot(s['TimeStamp'], s['xGyr'], label=i)
        axb.plot(s['TimeStamp'], s['yGyr'], label=i)
        axc.plot(s['TimeStamp'], s['zGyr'], label=i)
    fig.suptitle(phase+' '+test)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Roll (°)')
    ax1.set_title('Roll')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Pitch (°)')
    ax2.set_title('Pitch')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Yaw (°)')
    ax3.set_title('Yaw')
    axa.set_xlabel('Time (s)')
    axa.set_ylabel('xGyr (°/s)')
    axa.set_title('xGyr')
    axb.set_xlabel('Time (s)')
    axb.set_ylabel('yGyr (°/s)')
    axb.set_title('yGyr')
    axc.set_xlabel('Time (s)')
    axc.set_ylabel('zGyr (°/s)')
    axc.set_title('zGyr')
    ax1.margins(0, 0.1)
    ax2.margins(0, 0.1)
    ax3.margins(0, 0.1)
    axa.margins(0, 0.1)
    axb.margins(0, 0.1)
    axc.margins(0, 0.1)
    fig.tight_layout()
    show()
    return None
# _______________________________________________________________________________


def Set_Data(data):
    """
    This fuction set the sensors to start in 0.
    """
    for i in data:
        s = data[i]
        s = s.iloc[50:data[i].size-29, :]  # errase first 50 takes and last 29
        time = s["TimeStamp"]
        time = time-time.iloc[0]
        s['TimeStamp'] = time
        data[i] = s
    return data
# _______________________________________________________________________________


def Change_Range(data, thresh=89):
    """
    This fuction fix the angles lokking for the abrupt changes.
    """
    for s in data:
        n_d = data[s].loc[:, ]
        for d in ['Roll', 'Pitch', 'Yaw']:
            var = n_d = data[s].loc[:, d]
            drv = where(((abs(var.diff())) >= thresh))
            drv = drv[0].tolist()
            if (len(drv) % 2) != 0:
                drv.append(len(n_d)-1)
            for f in range(0, len(drv), 2):
                chg = var.iloc[drv[f]-1]+var.iloc[drv[f]]
                var.iloc[drv[f]:drv[(f)+1]] = - \
                    (var.iloc[drv[f]:drv[(f)+1]])+chg
            data[s].loc[:, d] = var
    return data
# _______________________________________________________________________________


def Resample(data, f):
    """
    This fuction resample the data to a frecuency passed by the user.
    """
    for i in data:
        s = data[i]
        n_t = s.loc[:, 'TimeStamp']
        n_t = n_t-n_t.iloc[0]
        n_t = linspace(0, n_t.iloc[-1], round(n_t.iloc[-1]*f))
        r = s['Roll']
        p = s['Pitch']
        h = s['Yaw']
        x = s['xGyr']
        y = s['yGyr']
        z = s['zGyr']
        r = pchip_interpolate(s['TimeStamp'], r, n_t)
        p = pchip_interpolate(s['TimeStamp'], p, n_t)
        h = pchip_interpolate(s['TimeStamp'], h, n_t)
        x = pchip_interpolate(s['TimeStamp'], x, n_t)
        y = pchip_interpolate(s['TimeStamp'], y, n_t)
        z = pchip_interpolate(s['TimeStamp'], z, n_t)
        s = DataFrame({'TimeStamp': n_t, 'Roll': r, 'Pitch': p, 'Yaw': h, 'xGyr': x,
                       'yGyr': y, 'zGyr': z})
        data[i] = s
    return data
# _______________________________________________________________________________


def Syncronize(data):
    """
    This function synchronizes the sensors and returns the synchronized data 
    using cross correlation lag.
    """
    lag = {}
    n = list(data.keys())
    l = len(data[n[0]])
    ref = n[0]
    for i in range(1, len(n)):
        if len(data[n[i]]) < l:
            l = len(data[n[i]])
            ref = n[i]
    n.remove(ref)
    data_a = data[ref].loc[:, ['xGyr', 'yGyr', 'zGyr']]
    lag = [0]
    for s in n:
        data_b = data[s].loc[:, ['xGyr', 'yGyr', 'zGyr']]
        corr = correlate(data_b, data_a, mode='same')
        lags = correlation_lags(len(data_a), len(data_b), mode='same')
        corr_max = argmax(corr, axis=0)
        lag = append(lag, median([lags[corr_max[0]], lags[corr_max[1]],
                                  lags[corr_max[2]]]))
    n = append(ref, n)
    if 0 > min(lag):
        lag += abs(min(lag))
    for s in range(0, len(n)):
        data[n[s]] = data[n[s]].iloc[int(lag[s]):, :]
        time = data[n[s]]['TimeStamp']
        time = time-time.iloc[0]
        data[n[s]]['TimeStamp'] = time
    return data
# _______________________________________________________________________________


def Same_size(data):
    """
    This function makes all the dataframes have the same size.
    """
    n = list(data.keys())
    l = len(data[n[0]])
    for i in range(1, len(n)):
        if len(data[n[i]]) < l:
            l = len(data[n[i]])
    for s in n:
        data[s] = data[s].iloc[0:l, :]
    return data
