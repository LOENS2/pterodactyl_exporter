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
                        'is_transferring': False,
                        'is_node_under_maintenance': False,
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
                },
                {
                    'attributes': {
                        'is_suspended': True,
                        'is_installing': False,
                        'is_transferring': False,
                        'is_node_under_maintenance': False,
                        'name': 'server2',
                        'identifier': 'id2',
                        'limits': {
                            'memory': 4543,
                            'swap': 321,
                            'disk': 4353,
                            'io': 23,
                            'cpu': 3
                        }
                    }
                },
                {
                    'attributes': {
                        'is_suspended': False,
                        'is_installing': True,
                        'is_transferring': False,
                        'is_node_under_maintenance': False,
                        'name': 'server3',
                        'identifier': 'id3',
                        'limits': {
                            'memory': 6544,
                            'swap': 43,
                            'disk': 7544,
                            'io': 325,
                            'cpu': 2
                        }
                    }
                },
                {
                    'attributes': {
                        'is_suspended': False,
                        'is_installing': False,
                        'is_transferring': True,
                        'is_node_under_maintenance': False,
                        'name': 'server4',
                        'identifier': 'id4',
                        'limits': {
                            'memory': 1024,
                            'swap': 0,
                            'disk': 2048,
                            'io': 500,
                            'cpu': 2
                        }
                    }
                },
                {
                    'attributes': {
                        'is_suspended': False,
                        'is_installing': False,
                        'is_transferring': False,
                        'is_node_under_maintenance': True,
                        'name': 'server5',
                        'identifier': 'id5',
                        'limits': {
                            'memory': 1024,
                            'swap': 0,
                            'disk': 2048,
                            'io': 500,
                            'cpu': 2
                        }
                    }
                },
                {
                    'attributes': {
                        'is_suspended': False,
                        'is_installing': False,
                        'is_transferring': False,
                        'is_node_under_maintenance': False,
                        'name': 'server6',
                        'identifier': 'id6',
                        'limits': {
                            'memory': 5436,
                            'swap': 0,
                            'disk': 3554,
                            'io': 4350,
                            'cpu': 5
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
                        'is_transferring': False,
                        'is_node_under_maintenance': False,
                        'name': 'server7',
                        'identifier': 'id7',
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

        response_error = MagicMock()
        response_error.status_code = 504

        mock_get.side_effect = [
            response_servers_page1,
            response_servers_page1,
            response_servers_page2,
            response_resources_s1,
            response_backup_s1,
            response_error,
            response_resources_s2,
            response_backup_s2
        ]

        client = HTTPClient(config)
        metrics = client.get_metrics()

        # check fetch servers
        self.assertEqual(metrics.name, ['server1', 'server6','server7'])
        self.assertEqual(metrics.id, ['id1', 'id6','id7'])
        self.assertEqual(metrics.max_memory, [1024, 5436, 2048])
        self.assertEqual(metrics.max_swap, [0, 0, 0])
        self.assertEqual(metrics.max_disk, [2048, 3554, 4096])
        self.assertEqual(metrics.io, [500, 4350, 1000])
        self.assertEqual(metrics.max_cpu, [2, 5, 4])

        # check fetch resources
        self.assertEqual(metrics.memory, [1, 2])  # bytes to MiB
        self.assertEqual(metrics.cpu, [20, 40])
        self.assertEqual(metrics.disk, [2, 4])
        self.assertEqual(metrics.rx, [0.5, 1.0])
        self.assertEqual(metrics.tx, [0.5, 1.0])
        self.assertEqual(metrics.uptime, [12345, 67890])

        # check fetch backup
        self.assertEqual(metrics.last_backup_time, [1748520000, 1748433600])


    if __name__ == '__main__':
        unittest.main()
