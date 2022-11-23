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
def calculate_instaneous_sound_energy(sound_data): 
    acc = 0 
    for i in range(0, 512): 
        acc += sound_data[i]**2 
    return acc 

def calculate_beat_diff(sample_rate, sound_data): 

    # calculate deque max len 
    max_len = math.floor(sample_rate/512)

    circular_buffer = collections.deque(maxlen=max_len)
    coeffient_of_sensibility = 1.3 
    beat_count = 0 
    beat = []
    local_average_sound_energy = 0
    #initialize buffer 
    for i in range(0, max_len): 
        circular_buffer.append(sound_data[i]**2)

    #TODO Need to redo this code to correctly calcute the diff
    for i in range(0, len(sound_data) - 512, 512): 
        local_average_sound_energy = calculate_average_sound_energy(sample_rate, circular_buffer)
        instaneous_energy = calculate_instaneous_sound_energy(circular_buffer)
        print(local_average_sound_energy, instaneous_energy)
        if instaneous_energy > coeffient_of_sensibility*local_average_sound_energy:
            beat_count += 1
            beat.append(instaneous_energy)
        for j in range(512): 
            circular_buffer.popleft
            circular_buffer.append(sound_data[i + j])
        print(i)
    final_buffer = list(circular_buffer)
    #for i in range(0, len(circular_buffer), 512): 
    #    instaneous_energy = calculate_instaneous_sound_energy(final_buffer[i:])
    #    if instaneous_energy > coeffient_of_sensibility*local_average_sound_energy:
    #        beat_count += 1
    #        beat.append(instaneous_energy)
    return beat_count
    
    


        
#only three seconds of data
#print(calculate_beat_diff(sample_rate, normalized_data))
print(sample_rate)