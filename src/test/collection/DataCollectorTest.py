import pytest
from sqlite3 import Cursor
from time import sleep
from typing import Dict, List, Optional
from chariot.collection import DataCollector
from chariot.collection.configuration import DataCollectionConfiguration
from chariot.database.configuration import DatabaseConfiguration
from chariot.network import Network
from chariot.network.configuration import NetworkConfiguration
from chariot.utility.JSONTypes import JSONObject
from test.testutils import MockDeviceTester, TestDatabaseWriter


class DataCollectorTest(MockDeviceTester):
    instance: Optional[DataCollector] = None
    NUM_DEVICES: int = 64
    EPISODE_LEN: float = 15.0

    def _buildNetwork(self) -> Network:
        networkConfig: NetworkConfiguration = NetworkConfiguration({
            'networkName': 'Network 1',
            'description': 'Sample network',
        })
        network: Network = Network(networkConfig)
        return network

    def _buildDatabase(self) -> TestDatabaseWriter:
        dbConfig: DatabaseConfiguration = DatabaseConfiguration({
            'dbId': 'Test Database',
            'databaseName': 'TestDataStore',
            'type': 'TestDB',
            'host': 'localhost',
        })
        dbWriter: TestDatabaseWriter = TestDatabaseWriter(dbConfig)
        return dbWriter

    def emptyNetworkTest(self):
        collectorConfig: DataCollectionConfiguration = DataCollectionConfiguration({
            'configId': 'Test Collector',
            'network': self._buildNetwork(),
            'database': self._buildDatabase(),
        })
        self.instance = DataCollector(collectorConfig)
        with pytest.raises(AssertionError):
            self.instance.startCollection()

    def validNetworkTest(self):
        network: Network = self._buildNetwork()
        database: TestDatabaseWriter = self._buildDatabase()
        for i in range(self.NUM_DEVICES):
            network.addDevice(self._buildDevice(f'Test Device {i + 1}'))
        collectorConfig: DataCollectionConfiguration = DataCollectionConfiguration({
            'configId': 'Test Collector',
            'network': network,
            'database': database,
        })
        self.instance = DataCollector(collectorConfig)
        self.instance.startCollection()
        assert self.instance.isRunning() == True
     
        # this object should be locked from modificaiton while episode is running
        # this is better enforced by the web API, but why not
        with pytest.raises(AssertionError):
            self.instance.updateConfig({})

        sleep(self.EPISODE_LEN)
        self.instance.stopCollection()

        assert self.instance.isRunning() == False

        # Test Database doesn't actually disconnect though, just says it is
        assert database.isConnected() == False

        # check that all devices were able to report data
        db: Cursor = database.getClient()
        dataDict: Dict[str, List[JSONObject]] = {}

        # there are random failures with this query, not sure why
        for record in db.execute('SELECT * from data'):
            if record[1] not in dataDict:
                dataDict[record[1]] = [record]
            else:
                dataDict[record[1]].append(record)

        database.cleanup()
        assert len(dataDict.keys()) == self.NUM_DEVICES

        # this should no longer fail as the lock has been released
        self.instance.updateConfig({})
