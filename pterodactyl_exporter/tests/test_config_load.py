import unittest
from unittest.mock import mock_open, patch
from ..config_load import get_config


class TestGetConfig(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open,
           read_data="host: example.com\nport: 8080\napi_key: test123\nhttps: true\nignore_ssl: false\nserver_list_type: owner\nquery_interval: 15")
    def test_get_config_valid(self, mock_file_open):
        path = "test_config.yml"

        config = get_config(path)

        self.assertEqual(config.host, "example.com")
        self.assertEqual(config.port, 8080)
        self.assertEqual(config.api_key, "test123")
        self.assertEqual(config.https, True)
        self.assertEqual(config.ignore_ssl, False)
        self.assertEqual(config.server_list_type, "owner")
        self.assertEqual(config.query_interval, 15)

        mock_file_open.assert_called_once_with(path)


if __name__ == '__main__':
    unittest.main()
