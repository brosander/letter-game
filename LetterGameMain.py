#!/usr/bin/env python

from os import listdir, mkdir, path
from os.path import isfile, isdir, join

import pygame
import random
import requests
import sys
import urllib

class LetterGameMain:
  def __init__(self, asset_dir, tts_prefix, render_full = True, width=1024, height=768):
    pygame.init()
    pygame.mixer.init()
    self.width = width
    self.height = height
    self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
    self.asset_dir = asset_dir
    self.tts_prefix = tts_prefix
    self.font = pygame.font.SysFont("monospace", 48)
    self.render_full = render_full
    self.assets = self._build_assets()

  def _get_tts(self, text, output_file):
    r = requests.get(self.tts_prefix + urllib.quote_plus(text), stream = True)
    with open(output_file, 'wb') as f:
      for chunk in r.iter_content(chunk_size = 1024):
        if chunk:
          f.write(chunk)

  def _build_assets(self):
    assets = {}
    for f in listdir(self.asset_dir):
      if f.endswith('.png') or f.endswith('.jpg'):
        p = join(self.asset_dir, f)
        if isfile(p):
          letter = f[0].upper()
          if letter not in assets:
            assets[letter] = []
          original_image = pygame.image.load(p).convert()
          new_width = int(float(original_image.get_width()) / original_image.get_height() * self.height)
          image = pygame.Surface((self.width, self.height))
          image.fill((0, 0, 0))
          image.blit(pygame.transform.smoothscale(original_image, (new_width, self.height)), ((self.width - new_width) / 2, 0))
          text_name = f[:-4]
          text = letter + ' is for ' + text_name
          tts = join(self.asset_dir, text_name + '.mp3')
          if not isfile(tts):
            print('Getting tts for ' + text)
            self._get_tts(text, tts)
          if self.render_full:
            orig_text_label = self.font.render(text, 1, (255, 255, 0))
          else:
            orig_text_label = self.font.render(text[0], 1, (255, 255, 0))
          new_text_height = int(self.height * 0.15)
          new_text_width  = int((float(orig_text_label.get_width()) / orig_text_label.get_height()) * new_text_height)
          text_label = pygame.transform.smoothscale(orig_text_label, (new_text_width, new_text_height))
          image.fill((0, 0, 0), pygame.Rect((0, self.height - text_label.get_height()), (self.width, text_label.get_height() + 5)))
          image.blit(text_label, ((self.width - text_label.get_width())/2, self.height - text_label.get_height()))
          assets[letter].append((text, image, tts))
    return assets

  def main_loop(self):
    letter_indices = {}
    while 1:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return
        elif event.type == pygame.KEYDOWN and event.key >= 0 and event.key < 256:
          if event.key == pygame.K_ESCAPE:
            return
          letter = str(chr(event.key)).upper()
          if letter in self.assets:
            if letter not in letter_indices:
              letter_indices[letter] = 0
            letter_index = letter_indices[letter]
            options = self.assets[letter]
            option = options[letter_index]
            letter_indices[letter] = (letter_index + 1) % len(options)
            image = option[1]
            self.screen.fill((0, 0, 0))
            self.screen.blit(image, ((self.width - image.get_width()) / 2, 0))
            pygame.display.flip()
            pygame.mixer.music.load(option[2])
            pygame.mixer.music.play()

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser(description = 'A simple game to help small children learn their ABCs',
    formatter_class=lambda prog: argparse.ArgumentDefaultsHelpFormatter(prog, width=120))
  parser.add_argument("-p", "--pictureDirectory", help="Directory of images to use", default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'default'))
  parser.add_argument("-t", "--ttsUrlPrefix", help="Url prefix to append tts query to", default='https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=En-us&q=')
  args = parser.parse_args()

  main = LetterGameMain(args.pictureDirectory, args.ttsUrlPrefix, False)
  main.main_loop()
  pygame.quit()