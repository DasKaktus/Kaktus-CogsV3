import time
import os
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import wave
import math
import io

from copy import copy
from redbot.core import commands
from .kaktusutils import Kaktusutils
from redbot.core.data_manager import cog_data_path
from scipy.io import wavfile
from tkinter import *

morse_code = ["*-", "-***", "-*-*", "-**", "*", "**-*", "--*", "****", "**", "*---", "-*-", "*-**", "--", "-*", "---", "*--*", "--*-", "*-*", "***", "-", "**-", "***-", "*--", "-**-", "-*--", "--**", "*----", "**---", "***--", "****-", "*****", "-****", "--***", "---**", "----*", "-----", "|"]
alphabetEN = ['a',    'b',    'c',   'd',  'e',   'f',   'g',    'h',   'i',   'j',   'k',    'l',   'm',  'n',  'o',    'p',    'q',   'r',   's',  't',  'u',   'v',    'w',    'x',    'y',    'z',    '1',     '2',     '3',     '4',      '5',     '6',     '7',    '8',     '9',     '0',   ' ']
alphabetEN_length = len(alphabetEN) - 1

class Morsedecoder(commands.Cog):
    """Morse Decoder cog"""

    @commands.command()
    async def decode(self, ctx):
        """Tries to decode morse from attached audio or video"""
        msg = copy(ctx.message)
        _fp = io.BytesIO()
        await msg.attachments[0].save(_fp)
        datan = await msg.attachments[0].read()
        tstamp = int(time.time())
        path: pathlib.Path = cog_data_path(self)
        wav_path = path / (str(tstamp) + ".wav")
        
        global dot_or_dash
        dot_or_dash = []
        global spaces
        spaces = []
        global spaces_length
        spaces_length = []
        global letter_spacing    
        waveform = np.array([])

        
        with wav_path.open("wb") as file:
            file.write(datan)
       
        await ctx.send("Decoding, please wait...")
        
#    try:
        with wave.open(str(wav_path),'r') as wav_file:

            num_channels = wav_file.getnchannels()
            frame_rate = wav_file.getframerate()
            downsample = math.ceil(frame_rate * num_channels / 1000)

            process_chunk_size = 600000 - (600000 % frame_rate)
            signal = None

            while signal is None or signal.size > 0:
                signal = np.frombuffer(wav_file.readframes(process_chunk_size), dtype='int16')

                sub_waveform = np.nanmean(
                    np.pad(np.absolute(signal), (0, ((downsample - (signal.size % downsample)) % downsample)), mode='constant', constant_values=np.NaN).reshape(-1, downsample),
                    axis=1
                )

                waveform = np.concatenate((waveform, sub_waveform))

            for i in waveform:
                if i <= 300:
                    spaces_length.append(len(spaces))
                    spaces = []
                else:
                    spaces.append("No")

            letter_spacing = int((max(spaces_length) + sum(spaces_length)/len(spaces_length))/3)
            encoded_list = []
            for i in waveform:
                if i <= 500:
                    dot_or_dash.append("Yes")
                    if len(spaces) >= letter_spacing:
                        encoded_list.append("|")
                    else:
                        pass
                    spaces = []
                else:
                    spaces.append("No")
                    if 2 < len(dot_or_dash) <= 10:
                        encoded_list.append("*")
                    elif len(dot_or_dash) > 10:
                        encoded_list.append("-")
                    else:
                        pass
                    dot_or_dash = []

            encoded_list.append("|")
            encoded_word = ''.join(encoded_list)

            await ctx.send("```" + encoded_word[0:50] + "```")

            encrypted = []
            encoded_list = encoded_word.split("|")
            encoded_list_length = len(encoded_list)
            ''' Here we have SOS priority'''
            if (encoded_word == "***---***"):
                print("sos")
            else:
                for j in range(encoded_list_length):
                   if encoded_list[j] in morse_code:
                       try:
                          encrypted.append(alphabetEN[morse_code.index(encoded_list[j])])
                       except:
                           pass
                   else:
                       pass
                encrypted = ''.join(encrypted)

                await ctx.send(encrypted)

#    except:
#       await ctx.send("Error..........")