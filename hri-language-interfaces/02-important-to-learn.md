# Important Things to Learn

## LLM + agent foundations

- Prompt engineering, structured output (JSON schema, tool calling).
- Tool use / function calling patterns (Anthropic, OpenAI, Gemini).
- Retrieval-augmented generation (RAG) for task knowledge.
- Local LLM inference: llama.cpp, vLLM, MLC, Ollama.
- Latency budgets — sub-500 ms ASR+LLM+TTS pipelines.

## Speech and audio

- ASR: Whisper, Distil-Whisper, NVIDIA Parakeet, Moonshine.
- VAD (voice activity detection): Silero, WebRTC VAD.
- TTS: Piper, XTTS-v2, ElevenLabs, Sesame CSM.
- Speaker diarization, wake-word detection.

## Multimodal perception of humans

- Pose: MediaPipe, OpenPose, BlazePose, ViTPose.
- Gaze / face: MediaPipe FaceMesh, gaze estimation models.
- Hands and gestures: MediaPipe Hands, HaMeR.
- Emotion / affect: AffectNet-trained classifiers; use sparingly,
  ethically-fraught.

## Planning and grounding

- Task and motion planning (TAMP): PDDL, OpenRAVE-style integrations.
- LLM-as-planner: SayCan, Code-as-Policies, ProgPrompt patterns.
- Grounding: VLMs (LLaVA, PaliGemma) + open-vocabulary detectors
  (Grounding DINO, OWL-ViT, YOLO-World).

## Safety, trust, and social signaling

- Safe motion around humans (speed scaling, ISO 10218 / ISO/TS 15066).
- Legibility / predictability of motion (Dragan, Srinivasa).
- Proxemics, gaze cues, intent signaling lights/sounds.

## Tools

ROS2 + rclpy, LangChain / LangGraph (cautious use), Whisper-server,
Piper, MediaPipe, Foxglove for HRI logging.

## Must-read papers

SayCan, Code-as-Policies, Inner Monologue, VoxPoser, TidyBot,
"Legibility and Predictability of Robot Motion" (Dragan), "Effects of
Robot Gaze" (Mutlu et al.).
