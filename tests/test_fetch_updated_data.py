"""Network-free checks for bounded retries and safe partial-file replacement."""
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, call
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from fetch_updated_data import download

URL = 'https://example.invalid/test.nc'


class InterruptedBody(io.BytesIO):
    def __init__(self):
        super().__init__(b'long incomplete payload')
        self.reads = 0

    def read(self, size=-1):
        self.reads += 1
        if self.reads > 1:
            raise URLError('simulated interrupted transfer')
        return super().read(size)


class DownloadRetryTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.partial = Path(self.directory.name) / 'test.nc.part'
        self.sleep = Mock()

    def test_transient_gateway_error_then_success(self):
        opener = Mock(side_effect=[HTTPError(URL, 504, 'Gateway timeout', None, None),
                                   io.BytesIO(b'complete')])
        download(URL, self.partial, opener=opener, sleep=self.sleep)
        self.assertEqual(self.partial.read_bytes(), b'complete')
        self.assertEqual(opener.call_count, 2)
        self.sleep.assert_called_once_with(2)

    def test_interrupted_partial_is_rewritten_not_appended(self):
        self.partial.write_bytes(b'older partial file with trailing bytes')
        opener = Mock(side_effect=[InterruptedBody(), io.BytesIO(b'new')])
        download(URL, self.partial, opener=opener, sleep=self.sleep)
        self.assertEqual(self.partial.read_bytes(), b'new')
        self.assertEqual(opener.call_count, 2)
        self.sleep.assert_called_once_with(2)

    def test_permanent_http_errors_fail_without_retry(self):
        for status in (403, 404):
            with self.subTest(status=status):
                opener = Mock(side_effect=HTTPError(URL, status, 'Permanent', None, None))
                with self.assertRaises(HTTPError):
                    download(URL, self.partial, opener=opener, sleep=self.sleep)
                self.assertEqual(opener.call_count, 1)
        self.sleep.assert_not_called()

    def test_timeout_stops_after_four_attempts(self):
        opener = Mock(side_effect=TimeoutError('simulated timeout'))
        with self.assertRaises(TimeoutError):
            download(URL, self.partial, opener=opener, sleep=self.sleep)
        self.assertEqual(opener.call_count, 4)
        self.assertEqual(self.sleep.call_args_list, [call(2), call(4), call(8)])


if __name__ == '__main__':
    unittest.main()
