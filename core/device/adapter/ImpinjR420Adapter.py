from queue import Queue
from sllurp.llrp import LLRPClientFactory
from twisted.internet import reactor
from typing import Union
from core.JSONTypes import JSONObject
from core.device.adapter.DeviceAdapter import DeviceAdapter
from core.device.configuration.ImpinjR420Configuration import ImpinjR420Configuration

class ImpinjR420Adapter(DeviceAdapter):
    def __init__(self, config: ImpinjR420Configuration):
        super().__init__(config)
        self.llrpFactory: Union[LLRPClientFactory, None] = None

    def _reportData(self, data: Dict[str, JSONObject]):
        self.dataQueue.put(data, block=True)

    def beginDataCollection(self, errorQueue: Queue) -> None:
        if not self.connected:
            # raise DeviceNotConnected(?)Error
            stackTrace = self._generateStackTrace(AssertionError('Device was not connected'))
            errorQueue.put(stackTrace, block=True)
        self.inCollectionEpisode = True
        try:
            self.llrpFactory.addTagReportCallback(self._reportData)
            reactor.run()
        except Exception as err:
            stackTrace = self._generateStackTrace(err)
            errorQueue.put(stackTrace, block=True)

    def connect(self) -> None:
        #TODO: condition for the abscence of optional configs
        self.llrpFactory = LLRPClientFactory(
            report_every_n_tags=self._config.report_every_n_tags,
            tx_power=self._config.tx_power,
            session=self._config.session,  
            start_inventory=self._config.start_inventory,
            mode_identifier=self._config.mode_indentifier,
            tag_population=self._config.tag_population,
            tag_content_selector={
                'EnableROSpecID': self._config.EnableROSpecID,
                'EnableSpecIndex': self._config.EnableSpecIndex,
                'EnableInventoryParameterSpecID': self._config.EnableInventoryParameterSpecID,
                'EnableAntennaID': self._config.EnableAntennaID,
                'EnableChannelIndex': self._config.EnableChannelIndex,
                'EnablePeakRSSI': self._config.EnablePeakRSSI_General,  
                'EnableFirstSeenTimestamp': self._config.EnableFirstSeenTimestamp,
                'EnableLastSeenTimestamp': self._config.EnableLastSeenTimestamp,
                'EnableTagSeenCount': self._config.EnableTagSeenCount,
                'EnableAccessSpecID': self._config.EnableAccessSpecID
            },
            impinj_tag_content_selector={
                'EnablePeakRSSI': self._config.EnablePeakRSSI_Impinj,
                'EnableRFPhaseAngle': self._config.EnableRFPhaseAngle,
                'EnableRFDopplerFrequency': self._config.EnableRFDopplerFrequency
            })
        reactor.connectTCP(self._config.ipAddress, self._config.port, self.llrpFactory, timeout=5)
        self.connected = True

    def disconnect(self) -> None:
        if not self.connected:
            # raise DeviceNotConnected(?)Error
            raise AssertionError
        self.llrpFactory = None

    
    def stopDataCollection(self) -> None:
        super().stopDataCollection()
        reactor.stop()


__all__ = ['ImpinjR420Adapter']
