from typing import Optional
from test.testutils.MockServer import MockServer
from test.testutils.TestDeviceAdapter import TestDeviceAdapter
from test.testutils.TestDeviceConfiguration import TestDeviceConfiguration


class MockDeviceTester:
    server: Optional[MockServer] = None

    @classmethod
    def setup_class(cls):
        cls.server: MockServer = MockServer()
        cls.server.start()

    @classmethod
    def teardown_class(cls):
        cls.server.stop()

    def _buildDevice(self, name: str, pollDelay: int = 500, strLen: int = 10) -> TestDeviceAdapter:
        config: TestDeviceConfiguration = self._buildDeviceConfig(name, pollDelay, strLen)
        device: TestDeviceAdapter = TestDeviceAdapter(config)
        return device

    def _buildDeviceConfig(self, name: str, pollDelay, strLen) -> TestDeviceConfiguration:
        return TestDeviceConfiguration({
            'deviceId': name,
            'deviceType': 'TestDevice',
            'pollDelay': pollDelay,
            'strLen': strLen,
        })
