import scipy.io.wavfile as wavfile
import time
import os
from numpy.fft import fft
from numpy import *

from copy import copy
from redbot.core import commands
from .kaktusutils import Kaktusutils
from redbot.core.data_manager import cog_data_path

class Morsedecoder(commands.Cog):
    """Morse Decoder cog"""

    @commands.command()
    async def decode(self, ctx):
        """Tries to decode morse from attached audio or video"""
        msg = copy(ctx.message)
        datan = await msg.attachments[0].read()
        tstamp = int(time.time())
        #if not os.path.exists('data/morsedecoder'):
        #    os.mkdir('data/morsedecoder')
        #tmppath = f"{bundled_data_path(self)}/tmp"
        #if not os.path.exists(tmppath):
        #    os.mkdir(tmppath)
        fname = cog_data_path(self) / f"{tstamp}.wav"
        #fname = f"{bundled_data_path(self)}/{}.log".format(tstamp)
        _fp = io.BytesIO()
        await msg.attachments[0].save(_fp)
        with open(fname, 'a', errors='backslashreplace') as f:
            f.write(_fp)
        
        the_file = SoundFile(fname)
        the_filter = SignalFilter()
        the_filter.filter(the_file)
        analyzer = SpectreAnalyzer()
        pulses = analyzer.findpulses(the_file)
        
        pul_translator = PulsesTranslator()
        code_string = pul_translator.tostring(pulses)
        
        str_translator = StringTranslator()
        s = str_translator.totext(code_string)
        
        await ctx.send(code_string)
        await ctx.send(s)
        #await ctx.send(data)
        #files: List[discord.File] = await Kaktusutils.files_from_attach(msg)
        #for f in files:
        #    await ctx.send(f.url)
        #max_size = 8 * 1000 * 1000
        #if msg.attachments and sum(a.size for a in m.attachments) <= max_size:
        #    for a in m.attachments:
        #        _fp = io.BytesIO()
        #        await a.save(_fp)
        #        files.append(discord.File(_fp, filename=a.filename))
class SoundFile:

	def __init__(self, datan):
		#1 - leer el archivo con las muestras
		#	el resultado de read es una tupla, el elemento 1 tiene las muestras
		the_file = wavfile.read(datan)
		self.rate = the_file[0]
		self.length = len(the_file[1])
		self.data = the_file[1]
		# appendea ceros hasta completar una potencia de 2
		power = 10
		while pow(2,power) < self.length:
			power += 1
		self.data = append(self.data, zeros(pow(2,power) - self.length))
	
	def setdata(self, data):
		self.data = data

	def getdata(self):
		return self.data

	def getlength(self):
		return self.length

	def saveas(self, path):
		wavfile.write(path, self.rate, self.data)

	def saveplot(self, fileName):
		plotter.saveplot(fileName,self.data,length=self.length)

class PulsesTranslator:
	def tostring(self, pulses):
		pa = PulsesAnalyzer()
		comp_vec = pa.compress(pulses)
		comp_tup = pa.split(comp_vec)
		
		onessl = pa.findshortlong(comp_tup[0])
		# zeros are subdivided
		dup = pa.findshortlongdup(comp_tup[1])
		zerossl = pa.createshortlong(dup[0], dup[1])
		dup2 = pa.findshortlongdup(dup[1])
		zeroextra = pa.createshortlong(dup2[0], dup2[1])
		
		symdec = SymbolDecoder(onessl, zerossl, zeroextra)
		
		s = ""
		for i in range(len(comp_vec)//2):
			s += symdec.getonesymbol(comp_vec[2*i])
			s += symdec.getzerosymbol(comp_vec[2*i+1])
		s += symdec.getonesymbol(comp_vec[-1])
		return s

class PulsesAnalyzer:
	
	def compress(self, pulses):
		vec = []
		i = 0
		
		if pulses[0] == 1:
			vec += [0]
			i = 1
		
		last = pulses[0]
		
		while i < len(pulses):
			c = 0
			last = pulses[i]
			while i < len(pulses) and pulses[i] == last:
				i += 1
				c += 1
			vec += [c]
			i += 1
		
		vec = vec[1:-1]
		return vec

	def split(self, vec):
		onesl = zeros(1+len(vec)//2)
		zerosl = zeros(len(vec)//2)
		for i in range(len(vec)//2):
			onesl[i] = vec[2*i]
			zerosl[i] = vec[2*i+1]
		onesl[-1] = vec[-1]
		return (onesl, zerosl)

	def findshortlongdup(self, vec):
		sor = sort(vec)
		last = sor[0]
		for i in range(len(sor))[1:]:
			if sor[i] > 2*last:
				shorts = sor[:i-1]
				longs = sor[i:]
				return (shorts, longs)
		return (vec, [])

	def createshortlong(self, shorts, longs):
		return ShortLong(shorts, longs)

	def findshortlong(self, vec):
		dup = self.findshortlongdup(vec)
		return self.createshortlong(dup[0], dup[1])

class SpectreAnalyzer:

	def spectrogram(self, signal):
		#spectrogram = specgram(signal)
		#savefig("spectrogram", format="pdf")
		#cla()
		spectrogram = plotter.specgram("spectrogram", signal)
		return spectrogram

	def sumarizecolumns(self, mat):
		vec_ones = ones(len(mat))
		vec_sum = (matrix(vec_ones) * matrix(mat)).transpose()
		plotter.saveplot("frecuency_volume",vec_sum)
		return vec_sum

	def findpresence(self, vec_sum):
		presence = zeros(len(vec_sum))
		threshold = max(vec_sum) / 2.0
		for i in range(len(presence)):
			if vec_sum[i] > threshold:
				presence[i] = 1
		plotter.saveplot("presence", presence, dpi=300, height=5)
		return presence

	def findpulses(self, soundfile):
		spec = self.spectrogram(soundfile.getdata())
		# spec[0] es la matriz del rojo
		red_matrix = spec[0]
		vec_sum = self.sumarizecolumns(red_matrix)
		presence = self.findpresence(vec_sum)
		return presence

class SignalFilter:

	def filter(self, soundfile):
		#2 - aplico transformada de fourier
		trans = fft.rfft(soundfile.getdata())
		trans_real = abs(trans)
		#2b - lo grafico
		plotter.saveplot("transformed",trans_real)
		#3 - busco la frecuencia
		band = 2000
		# ignore the first 200Hz
		hzignored = 200
		frec = hzignored + argmax(trans_real[hzignored:])
		#print max(trans_real)
		#print trans_real[frec]
		#print frec
		min = (frec - band / 2) if (frec > band / 2) else 0
		filter_array = append(zeros(min), ones(band))
		filter_array = append(filter_array, zeros(len(trans_real) - len(filter_array)))
		filtered_array = multiply(trans, filter_array)
		plotter.saveplot("filtered_trans",abs(filtered_array))
		#4 - antitransformo
		filtered_signal = array(fft.irfft(filtered_array)[:soundfile.getlength()], dtype="int16")
		plotter.saveplot("filtered_signal",filtered_signal)
		soundfile.setdata(filtered_signal)