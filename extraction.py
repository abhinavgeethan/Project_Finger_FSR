import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root="P_1"
idx='2'

stim=pd.read_csv(f"data/{root}/stim{idx}.txt",header=None)
time=pd.read_csv(f"data/{root}/timestamp{idx}.txt",header=None)
print("Loaded")
pulse_duration=None
pulse_amp=1.0

good_time=time.iloc[:3000,1]
good_stim=stim.iloc[:3000,1:7]

pulse_starts=[]
pulse_durations=[]
gaps=[]
midpoint_distances=[]
idx=0
while idx<good_time.shape[0]:
    # print(f"Iteration:{idx}")
    curr_stim=good_stim.iloc[idx,:].sum()
    while curr_stim<pulse_amp and idx<good_time.shape[0]-1:
        idx+=1
        curr_stim=good_stim.iloc[idx,:].sum()
        curr_time=good_time[idx]

    pulse_start=curr_time
    pulse_starts.append(pulse_start)
    # print(f"Pulse at: {curr_time}, Stim: {curr_stim}")

    while curr_stim==pulse_amp and idx<good_time.shape[0]-1:
        idx+=1
        curr_stim=good_stim.iloc[idx,:].sum()
        curr_time=good_time[idx]

    pulse_end=curr_time
    pulse_duration=pulse_end-pulse_start
    pulse_durations.append(pulse_duration)

    # print(f"Start: {pulse_start}s | End: {pulse_end}s | Duration: {pulse_duration}s")

    while curr_stim<pulse_amp and idx<good_time.shape[0]-1:
        idx+=1
        curr_stim=good_stim.iloc[idx,:].sum()
        curr_time=good_time[idx]

    next_pulse_start=curr_time
    pulse_starts.append(next_pulse_start)
    gap=next_pulse_start-pulse_end
    gaps.append(gap)
    midpoint=(next_pulse_start+pulse_end)/2.0
    midpoint_dist=midpoint-pulse_end
    midpoint_distances.append(midpoint_dist)
    # print(f"Next Pulse at: {next_pulse_start}s | Midpoint: {midpoint}s")
    # print(f"Time to midpoint from Pulse End: {midpoint-pulse_end}s")
    # print()
    if idx==good_time.shape[0]-1:
        break
avg_pulse_duration=sum(pulse_durations)/len(pulse_durations)
avg_midpoint_distance=sum(midpoint_distances)/len(midpoint_distances)
# avg_midpoint_distance*=0.6
avg_gap=sum(gaps)/len(gaps)
# avg_gap-=0.2*avg_gap

print(f"Avg Duration:{avg_pulse_duration}s | Midpt Dist: {avg_midpoint_distance}s | Gap: {avg_gap}s")

idx=0
curr_stim=good_stim.iloc[idx,:].sum()
while curr_stim<pulse_amp:
    idx+=1
    curr_stim=good_stim.iloc[idx,:].sum()
    curr_time=good_time[idx]

while curr_stim==pulse_amp:
    idx+=1
    curr_stim=good_stim.iloc[idx,:].sum()
    curr_time=good_time[idx]

first_pulse_end=curr_time

print(f"First Pulse End: {first_pulse_end}s")

reversed_stim=good_stim[::-1]
idx=0
time_last_idx=good_time.shape[0]-1
curr_stim=reversed_stim.iloc[idx,:].sum()
while curr_stim<pulse_amp:
    idx+=1
    curr_stim=reversed_stim.iloc[idx,:].sum()
    curr_time=good_time[time_last_idx-idx]

while curr_stim==pulse_amp:
    idx+=1
    curr_stim=reversed_stim.iloc[idx,:].sum()
    curr_time=good_time[time_last_idx-idx]

last_pulse_start=curr_time

print(f"Last Pulse Start: {last_pulse_start}s")

def make_midpoints(first_pulse_end,last_pulse_end,avg_midpoint_distance,avg_gap,avg_pulse_duration):
    curr_start=first_pulse_end
    starts=[]
    starts.append(curr_start)
    midpoints=[]
    while curr_start<last_pulse_start:
        midpoints.append(curr_start+avg_midpoint_distance)
        curr_start+=avg_gap+avg_pulse_duration
        starts.append(curr_start)
    return midpoints,starts

midpoints,starts=make_midpoints(first_pulse_end,last_pulse_start,avg_midpoint_distance,avg_gap,avg_pulse_duration)

print(midpoints)

# def derivate(obj):
#     index = obj.index
#     den = index.to_series().diff()
#     num = obj.diff()
#     return num.div(den, axis=0)
# derivative=derivate(good_stim)
# derivative=derivate(derivative)
# pulse_starts=good_time[np.where(derivative.sum(axis=1)>0)[0]]

# #Taking initial comparison values from first row
# b = pulse_starts.iloc[0]
# #Including first row in result
# filters = [True]
# closeness = 0.013
# #Skipping first row in comparisons
# for val in pulse_starts[1:]:
#     if (1-closeness)*b <= val <= (1+closeness)*b:
#         filters.append(False)
#     else:
#         filters.append(True)
#         # Updating values to compare based on latest accepted val
#         b = val

# pulse_starts = pulse_starts.loc[filters]


# plt.subplot(2,1,1)
plt.plot(good_time, good_stim)
# plt.axvline(first_pulse_end,color='g',linestyle='--')
# plt.axvline(last_pulse_start,color='g',linestyle='--')
# for x in pulse_starts:
#     plt.axvline(x,color='r',linestyle='--')
for x in midpoints:
    plt.axvline(x,color='b',linestyle='--')
for x in starts:
    plt.axvline(x,color='g',linestyle='--')
# plt.subplot(2,1,2)
# plt.plot(good_time, derivative)
plt.show()