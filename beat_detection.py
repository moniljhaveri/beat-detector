from scipy.io import wavfile 
import math
import numpy as np
from sympy import ifft

# will need to come back paramaterize this 
# this is stored as mono 
sample_rate, data = wavfile.read('CantinaBand60.wav')
max_data = max(data)
normalized_data = [i/max_data for i in data]

class QueueNode: 
    def __init__(self, data) -> None:
        self.data = data
        self.prev = None 
        self.next = None 

class SoundQueue: 
    def __init__(self, max_size_of_queue) -> None:
        self.sum = 0 
        self.max_size_of_queue = max_size_of_queue
        self.head_ptr = QueueNode(0)
        self.tail_ptr = QueueNode(0)

        self.head_ptr.next = self.tail_ptr
        self.tail_ptr.prev = self.head_ptr

        self.tail_ptr.next = None 
        self.head_ptr.prev = None 
    
    def add_to_beginning(self, data): 
        self.sum += data
        node = QueueNode(data)
        tmp__next  = self.head_ptr.next
        node.prev = self.head_ptr
        self.head_ptr.next = node 
        node.next = tmp__next
    
    

class SoundQueueArray: 
    def __init__(self, size_of_arr) -> None:
        pass
    

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

# cooley-tukey algorithm 
def fft(x): 
    N = len(x)
    if N == 1: 
        return x 
    x_even = fft(x[::2])
    x_odd = fft(x[1::2])

    factor = np.exp(-2j*np.pi*np.arange(N)/N)
    X = np.concatenate([x_even + factor[:int(N/2)]*x_odd,x_even + factor[int(N/2):]*x_odd])
    return X
def conjate(x): 
    res = [complex(i.real, -1*i.imag) for i in x if isinstance(i, complex)]
    return res
    

def ifft(samples, inverse_bool = False): 
    N = len(samples)
    inverse_samples = conjate(samples)
    inverse_fft_data = fft(inverse_samples)
    res = conjate(inverse_fft_data)
    return [i/N for i in res]

def compute_es(arr): 
    # need to test 
    c = 32/512 
    ans = [0]*16
    for i in range(16): 
        for j in range(i*32, (i+1)*32): 
            ans[i] +=  arr[j]
        ans[i] *= c
    return ans 

def frequency_selected_sound_energy(x): 
    for i in range(0, len(x)-512, 512): 
        buffer = x[i:(i+512)]
        fft_buffer = fft(buffer)
        fft_power_buffer = [(i.real**2 + i.imag**2)**0.5 for i in fft_buffer]
        es_buffer = compute_es(fft_power_buffer)

frequency_selected_sound_energy(data)
#print(np.allclose(fft(test_data), np.fft.fft(test_data)))
#print(len(np.fft.irfft(fft(test_data))))

test = [1]*512 
print(compute_es(test))

#only three seconds of data
#print(calculate_beat_diff(sample_rate, normalized_data))