#!/usr/bin/env python2

import unittest
from parser import Parser
from scene import *

class TestParser(unittest.TestCase):

  def parse(self, input, print_nodes=False):
    parser = Parser(input)
    if(print_nodes): parser.print_nodes()
    return parser.scene

  def test_sum_vs_product_assoc(self):
    scene = self.parse('$ = box : s 1 + 1 * 1')
    expr = scene.find_rule('$')[0].param
    self.assertIsInstance(expr, Plus)
    self.assertIsInstance(expr[0], Number)
    self.assertIsInstance(expr[1], Times)
    self.assertIsInstance(expr[1][0], Number)
    self.assertIsInstance(expr[1][1], Number)

  def test_transform_vs_and_assoc(self):
    scene = self.parse('$ = box & box : s 1')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], And)
    self.assertIsInstance(rule[0][0], Box)
    self.assertIsInstance(rule[0][1], Transform)
    self.assertIsInstance(rule[0][1][0], Box)

  def test_or_left_assoc(self):
    scene = self.parse('$ = box | box | box')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], Or)
    self.assertIsInstance(rule[0][0], Or)
    self.assertIsInstance(rule[0][0][0], Box)
    self.assertIsInstance(rule[0][0][1], Box)
    self.assertIsInstance(rule[0][1], Box)

  def test_and_left_assoc(self):
    scene = self.parse('$ = box & box & box')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], And)
    self.assertIsInstance(rule[0][0], And)
    self.assertIsInstance(rule[0][0][0], Box)
    self.assertIsInstance(rule[0][0][1], Box)
    self.assertIsInstance(rule[0][1], Box)

  def test_and_vs_or_assoc(self):
    scene = self.parse('$ = box & box | ball')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], And)
    self.assertIsInstance(rule[0][0], Box)
    self.assertIsInstance(rule[0][1], Or)
    self.assertIsInstance(rule[0][1][0], Box)
    self.assertIsInstance(rule[0][1][1], Ball)

  def test_power_vs_transform_assoc(self):
    scene = self.parse('$ = box : s 1 ^1')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], Power)
    self.assertIsInstance(rule[0][0], Transform)
    self.assertIsInstance(rule[0][0][0], Box)

  def test_and_vs_power_assoc(self):
    scene = self.parse('$ = box & box ^1')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], And)
    self.assertIsInstance(rule[0][0], Box)
    self.assertIsInstance(rule[0][1], Power)
    self.assertIsInstance(rule[0][1][0], Box)

  def test_or_vs_transform_assoc(self):
    scene = self.parse('$ = box | box : s 1')
    rule = scene.find_rule('$')
    self.assertIsInstance(rule[0], Or)
    self.assertIsInstance(rule[0][0], Box)
    self.assertIsInstance(rule[0][1], Transform)
    self.assertIsInstance(rule[0][1][0], Box)

if __name__ == '__main__':
  unittest.main()
