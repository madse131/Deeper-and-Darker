import pygame as pg
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

global title_screen
title_screen = pg.image.load("Deeper-and-Darker/Assets/DaD title screen.png")

global play_button
play_button = pg.image.load("Assets/DaD play sprite.png")
