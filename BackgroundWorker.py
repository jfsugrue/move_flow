from PyQt5.QtCore import QObject, pyqtSignal
from AtomicApi import AtomicApi


class BackgroundWorker(QObject):
    update = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        # adjust the flows list to match the flows you want to move along with their names. Id is source AF id
        flows = [
            #{'id': '<your action flow id>', 'name': '<the name you want to call it once moved>'},
        ]

        api = AtomicApi()
        # run thru the flows list and get each config and add to dest environment
        # then update the name as this isn't sent in the config
        for flow in flows:
            flow_id = flow['id']
            name = flow['name']
            flow_config = api.get_flow_config(flow_id)
            self.update.emit(f'Converting {name}...')
            api.post_flow_config(flow_id, flow_config)
            self.update.emit('Done')
            self.update.emit('Updating')
            api.update_action_flow(flow_id, name)
            self.update.emit("--------------------------")

        self.finished.emit()
