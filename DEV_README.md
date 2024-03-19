# HIP Subnet Documentation

## Overview
The HIP subnet is designed to determine the human-likeness of data by leveraging the collective intelligence of human miners. The subnet consists of validators and miners who work together to establish a consensus on the human-likeness of given data samples. The subnet interacts with a centralized database hosted on Railway.app and aims to provide a seamless deployment experience for miners and validators.

## Forward Functionality (`forward.py`)
The `forward` function is the core component of the HIP subnet's validator. It orchestrates the task distribution, consensus establishment, and reward calculation processes. Here's an overview of its main functionality:

 1. Task Generation:
   - The validator retrieves the total number of active miners from the Bittensor metagraph.
   - It divides the miners into groups based on the number of active miners.
   - For each group, the validator generates a task by retrieving random data samples from the centralized database. #TODO (previously websocket)

   ### THIS WILL BE HANDLED BY REST API CALLS. NEED TO IMPLEMENT INTO FORWARD AND NEURON/MINER

 2. Miner Querying:
   - The validator queries each group of miners with their respective task using the Bittensor `Dendrite` class.
   - Miners process the task and provide their evaluations of the human-likeness of the data samples.
   - The validator collects the miner responses and their corresponding weights.

 3. Consensus Establishment:
   - The validator establishes the ground truth for each group based on the miner responses and weights using the `weighted_means_consensus` function.
   - It performs cross-validation by querying each group of miners with the ground truth from the other groups.

 4. Reward Calculation (Insentive):
   - The validator calculates rewards for miners based on their responses and alignment with the established consensus using the `get_rewards` function.
   - It updates the scores of the miners based on the calculated rewards.



## Protocol (`protocol.py`)
The `protocol.py` file defines the communication protocol between the validator and miners. It includes the `HIPProtocol` class, which inherits from `bt.Synapse` and specifies the data structure for exchanging information.

The `HIPProtocol` class contains the following fields:
- `data`: The task data that needs to be evaluated for human-likeness.
- `uid`: The unique identifier of the miner.
- `response`: The miner's response indicating the evaluated human-likeness of the data.
- `consensus`: The established consensus on the human-likeness of the data.
- `weights`: The weights assigned to each miner's response.

The `HIPProtocol` class includes `serialize` and `deserialize` methods for converting the protocol instance to and from bytes for network transmission.

## Front-facing Interface
To provide a user-friendly experience for miners and validators, the HIP subnet plans to integrate a front-facing interface using React and Next.js. The interface will communicate with the subnet through a REST API.

The front-facing interface will offer the following features:

 1. User Authentication:
   - Miners and validators will be able to create accounts and authenticate themselves securely.
   - Authentication will be handled using industry-standard practices, such as JWT (JSON Web Tokens).

 2. Task Presentation:
   - The interface will present the data samples to be evaluated in a clear and intuitive manner.
   - Miners will be able to provide their evaluations of the human-likeness of the data using predefined options (e.g., "Very Human-like," "Somewhat Human-like," "Not Human-like," "Unsure").

 3. Reward Tracking (Future Release):
   - Miners and validators will have access to a dashboard that displays their earned rewards.
   - The dashboard will provide a breakdown of rewards earned for each task and overall performance metrics.

 4. User Deployment Simplification:
   - The front-facing interface will offer a streamlined deployment process for miners and validators.
   - Miners and validators will be able to deploy their nodes with a single click on github with railway intergration, eliminating the need for complex setup procedures.
   - The interface will interact with the centralized database on Railway.app to manage node configurations and settings.

## Database Integration (Railway.app)
The HIP subnet will integrate with a centralized database hosted on Railway.app to store and retrieve data samples for evaluation. The database will be accessed using a RESTapi, which will establish a connection to the Railway.app server. The database integration is for storage and retrieval of data samples, ensuring a smooth flow of tasks to the miners for evaluation.

## DEVELOPMENT

### Code Review:
`Task`: Code Review and Security recommendations:

`Description`: A code review and security recommendations for implementing features that aline with the Bittensor networks goals. Functionality tests and recommendations. 
- Review the code for the communication protocol between validators and miners. Ensure that the protocol is well-defined, efficient, and secure. 
- Check that the serialization and deserialization methods are implemented correctly and efficiently. 
- Ensure that the miner logic is correct, efficient, and aligns with the Bittensor network. 
- Verify that the Validator class inherits from the appropriate base class and initializes correctly.
- Check that the forward function orchestrates the task distribution, consensus establishment, and reward calculation processes effectively.
- Verify that the reward function calculates rewards based on the specified criteria and ground truth.
- Check that the weighted_means_consensus function accurately determines the consensus based on miner responses and weights.
- Provide feedback on any potential improvements or gaps in the subnet.


# PROPOSED SLEEPING MINER INSENTIVE MECHANISM

In a typical scenario, miners in the HIP subnet actively evaluate the human-likeness of task data and provide their responses to the validators. However, there will be situations where some miners are temporarily unavailable or asleep, which means they cannot perform the evaluation tasks assigned to them.

To address this issue, the perceptron sleeping miner feature is introduced. It involves training a perceptron model to predict the responses of sleeping miners based on historical data and the current task data.

Here's a brief overview of how the perceptron sleeping miner works:

1. Data Collection: Historical data on miner responses and corresponding task data is collected and stored. This data serves as the training dataset for the perceptron model.

2. Perceptron Model Training: The collected data is preprocessed and used to train a perceptron model. The perceptron model learns to predict miner responses based on the input task data.

3. Model Deployment: The trained perceptron model is serialized and distributed to all miners in the HIP subnet. Each miner loads the model and uses it to predict responses when they are asleep.

4. Miner Sleep Status: Miners have the ability to indicate their sleep status (awake or asleep) through the front-facing interface. When a miner is asleep, they do not actively participate in the evaluation tasks.

5. Prediction of Sleeping Miner Responses: When a validator assigns tasks to miners, it checks the sleep status of each miner. For sleeping miners, the validator uses the trained perceptron model to predict their responses based on the current task data.

6. Reward Calculation: The predicted responses from sleeping miners are incorporated into the weighted-means consensus establishment process alongside the actual responses from awake miners. The validators calculate rewards based on the combined responses, taking into account the accuracy of the predicted responses. #TODO: maybe too convoluted, need to simplify.

7. Reward Distribution: Rewards are distributed to both awake and sleeping miners based on their contributions to the subnets process. Sleeping miners receive rewards proportional to the accuracy of their predicted responses.
The perceptron sleeping miner feature aims to increase the inclusivity and fairness of the HIP subnet by allowing miners to earn rewards even when they are temporarily unavailable.

However, it's important to note that the perceptron sleeping miner is a complementary feature and does not replace the active participation of awake miners. The HIP subnet will still rely on the majority of miners being awake and actively evaluating task data to maintain the integrity and accuracy of the consensus process.


### Perceptron Model Development:
Perceptron Integration (for the sleeping miners):
   - If a perceptron model is used for the sleeping insentive mechanism, the validator collects all miner responses and passes them to the inactive miners perceptron model.
   - The perceptron model predicts the final consensus of waking miner responses.
   - Rewards are calculated based on the perceptron's output.
   - Perceptron model can only be used once every 12 hours
   - Design and implement the perceptron model that will be used to predict miner responses.
   - Define the input features and output structure of the perceptron model.
   - Implement the perceptron model using a machine learning framework.
   - Develop a training pipeline that takes the preprocessed data and trains the perceptron model.
   - Implement evaluation metrics to assess the performance of the trained model.
