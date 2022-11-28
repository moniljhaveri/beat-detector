from scipy.io import wavfile 
import collections
import itertools
import math

# will need to come back paramaterize this 
# this is stored as mono 
sample_rate, data = wavfile.read('CantinaBand60.wav')
max_data = max(data)
normalized_data = [i/max_data for i in data]

# this is multiplied 
def calculate_average_sound_energy(sample_rate, sound_data): 
    coefficient = 512/sample_rate 
    sound_energy = sum(sound_data)
    average_sound_energy = coefficient * sound_energy
    return average_sound_energy

# currently only works for mono wav files
# TODO make it work for both mono and stereo audio 
def calculate_instaneous_sound_energies(max_len, sound_data): 
    ans = []
    for i in range(0, max_len, 512): 
        acc = 0 
        for j in range(i, i + 512): 
            acc += sound_data[j]
        ans.append(acc)
    return ans 

def calculate_variance(buffer, mean): 
    deviations = [(x - mean)**2 for x in buffer]
    variance = sum(deviations)/len(buffer)
    return variance

def calculate_coefficient_of_sensibility(variance): 
    return -0.0025714*variance + 1.5142857

def calculate_beat_diff(sample_rate, sound_data): 
    max_len = math.floor(sample_rate/512) * 512
    sound_data_len = math.floor(len(sound_data)/max_len) * max_len
    beat_count = 0 
    beat = []

    for i in range(0, sound_data_len, max_len): 
        buffer = [0] * max_len
        variance_buffer = [0] * max_len
        for j in range(i, i + max_len): 
            buffer[j - i] = sound_data[j]**2
            variance_buffer[j - i] = sound_data[j]
        average_energy = calculate_average_sound_energy(max_len, buffer)
        instaneous_sound_energy = calculate_instaneous_sound_energies(max_len, buffer)
        variance = calculate_variance(variance_buffer, average_energy)
        print(variance)
        coeffient_of_sensibility = calculate_coefficient_of_sensibility(variance)
        for ise in instaneous_sound_energy: 
            if ise > (average_energy * coeffient_of_sensibility): 
                beat_count += 1
                beat.append(ise)
    return beat_count

#only three seconds of data
print(calculate_beat_diff(sample_rate, normalized_data))