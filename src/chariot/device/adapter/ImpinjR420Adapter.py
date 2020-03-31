from sllurp.llrp import LLRPClientFactory
from twisted.internet import reactor
from typing import Dict, Optional
from chariot.device.adapter import DeviceAdapter
from chariot.device.configuration import ImpinjR420Configuration


class ImpinjR420Adapter(DeviceAdapter):
    def __init__(self, config: ImpinjR420Configuration):
        super().__init__(config)
        self.llrpFactory: Optional[LLRPClientFactory] = None

    def _startDataCollection(self) -> None:
        self.llrpFactory.addTagReportCallback(self._reportData)
        reactor.run()

    def _connect(self) -> None:
        # TODO: condition for the abscence of optional configs
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

    def _disconnect(self) -> None:
        self.llrpFactory = None

    def _stopDataCollection(self) -> None:
        reactor.stop()


__all__ = ['ImpinjR420Adapter']
