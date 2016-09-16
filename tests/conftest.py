import os
from hypothesis import settings, Verbosity
from tests.examples_database import ThreadedSQLiteExampleDatabase

hypothesis_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../.hypothesis')
settings.register_profile("ci", settings(max_examples=100000, verbosity=Verbosity.verbose,
                                         database=ThreadedSQLiteExampleDatabase(max_workers=2, path=hypothesis_path)))
settings.register_profile("default", settings(max_examples=10000, verbosity=Verbosity.verbose,
                                              database=ThreadedSQLiteExampleDatabase(max_workers=4)))
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))
