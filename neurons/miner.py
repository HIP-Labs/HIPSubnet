import typing
import random
import time
import bittensor as bt
import hip
from hip.base.miner import BaseMinerNeuron

class Miner(BaseMinerNeuron):
    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)

    async def forward(self, synapse: hip.protocol.HIPProtocol) -> hip.protocol.HIPProtocol:
        """
        Process the incoming HIPProtocol synapse by selecting an option based on the task.
        """
        # Extract the task data from the synapse
        task_data = synapse.data

        # Determine the human-likeness of the task data
        human_likeness = await self.evaluate_human_likeness(task_data)

        # Set the miner's response in the synapse
        synapse.response = human_likeness

        return synapse

    async def blacklist(self, synapse: hip.protocol.HIPProtocol) -> typing.Tuple[bool, str]:
        """
        Determine if the incoming request should be blacklisted.
        """
        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            bt.logging.trace(f"Blacklisting unregistered hotkey {synapse.dendrite.hotkey}")
            return True, "Unrecognized hotkey"

        if not self.metagraph.validator_permit[uid]:
            bt.logging.warning(f"Blacklisting request from non-validator hotkey {synapse.dendrite.hotkey}")
            return True, "Non-validator hotkey"

        return False, "Hotkey recognized!"

    async def priority(self, synapse: hip.protocol.HIPProtocol) -> float:
        """
        Assign priority to the incoming request.
        """
        caller_uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        priority = float(self.metagraph.S[caller_uid])
        bt.logging.trace(f"Prioritizing {synapse.dendrite.hotkey} with value: {priority}")
        return priority

    async def evaluate_human_likeness(self, task_data: str) -> str:
        """
        Evaluate the human-likeness of the given task data.
        """
        try:
            # Present the task data to the user through an interface
            human_likeness = await self.present_task_to_user(task_data)
            bt.logging.debug(f"User evaluated human-likeness as '{human_likeness}' for task data: {task_data}")
            return human_likeness
        except Exception as e:
            bt.logging.error(f"Error evaluating human-likeness for task data: {task_data}. Error: {str(e)}")
            return "Unsure"

    async def present_task_to_user(self, task_data: str) -> str:
        """
        Present the task data to the user through an interface and return the evaluated human-likeness.
        """
        # TODO: Implement the logic to present the task data to the user through an interface
        # and return the evaluated human-likeness
        # For now, we'll simulate user evaluation by randomly selecting a human-likeness option
        options = ["Very Human-like", "Somewhat Human-like", "Not Human-like", "Unsure"]
        human_likeness = random.choice(options)
        return human_likeness

# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)