import unittest
from unittest.mock import patch, MagicMock
from pterodactyl_exporter.http_client import HTTPClient
from pterodactyl_exporter.dto.config import Config
from pterodactyl_exporter.enum.server_list_type import ServerListType

class TestHTTPClient(unittest.TestCase):
    @patch('pterodactyl_exporter.http_client.requests.get')
    def test_get_metrics(self, mock_get):
        config = Config(
            port=9531,
            host="example.com",
            api_key="test123",
            https=True,
            ignore_ssl=False,
            server_list_type=ServerListType.OWNER
        )

        # Page 1
        response_servers_page1 = MagicMock()
        response_servers_page1.status_code = 200
        response_servers_page1.json.return_value = {
            'meta': {'pagination': {'total_pages': 2}},
            'data': [
                {
                    'attributes': {
                        'is_suspended': False,
                        'is_installing': False,
                        'name': 'server1',
                        'identifier': 'id1',
                        'limits': {
                            'memory': 1024,
                            'swap': 0,
                            'disk': 2048,
                            'io': 500,
                            'cpu': 2
                        }
                    }
                }
            ]
        }

        # Page 2
        response_servers_page2 = MagicMock()
        response_servers_page2.status_code = 200
        response_servers_page2.json.return_value = {
            'meta': {'pagination': {'total_pages': 2}},
            'data': [
                {
                    'attributes': {
                        'is_suspended': False,
                        'is_installing': False,
                        'name': 'server2',
                        'identifier': 'id2',
                        'limits': {
                            'memory': 2048,
                            'swap': 0,
                            'disk': 4096,
                            'io': 1000,
                            'cpu': 4
                        }
                    }
                }
            ]
        }

        response_resources_s1 = MagicMock()
        response_resources_s1.status_code = 200
        response_resources_s1.json.return_value = {
            'attributes': {
                'resources': {
                    'memory_bytes': 1048576,
                    'cpu_absolute': 20,
                    'disk_bytes': 2097152,
                    'network_rx_bytes': 524288,
                    'network_tx_bytes': 524288,
                    'uptime': 12345
                }
            }
        }

        response_backup_s1 = MagicMock()
        response_backup_s1.status_code = 200
        response_backup_s1.json.return_value = {
            'data': [
                {
                    'attributes': {
                        'completed_at': '2025-05-29T12:00:00Z',
                        'is_successful': True
                    }
                }
            ]
        }

        response_resources_s2 = MagicMock()
        response_resources_s2.status_code = 200
        response_resources_s2.json.return_value = {
            'attributes': {
                'resources': {
                    'memory_bytes': 2097152,
                    'cpu_absolute': 40,
                    'disk_bytes': 4194304,
                    'network_rx_bytes': 1048576,
                    'network_tx_bytes': 1048576,
                    'uptime': 67890
                }
            }
        }

        response_backup_s2 = MagicMock()
        response_backup_s2.status_code = 200
        response_backup_s2.json.return_value = {
            'data': [
                {
                    'attributes': {
                        'completed_at': '2025-05-28T12:00:00Z',
                        'is_successful': True
                    }
                }
            ]
        }

        mock_get.side_effect = [
            response_servers_page1,
            response_servers_page1,
            response_servers_page2,
            response_resources_s1,
            response_backup_s1,
            response_resources_s2,
            response_backup_s2
        ]

        client = HTTPClient(config)
        metrics = client.get_metrics()

        self.assertEqual(metrics.name, ['server1', 'server2'])
        self.assertEqual(metrics.id, ['id1', 'id2'])
        self.assertEqual(metrics.max_memory, [1024, 2048])
        self.assertEqual(metrics.memory, [1, 2])  # bytes to MiB
        self.assertEqual(metrics.cpu, [20, 40])
        self.assertEqual(metrics.disk, [2, 4])
        self.assertEqual(metrics.uptime, [12345, 67890])
        self.assertEqual(len(metrics.last_backup_time), 2)
        self.assertGreater(metrics.last_backup_time[0], 0)
        self.assertGreater(metrics.last_backup_time[1], 0)


    if __name__ == '__main__':
        unittest.main()
