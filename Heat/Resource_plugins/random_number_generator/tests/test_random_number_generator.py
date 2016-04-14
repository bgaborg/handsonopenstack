"""
Hints about actually running this:
  Create a new directory called random_number_generator in <heat>/contrib/
  Copy the entire random_number_generator directory into this new directory
"""

import six

from heat.common import exception
from heat.common import template_format
from heat.engine import stack as parser
from heat.engine import template
from heat.engine import resource
from heat.tests import common
from heat.tests import utils
from random_number_generator import random_number_generator

class TestRandomNumberGenerator(common.HeatTestCase):
    def setUp(self):
        resource._register_class("Nokia::lCase::RandomNumberGenerator", random_number_generator.RandomNumberGenerator)
        super(TestRandomNumberGenerator, self).setUp()
        self.ctx = utils.dummy_context()

    def create_stack(self, template_string):
        self.stack = self.parse_stack(template_format.parse(template_string))
        self.assertIsNone(self.stack.create())
        return self.stack

    def parse_stack(self, template_string):
        stack_name = 'test_stack'
        tmpl = template.Template(template_string)
        stack = parser.Stack(utils.dummy_context(), stack_name, tmpl)
        stack.validate()
        stack.store()
        return stack

    def test_random_number_generator(self):
        template_rng = '''
heat_template_version: 2014-10-16
resources:
  rng:
    type: Nokia::lCase::RandomNumberGenerator
    properties:
      LowerBound: 0
      UpperBound: 5
'''
        stack = self.create_stack(template_rng)
        rng = stack['rng']

        random_number = rng.FnGetAtt('NextInt')
        self.assertRaises(exception.InvalidTemplateAttribute,
                          rng.FnGetAtt, 'foo')
        self.assertTrue(0 <= random_number <= 5)

    def test_missing_bounds(self):
        template_rng = '''
heat_template_version: 2014-10-16
resources:
  rng:
    type: Nokia::lCase::RandomNumberGenerator
    properties:
      UpperBound: 5
'''
        exc = self.assertRaises(exception.StackValidationFailed,
                                self.create_stack, template_rng)
        self.assertEqual('Property error: resources.rng.properties: Property LowerBound not assigned',
                         six.text_type(exc))

    def test_lower_bound_greater_than_upper_bound(self):
        template_rng = '''
heat_template_version: 2014-10-16
resources:
  rng:
    type: Nokia::lCase::RandomNumberGenerator
    properties:
      LowerBound: 5
      UpperBound: 0
'''
        exc = self.assertRaises(exception.StackValidationFailed,
                                self.create_stack, template_rng)
        self.assertEqual('The value of parameter "UpperBound" (0) should be greater or equal to "LowerBound" (5).',
                         six.text_type(exc))
