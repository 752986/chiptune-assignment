import wave
import math


SAMPLE_RATE = 44100 # since the 2A03 doesn't have a specific sample rate, we use the standard 44100Hz
LENGTH = 1.0 # the length in seconds of the file
VOLUME = 0.25 # the overall volume factor of the file


class Sampler:
	# this is a class so that you can carry state between samples
	def __init__(self, frequency: float = 261.6, volume: float = 1):
		'''`frequency` is the volume in Hz, and `volume` is a factor from `0` to `1`.'''
		self.frequency = frequency
		self.volume = volume

	def sample(self, time: float) -> float:
		'''`time` is the time in seconds since the beginning of the note. Outputs a number from -1 to 1 coresponding to the amplitude at that point.'''
		# note that this function should take into account the frequency and volume!

		return 0


class SineSampler(Sampler):
	def sample(self, time: float) -> float:
		ampiltude = math.sin(time * 2*math.pi * self.frequency) * self.volume # calculate the amplitude of the sample
		return ampiltude


# write your own `Sampler` class here!


def main():
	sampler = SineSampler(261.6) # change this line to use your own sampler!

	# you shoudn't need to touch anything below here
	data = bytes(
			int(
				sampler.sample(i / SAMPLE_RATE) * 127 * VOLUME + 127
			) for i in range(int(SAMPLE_RATE * LENGTH))
		) # process and write the samples

	with wave.open("out.wav", "wb") as file: # open the file with write access
		file.setframerate(SAMPLE_RATE)
		file.setnchannels(1) # only one channel for simplicity
		file.setsampwidth(1) # the 2A03 only has 4 bits per sample, but the smallest we can do is one byte

		file.writeframes(data)

if __name__ == "__main__":
	main()