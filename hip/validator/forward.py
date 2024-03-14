import bittensor as bt
from hip.protocol import HIPProtocol
from hip.validator.reward import get_rewards, weighted_means_consensus
from hip.utils.uids import get_random_uids
import asyncio
from hip_service import SocketIOClient

async def forward(self):
    """
    The forward function is called by the validator every time step.
    It is responsible for querying the network and scoring the responses.
    """
    # Get the total number of active miners
    active_miners = len(self.metagraph.uids)

    # Calculate the number of groups based on the number of active miners
    if active_miners < 32:
        num_groups = 2
    elif active_miners < 128:
        num_groups = 4
    else:
        num_groups = 8

    # Calculate the group size based on the number of active miners and groups
    group_size = max(active_miners // num_groups, 8)

    # Assign random UIDs to groups
    miner_groups = [get_random_uids(self, k=group_size) for _ in range(num_groups)]

    # Generate tasks for each group using data from the WebSocket server
    tasks = []
    client = SocketIOClient()
    await client.connect("wss://hipservice-production.up.railway.app")
    for _ in range(num_groups):
        completion = await client.getRandomCompletion()
        if completion is not None:
            task = self.generate_task(completion)
            tasks.append(task)
        else:
            bt.logging.warning("Failed to retrieve random completion from the WebSocket server.")
    await client.close()

    # Query each group of miners with their respective task
    responses_by_group = []
    weights_by_group = []
    for group_index, group_uids in enumerate(miner_groups):
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in group_uids],
            synapse=[HIPProtocol(data=tasks[group_index], uid=uid) for uid in group_uids],
            deserialize=True,
        )
        responses_by_group.append([r.response for r in responses])
        weights_by_group.append([self.metagraph.S[uid].item() for uid in group_uids])

    # Establish ground truth for each group based on responses and weights
    ground_truths = [weighted_means_consensus(self, responses, weights)
                     for responses, weights in zip(responses_by_group, weights_by_group)]

    # Query each group of miners with the ground truth from the other groups
    cross_validated_responses = []
    for group_index, group_uids in enumerate(miner_groups):
        other_group_indices = [i for i in range(num_groups) if i != group_index]
        for other_group_index in other_group_indices:
            other_ground_truth = ground_truths[other_group_index]
            responses = await self.dendrite(
                axons=[self.metagraph.axons[uid] for uid in group_uids],
                synapse=[HIPProtocol(data=tasks[group_index], uid=uid, consensus=other_ground_truth) for uid in group_uids],
                deserialize=True,
            )
            cross_validated_responses.extend(responses)

    # Calculate rewards based on responses and ground truths
    rewards = get_rewards(self, cross_validated_responses, ground_truths)

    # Update scores based on rewards
    self.update_scores(rewards, [uid for group_uids in miner_groups for uid in group_uids])

    bt.logging.info("Validator forward pass completed")

    # Wait for 30 seconds before the next task
    await asyncio.sleep(30)