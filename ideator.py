#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ideator.py
# (c) 2020 Mal Minhas, <mal@malm.co.uk>
#
# Description
# -----------
# CLI for generating ideas using GPT3.
# Simply enter the domain you are interested in at the prompt.
# See here for more on the GPT-3 beta API: https://beta.openai.com/docs/introduction
# Completions are appended to output.txt file.
#
# History
# -------
# 14.11.20   v0.1    First version
# 25.11.21   v0.2    Updated to add output.txt support
#

import os
import sys
import time
import arrow
import openai
import docopt

PROGRAM         = __file__
VERSION         = '0.2'
AUTHOR          = 'Mal Minhas'
DATE            = '25.11.21'
DEFAULT_LENGTH  = 64

openai.api_key = os.environ["OPENAI_API_KEY"]

def getCompletion(input_text, output_length):
    response = openai.Completion.create(
        engine="davinci",
        prompt=input_text,
        temperature=0.7,
        max_tokens=output_length,
        top_p=1
    )
    return response.get('choices')[0].get('text')

def procArguments(arguments):
    text = arguments.get('<domain>')
    try:
        length = int(arguments.get('<length>'))
    except:
        length = DEFAULT_LENGTH
    return text, length

if __name__ == '__main__':
    import docopt
    loc = sys.stdout.encoding
    usage="""
    {}
    --------------------------
    Usage:
    {} <domain> [<length>]
    {} -h | --help
    {} -V | --version

    Options:
    -h --help               Show this screen.
    -v --verbose            Verbose mode.
    -V --version            Show version.
 
    Examples:
    1. Generate 256 words of output for ideas on fashion and the future of the clothing industry
    {} "fashion and the future of the clothing industry" 256

    Locale: {}
    """.format(*tuple([PROGRAM] * 5),loc)

    arguments = docopt.docopt(usage)
    #print(arguments)
    t0 = time.time()
    if arguments.get('--version') or arguments.get('-V'):
        print(f'{PROGRAM} version {VERSION} {AUTHOR} {DATE}')
    elif arguments.get('--help') or arguments.get('-h'):
        print(usage)
    else:
        input_text, output_len = procArguments(arguments)
        if input_text:
            t0 = time.time()
            prompt = f"Ideas involving {input_text}"
            print(prompt)
            print('-' * len(prompt))
            response = getCompletion(prompt, output_len)
            with open('output.txt','a') as f:
                dtime = arrow.utcnow().format()
                f.write(f'========= {dtime} {prompt} ==========\n')
                f.write(response)
                f.write("\n\n")
            print(response)
            t1 = time.time()
            # print(f'Finished in {round(t1-t0,2)} seconds')
        else:
            print(usage)
