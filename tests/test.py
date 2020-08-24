import unittest
from prometheus_build_info import builder
from prometheus_client import REGISTRY
from click.testing import CliRunner
import sys
import os
from json import load


class BuildInfoTestCase(unittest.TestCase):
    def tearDown(self):
        try:
            os.remove("build_info.json")
        except OSError as err:
            print("Nothing to cleanup")

    def test_metric(self):
        print("test_metric")
        # Setup build_info
        runner = CliRunner()
        runner.invoke(builder.make_build_info, ["test_app", "master", "abcdef", "1.0.0"])
        python_version_info = sys.version_info
        python_version = "{}.{}.{}".format(python_version_info.major, python_version_info.minor,
                                           python_version_info.micro)

        # Unregister all collectors.
        collectors = list(REGISTRY._collector_to_names.keys())
        print(f"before unregister collectors={collectors}")
        for collector in collectors:
            REGISTRY.unregister(collector)
        print(f"after unregister collectors={list(REGISTRY._collector_to_names.keys())}")

        labels = {"branch": "master",
                  "revision": "abcdef",
                  "pythonversion": python_version,
                  "version": "1.0.0"}

        # Test
        before = REGISTRY.get_sample_value("test_app_build_info", labels)
        from prometheus_build_info import info
        after = REGISTRY.get_sample_value("test_app_build_info", labels)
        self.assertEqual(before, None)
        self.assertEqual(after, 1.0)
        print("before: {}".format(before))
        print("after: {}".format(after))

        # Cleanup
        os.remove("build_info.json")

    def test_no_buildinfo(self):
        print("test_no_buildinfo")
        try:
            os.remove("build_info.json")
        except OSError as err:
            print("Nothing to cleanup")

        # Unregister all collectors.
        collectors = list(REGISTRY._collector_to_names.keys())
        print(f"before unregister collectors={collectors}")
        for collector in collectors:
            REGISTRY.unregister(collector)
        print(f"after unregister collectors={list(REGISTRY._collector_to_names.keys())}")

        python_version_info = sys.version_info
        python_version = "{}.{}.{}".format(python_version_info.major, python_version_info.minor,
                                           python_version_info.micro)
        labels = {"branch": "master",
                  "revision": "abcdef",
                  "pythonversion": python_version,
                  "version": "1.0.0"}
        before = REGISTRY.get_sample_value("test_app_build_info", labels)
        print("before: {}".format(before))
        from prometheus_build_info import info
        after = REGISTRY.get_sample_value("test_app_build_info", labels)
        print("after: {}".format(after))
        self.assertEqual(before, None)
        self.assertEqual(after, None)


class BuildBuilderTestCase(unittest.TestCase):
    def test_builder(self):
        runner = CliRunner()
        runner.invoke(builder.make_build_info, ["test_app", "master", "abcdef", "1.0.0"])
        self.assertEqual(os.path.exists("build_info.json"), True)

        with open(os.getcwd() + "/build_info.json", "r") as buildinfo:
            info = load(buildinfo)

        self.assertEqual(info['appname'], "test_app")
        self.assertEqual(info['branch'], "master")
        self.assertEqual(info['revision'], "abcdef")
        self.assertEqual(info['version'], "1.0.0")

    def tearDown(self):
        os.remove("build_info.json")


if __name__ == '__main__':
    unittest.main()
