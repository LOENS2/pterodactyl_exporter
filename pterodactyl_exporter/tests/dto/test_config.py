import unittest
from pterodactyl_exporter.dto.config import Config


class TestConfig(unittest.TestCase):
    def test_validate_port_valid(self):
        self.assertEqual(Config.validate_port(8080, field=None), 8080)

    def test_validate_port_invalid(self):
        with self.assertRaises(ValueError):
            Config.validate_port(70000, field=None)

        with self.assertRaises(ValueError):
            Config.validate_port('abc', field=None)

    def test_validate_server_list_type_valid(self):
        self.assertEqual(Config.validate_server_list_type("", field=None), "")
        self.assertEqual(Config.validate_server_list_type("owner", field=None), "owner")
        self.assertEqual(Config.validate_server_list_type("admin-all", field=None), "admin-all")

    def test_validate_server_list_type_invalid(self):
        with self.assertRaises(ValueError):
            Config.validate_server_list_type("invalid")
        with self.assertRaises(ValueError):
            Config.validate_server_list_type(1234)

    def test_validate_https_valid(self):
        self.assertEqual(Config.validate_https(True, field=None), True)
        self.assertEqual(Config.validate_https(False, field=None), False)
        self.assertEqual(Config.validate_https(0, field=None), False)
        self.assertEqual(Config.validate_https(1, field=None), True)
        self.assertEqual(Config.validate_https(10, field=None), True)
        self.assertEqual(Config.validate_https(-10, field=None), True)

    def test_validate_https_invalid(self):
        with self.assertRaises(ValueError):
            Config.validate_https('abc', field=None)

    def test_validate_ignore_ssl_valid(self):
        self.assertEqual(Config.validate_ignore_ssl(False, field=None), False)

    def test_validate_ignore_ssl_invalid(self):
        with self.assertRaises(ValueError):
            Config.validate_ignore_ssl('abc', field=None)


if __name__ == '__main__':
    unittest.main()
