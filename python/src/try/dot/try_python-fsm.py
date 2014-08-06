# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 19:20:23 2014

@author: dlmu__000
"""

from fsm import State, Transducer, get_graph

microwave = Transducer('Microwave Oven')

closed_i = State(r'CLOSED\nidle', initial=True)
closed_p = State(r'CLOSED\nprocessing')
opened_i = State(r'OPEN\nidle')
paused = State('PAUSED')
settings = State(r'SETUP')

closed_i[r'PSB, TK /\nset program,\nset timer'] = closed_i
closed_i['SSB / start'] = closed_p
closed_i['ODH / open door'] = opened_i
closed_i['ELS / enter setup'] = settings
settings['SSB / save setup'] = settings
settings['ELS / leave setup'] = closed_i
opened_i['DL / shut door'] = closed_i
closed_p['PRB / pause'] = paused
closed_p['ODH / open door'] = opened_i
closed_p['TO / ready'] = closed_i
paused['SSB / stop'] = closed_i
paused['PRB / resume'] = closed_p
paused[r'PSB, TK /\nreset program,\nreset timer'] = paused
paused['ODH / open door'] = opened_i

get_graph(microwave).draw('microwave.png', prog='dot')