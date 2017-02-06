import os
from hypothesis import settings, Verbosity

try:
    hypothesis_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../.hypothesis')
    settings.register_profile("ci", settings(max_examples=100000, verbosity=Verbosity.verbose))
    settings.register_profile("default", settings(max_examples=10000, verbosity=Verbosity.verbose))
    settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))
except ImportError:
    # Hypothesis is not being used in this job so we don't care
    pass
