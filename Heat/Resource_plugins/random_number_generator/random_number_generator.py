from oslo_log import log as logging
from heat.common import exception
from heat.common.i18n import _
from heat.engine import attributes
from heat.engine import properties
from heat.engine import resource
import random

LOG = logging.getLogger(__name__)

class RandomNumberGenerator(resource.Resource):
    """Resource to generate a random number between the parameters LowerBound and UpperBound (inclusive).
    """
    PROPERTIES = (
        LOWER_BOUND,
        UPPER_BOUND,
    ) = (
        'LowerBound',
        'UpperBound',
    )

    ATTRIBUTES = (
        NEXT_INT,
    ) = (
        'NextInt',
    )

    properties_schema = {
        LOWER_BOUND: properties.Schema(
            properties.Schema.INTEGER,
            _('Lower bound of generated numbers (inclusive)'),
            required=True
        ),
        UPPER_BOUND: properties.Schema(
            properties.Schema.INTEGER,
            _('Upper bound of generated numbers (inclusive)'),
            required=True
        ),
    }

    attributes_schema = {
        NEXT_INT: attributes.Schema(
            _("A random integer between the parameters LowerBound and UpperBound (inclusive)"),
            type=attributes.Schema.INTEGER
        ),
    }

    def handle_create(self):
        random.seed

    def validate(self):
        super(RandomNumberGenerator, self).validate()

        lower_bound = self.properties[self.LOWER_BOUND]
        upper_bound = self.properties[self.UPPER_BOUND]
        # Make sure that upper bound is greater or equal to lower bound
        if upper_bound < lower_bound:
            msg = _(
                "The value of parameter \"%s\" (%d) should be greater or equal to \"%s\" (%d).") % \
                (self.UPPER_BOUND, upper_bound, self.LOWER_BOUND, lower_bound)
            raise exception.StackValidationFailed(message=msg)

    def _resolve_attribute(self, name):
        if name == self.NEXT_INT:
            return random.randint(self.properties[self.LOWER_BOUND], self.properties[self.UPPER_BOUND])

def resource_mapping():
    return {
        'Nokia::lCase::RandomNumberGenerator': RandomNumberGenerator,
    }
