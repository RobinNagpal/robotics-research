# Four Projects You Can Build and Sell

## 1. Voice frontend SDK for OEM robots (~3 weeks)

Drop-in package: Whisper / Distil-Whisper ASR + a configurable LLM
backend + Piper / ElevenLabs TTS + ROS2 / gRPC adapters. Includes
wake-word, barge-in, function-calling schema, and an offline mode.

- **Buyers:** robot OEMs (AMRs, service robots, drones) without an audio
  team.
- **Pricing:** $25-100k licensing per OEM model; recurring per-unit fee.

## 2. Natural-language warehouse task router (~4 weeks)

A floor manager types or speaks: "pick all bin 17 items first, then
restock aisle 4." Your service translates to MES/WMS API calls and
fleet directives via an LLM + structured schema.

- **Stack:** Claude / GPT with tool calling, RAG over the customer's
  WMS docs, voice UI, audit log.
- **Buyers:** mid-tier 3PLs without expensive WES software.
- **Pricing:** $2-10k/mo SaaS + integration fees.

## 3. Robot tour guide / receptionist kit (~3 weeks)

Plug-and-play software for Spot, Stretch 3, or a Pepper-class robot:
takes a PDF / website about a venue, builds a RAG index, runs a
voice + face-aware tour guide with wave-to-stop, gaze-following, and a
"follow me" mode.

- **Stack:** Whisper, Llama / Claude, MediaPipe face/pose, ROS2 Nav2.
- **Buyers:** museums, corporate lobbies, hotels, real-estate showrooms.
- **Pricing:** $5-20k installation + $500-2k/mo support.

## 4. Human-aware social-nav layer for AMRs (~4 weeks)

A ROS2 plugin for Nav2 that adds: pedestrian intent prediction
(Trajectron++-style), proxemics-aware cost layers, gaze-aware yielding,
and audible / light intent signaling.

- **Stack:** Trajectron++ or a custom transformer predictor, Nav2 custom
  costmap layer, lightlbar driver.
- **Buyers:** AMR vendors expanding from warehouses into hospitals,
  airports, and retail.
- **Pricing:** $15-50k integration; recurring license per fleet.
