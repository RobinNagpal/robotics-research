# How to Get Started

## Week 1-2: Voice + LLM loop on your laptop

- Build a local stack: Whisper-cpp (ASR) -> Llama-3.1-8B or Claude API
  (LLM) -> Piper (TTS). Wrap in a Python service with FastAPI.
- Add VAD and barge-in so the user can interrupt the robot.

## Week 3-4: LLM as task planner

- Re-implement SayCan in simulation (Habitat or Robosuite + RoboCasa).
- Implement Code-as-Policies: LLM emits Python that calls a small robot
  API surface; run it in a sim.

## Week 5: Grounded perception

- Wire in Grounding DINO + SAM 2 so "pick up the red mug on the left"
  resolves to a 2D box -> 3D point.
- Combine with a simple pick policy (Diffusion Policy or VLA from the
  robot-learning-vla folder).

## Week 6: Human-aware motion

- Stand up a Nav2 robot in Gazebo with simulated pedestrians.
- Implement a social cost layer (Social-LSTM-style prediction +
  proxemics zones).

## Week 7-8: Real HRI demo

- Hook the voice loop, planner, and grounded perception together on a
  cheap arm (SO-100) or in sim.
- Record a 2-minute video: "open the drawer, take out the red marker,
  hand it to me." This is your portfolio piece.

## Datasets and sims

Habitat 3.0 (social nav), iGibson, RoboCasa, AI2-THOR, RH20T
(real-human-teleop), CMU Panoptic, ALOHA + Aloha-Sim.

## Communities

ACM/IEEE **HRI** conference (the flagship), CHI for the HCI side,
CoRL/RSS for embodied LLM work; r/robotics; LeRobot Discord.
