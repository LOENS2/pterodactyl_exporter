import unittest
from unittest.mock import MagicMock
from pterodactyl_exporter.http_server import HTTPServer
from pterodactyl_exporter.dto.config import Config
from pterodactyl_exporter.dto.metrics import Metrics


class TestHTTPServer(unittest.TestCase):
    def test_serve_metrics(self):
        config = Config(
            port=9531,
            host="example.com",
            api_key="test123",
            https=True,
            ignore_ssl=False,
            server_list_type="owner"
        )

        http_server = HTTPServer(config)
        http_server.metric_gauges = {
            "memory": MagicMock(),
            "cpu": MagicMock(),
            "disk": MagicMock(),
            "rx": MagicMock(),
            "tx": MagicMock(),
            "uptime": MagicMock(),
            "max_memory": MagicMock(),
            "max_swap": MagicMock(),
            "max_disk": MagicMock(),
            "io": MagicMock(),
            "max_cpu": MagicMock(),
            "last_backup_time": MagicMock()
        }

        metrics = Metrics(
            name=["Server1", "Server2"],
            id=["id1", "id2"],
            memory=[1024, 2048],
            cpu=[50, 75],
            disk=[512, 1024],
            rx=[100, 200],
            tx=[150, 250],
            uptime=[3600000, 7200000],
            max_memory=[4096, 8192],
            max_swap=[2048, 4096],
            max_disk=[2048, 4096],
            io=[1, 2],
            max_cpu=[90, 95],
            last_backup_time=[1234567890, 1234567900]
        )

        http_server.serve_metrics(metrics)

        expected_calls = [
            ((1024,), ("Server1", "id1")),
            ((50,), ("Server1", "id1")),
            ((512,), ("Server1", "id1")),
            ((100,), ("Server1", "id1")),
            ((150,), ("Server1", "id1")),
            ((3600000,), ("Server1", "id1")),
            ((4096,), ("Server1", "id1")),
            ((2048,), ("Server1", "id1")),
            ((2048,), ("Server1", "id1")),
            ((1,), ("Server1", "id1")),
            ((90,), ("Server1", "id1")),
            ((1234567890,), ("Server1", "id1")),

            ((2048,), ("Server2", "id2")),
            ((75,), ("Server2", "id2")),
            ((1024,), ("Server2", "id2")),
            ((200,), ("Server2", "id2")),
            ((250,), ("Server2", "id2")),
            ((7200000,), ("Server2", "id2")),
            ((8192,), ("Server2", "id2")),
            ((4096,), ("Server2", "id2")),
            ((4096,), ("Server2", "id2")),
            ((2,), ("Server2", "id2")),
            ((95,), ("Server2", "id2")),
            ((1234567900,), ("Server2", "id2")),
        ]
        for metric_name, mock_obj in http_server.metric_gauges.items():
            for call_args, call_kwargs in expected_calls:
                if metric_name in call_kwargs:
                    mock_obj.labels.assert_called_with(*call_kwargs)

    if __name__ == '__main__':
        unittest.main()
