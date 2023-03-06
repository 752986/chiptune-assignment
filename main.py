import wave
import math
import random


SAMPLE_RATE = 44100 # since the 2A03 doesn't have a specific sample rate, we use the standard 44100Hz. (the gameboy's default is 32773Hz.)
LENGTH = 0.5 # the length in seconds of the file
VOLUME = 0.25 # the overall volume of the file


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


class SquareSampler(Sampler):
	def sample(self, time: float) -> float:
		period = 1 / self.frequency
		return (-1 if time % period > period / 2 else 1) * self.volume


class SineSampler(Sampler):
	def sample(self, time: float) -> float:
		ampiltude = math.sin(time * 2*math.pi * self.frequency) * self.volume # calculate the amplitude of the sample
		ampiltude += (random.random() - 0.5) / 256 # add dithering (slight random noise) to remove an unwanted buzz; you probably don't need to do this
		return ampiltude


class NoiseSampler(Sampler):
	def __init__(self, frequency: float = 261.6, volume: float = 1, mode: bool = False):
		super().__init__(frequency, volume)
		self.bits = 0b1
		self.accum = 0
		self.mode = mode

	def sample(self, time: float) -> float:
		prev_accum = self.accum
		self.accum = time % (1 / (self.frequency * 2))
		if self.accum < prev_accum:
			new_val = (self.bits & 0b1) ^ ((self.bits >> (6 if self.mode else 1)) & 0b1)
			self.bits = (self.bits & ((1 << 14) - 1)) | (new_val << 14)
			self.bits >>= 1
		return -1 if self.bits & 0b1 == 0 else 1


def main():
	sampler = NoiseSampler(000, mode=False)
	sampler2 = SquareSampler(1000)

	with wave.open("out.wav", "wb") as file: # open the file with write access
		file.setframerate(SAMPLE_RATE)
		file.setnchannels(1) # only one channel for simplicity
		file.setsampwidth(1) # the 2A03 only has 4 bits per sample, but the smallest we can do is one byte

		# data = bytes(
		# 	int(
		# 		sampler2.sample(i / SAMPLE_RATE) * 127 * VOLUME + 127
		# 	) for i in range(int(SAMPLE_RATE * LENGTH))
		# ) # process and write the samples
		# file.writeframes(data)
		data = bytes(
			int(
				sampler.sample(i / SAMPLE_RATE) * 127 * VOLUME + 127
			) for i in range(int(SAMPLE_RATE * LENGTH))
		) # process and write the samples
		file.writeframes(data)

if __name__ == "__main__":
	main()