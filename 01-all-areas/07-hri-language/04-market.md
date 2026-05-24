# The HRI and Robot-Language-Interface Market

> Market intel for our team. Human-Robot Interaction and language
> interfaces for robots is a fast-growing but still-niche area,
> pulled forward since 2023 by the convergence of humanoids and
> LLMs. The companies below are the ecosystem of LLM-grounded
> robot work and conversational UX we operate in. Some are
> potential customers, some are partners we can integrate with,
> some are competitors, some are talent sources for our hires,
> and some are reference points for stack and case studies. Comp
> bands are included so we set our own salaries fairly against
> the market.

## What this file is for

When we pitch a new client on a voice or conversational layer on
top of a robot, we sometimes need to position against the big
names ("we do what Diligent's HRI team does, smaller and on top
of your existing hardware"). When we hire, we benchmark against
NVIDIA Riva / Deepgram / humanoid-startup comp so our offers
don't read as low. When we read CHI / HRI / CoRL papers on
grounded language, half are from teams listed here. This is our
shared map of the landscape.

See also: `01-examples.md` (deployed products and papers),
`05-projects.md` (what we sell), `06-courses.md` (where our team
learns from), `00-basics.md` (concrete agency project patterns
for the HRI / language layer).

## How to read each entry

For each company below: what they do, the tech stack they're
known to use, the TC band our team competes with, the location,
and **what they mean to us** — one of:

- *Potential customer* — their internal teams sometimes hire
  agencies for overflow or specialized work.
- *Partner candidate* — they run a formal partner / reseller /
  inception / agency program we could join.
- *Competitor* — they sell into the same RFPs we do.
- *Talent source / talent risk* — we hire from them; our team
  might leave to them.
- *Reference point* — published work, stack, or case studies we
  study but don't directly compete with.

---

## Big tech HRI and language-action teams

The hyperscalers staffing real teams against grounded language
and robot conversational UX. Mostly *reference points* for
stack and *talent risks* for senior ICs.

- **Google DeepMind Robotics / Gemini Robotics** — the PaLM-E
  and RT-2 lineage, now folded into Gemini Robotics (announced
  2024-2025). Grounded language to action; instruction-following
  on real arms. Stack: JAX on TPUs, internal eval harnesses,
  PyTorch on the edges. Mountain View + London. Senior IC TC
  $400-700k for research; lower for product.
  *To us:* reference point for VLA-with-language architecture
  and prompt formats; talent risk for senior ML ICs.

- **Microsoft (Project Bonsai, Mixed Reality, AI Frontier
  Labs)** — Bonsai for industrial autonomy with natural-language
  task specs; HoloLens / Mixed Reality for human-side UX with
  robots; the AI Frontiers group has explored LLM-to-robot
  prompting (the "ChatGPT for Robotics" 2023 paper came from
  here). Stack: C# + Python + ONNX. Redmond + global. Senior IC
  $250-400k.
  *To us:* reference point for industrial language-spec
  workflows; **partner candidate** via Microsoft for Startups
  (cloud credits, co-sell motions for Azure AI customers).

- **Apple** — Siri's robotics ambitions are quiet but real
  (home-robot rumors since 2024, internal projects across the
  Vision Products Group and SPG). Voice-first interaction on
  Apple Silicon. Stack: Swift + CoreML + Metal + custom on-
  device speech. Cupertino. Senior IC $300-500k.
  *To us:* reference point for on-device voice UX patterns; no
  realistic partner motion yet.

- **Amazon (Alexa+, Astro, Lab126)** — Astro mobile home robot
  pairs with the Alexa LLM stack (Alexa+ launched 2024). Voice
  intents, multi-turn grounding, basic embodied actions. Lab126
  is the hardware org; Alexa AI is the language org. Stack:
  Java + Python + internal DL frameworks; Amazon L5/L6 bands.
  *To us:* reference point for consumer voice-to-robot UX;
  potential customer for niche Astro / Alexa-skill integration
  work if their internal teams hit overflow (rare and hard to
  reach).

- **NVIDIA (Isaac + GR00T + Riva)** — Isaac and GR00T for the
  embodiment side, Riva for the speech-stack side; the GR00T
  roadmap explicitly includes voice / language. Multiple teams.
  Stack: C++ + PyTorch + CUDA + TensorRT + Riva (gRPC).
  Median TC ~$270k; senior staff $400k+.
  *To us:* **partner candidate** via NVIDIA Inception
  (Riva access, GR00T early access, DGX cloud credits, NVIDIA
  Connect intros); reference point for the on-edge speech stack
  used in field deployments.

---

## Humanoid startups with strong language stacks

The fastest-moving customers and talent destinations for HRI
work. Voice and conversational UX are increasingly first-class
features rather than demos.

- **Figure AI** — Helix VLA explicitly takes voice input;
  marketing materials lead with conversational behavior.
  Sunnyvale. PyTorch + C++ + NVIDIA Isaac internally. Voice /
  speech roles posted intermittently 2024-2025.
  *To us:* talent risk for senior multimodal ICs; reference
  point for voice-conditioned VLA UX.

- **1X Technologies** — NEO consumer humanoid leans heavily on
  conversational features (the household-companion framing).
  Norway + SF. PyTorch + C++. Hires speech and conversational-
  ML engineers explicitly.
  *To us:* reference point for consumer-grade voice UX on a
  humanoid; talent risk in Norway and SF.

- **Apptronik (Apollo)** — public Apollo demos include voice-
  task prompting; partnerships with Google DeepMind announced
  2024 brought language grounding work in-house. Austin TX.
  *To us:* potential customer for industrial voice-UX integration
  if their pilots expand; reference point.

- **Sanctuary AI** — natural-language control demos on Phoenix
  (BC, Canada). Has published on language-to-action grounding.
  Smaller team than Figure / 1X.
  *To us:* reference point; talent source for HRI-leaning ML.

- **Agility Robotics (Digit)** — Digit's conversational /
  operator layer is more industrial (warehouse instruction
  acknowledgment, status reports) than household. Albany OR +
  Pittsburgh. Senior IC $230-380k.
  *To us:* reference point for industrial HRI patterns; potential
  customer for niche operator-UX work.

- **Tesla Optimus** — secretive on the language stack; public
  demos so far focus on manipulation, not voice. PyTorch + custom
  C++. Base lower than peers, equity-heavy.
  *To us:* reference point; not a partner, not a realistic
  customer.

---

## VLA and language-conditioned policy startups

The research-leaning startups where the VLA-meets-language
boundary lives. Most of these treat language as a first-class
policy input, not a separate UX layer.

- **Physical Intelligence (Pi)** — pi0 and pi0.5 take natural-
  language prompts as policy conditioning. $400M Nov 2024 at
  $2.4B. Under 100 total, high talent density. PyTorch + JAX.
  *To us:* reference point for language-conditioned VLA; talent
  risk for senior multimodal ICs.

- **Skild AI** — robot-agnostic generalist policy with language
  conditioning. $300M Series A July 2024 at ~$1.5B. PyTorch.
  Pittsburgh + Bay Area.
  *To us:* reference point.

- **Covariant (pre-Amazon)** — the Brain stack had natural-
  language task specification before most of the current wave;
  most of the team has been absorbed into Amazon Robotics as of
  2024-2025.
  *To us:* reference point for what mature warehouse language-
  grounding looked like; talent source as ex-Covariant ICs come
  back onto the market.

- **OpenAI Robotics** — the original robotics team was wound
  down in 2021; multiple credible signals through 2024-2025
  suggest a resumed robotics effort. Stack assumed PyTorch +
  internal infra. SF.
  *To us:* reference point only until the team's scope is
  public; potential talent risk if they staff up aggressively.

- **Anthropic** — no robotics product yet, but Claude is used
  by several robotics teams as a planner or reasoning module
  (SayCan-style). Worth tracking only because their model
  releases shift what's possible at the planning layer.
  *To us:* reference point; not a competitor, not a customer.

---

## Voice and speech ecosystem (the building blocks)

The vendors whose APIs and SDKs we actually wire into customer
deployments. This is the layer where partnership programs are
the most concrete and where we get the most leverage.

- **OpenAI (Whisper, Realtime API)** — Whisper is the default
  open-weight ASR baseline; the Realtime API (2024) is the
  default low-latency voice-agent transport. Stack: REST +
  WebSocket. Pricing is metered; no formal robotics partner
  program (hedge: an "API ecosystem partner" tier exists for
  some named partners, but it's not openly application-based).
  *To us:* **default integration target** for voice-agent demos
  and prototypes; reference point for latency budgets.

- **Deepgram** — commercial speech-to-text with strong streaming
  latency and on-prem options. Has a partner / reseller program.
  San Francisco.
  *To us:* **partner candidate** for production STT in customer
  deployments where Whisper latency or compliance doesn't fit.

- **ElevenLabs** — commercial TTS with voice cloning; the
  default high-quality voice output for product demos. Partner
  / affiliate program exists.
  *To us:* **partner candidate** for TTS in customer-facing
  robot voices; reference point for voice-design UX patterns.

- **Cartesia** — newer (2024) low-latency TTS with on-device
  options; positioned against ElevenLabs on latency and edge
  deploy. SF.
  *To us:* reference point and integration target for edge-voice
  deployments where ElevenLabs latency doesn't fit.

- **NVIDIA Riva** — commercial speech stack (ASR + TTS + NMT)
  optimized for edge / Jetson deployment. Available through
  NVIDIA Inception.
  *To us:* **partner candidate** via Inception; default ASR /
  TTS for any deployment already on Jetson hardware.

- **Picovoice** — on-device wake-word, STT, and intent parsing
  for embedded hardware. Vancouver. Has a partner program for
  integrators and a generous free tier.
  *To us:* **partner candidate** for offline / privacy-sensitive
  voice deployments (hospital, elderly-care robots) where cloud
  ASR is a non-starter.

---

## Robotics-specific conversational and NLP startups

The smaller, more directly comparable market. This category is
thin — most "HRI startups" of the 2010s either pivoted or were
absorbed, and the current wave bundles language into broader VLA
or humanoid plays rather than standing it up as a separate
company.

- **Diligent Robotics (Moxi)** — one of the longest-running
  pure-HRI startups; hospital service robot with conversational
  affect. Austin TX. Smaller team; comp closer to mid-startup
  bands ($180-280k).
  *To us:* reference point for healthcare HRI; talent source for
  HRI designers and conversational engineers.

- **Robust.AI (Rodney Brooks)** — Carter collaborative cart with
  explicit HRI focus. Scaled 2023+. Bay Area.
  *To us:* reference point for collaborative-cart HRI patterns;
  potential talent source.

- **Hello Robot (Stretch 3)** — mobile manipulator pitched
  partly on HRI accessibility (assistive use cases). Open SDK,
  research-friendly. Martinez CA.
  *To us:* **integration platform** — their open SDK makes Stretch
  a realistic target for our HRI demos and case studies.

- **Bear Robotics, Pudu, Keenon** — service robots in restaurants
  and hotels. The conversational layer is shallow today (wake
  word + canned responses), but vendors hire HRI-adjacent UX work
  as deployments scale.
  *To us:* potential customers for niche conversational-UX
  upgrades; reference points for service-robot HRI norms.

- **Knightscope** — security patrol robots with basic voice
  interaction. Mountain View CA.
  *To us:* reference point only.

- **Reflexion Robotics** and similar smaller names — appear in
  press but published details are thin; treat as reference points
  only until track record is verifiable.

- **SoftBank Pepper ecosystem** — Pepper is end-of-life as a
  hardware platform but the ecosystem of integrators and
  conversational-content shops that grew around it (2014-2020)
  is partly still active. Most have pivoted to broader
  conversational AI or shut down.
  *To us:* reference point and cautionary case study on
  standalone HRI-startup economics.

---

## Competing HRI and language-interface services shops

Honest assessment: this market is thin. There is no large
established population of "HRI services shops" the way there is
for perception or web dev. Real candidates we'll run into:

- **Voice-UX consultancies that adapted from chatbot work** —
  most haven't crossed into robotics. The few that have (Tangible,
  Tangram Vision's UX side, a handful of design studios) are
  small and OEM-engaged rather than open market.
  *Where we beat them:* robotics-systems depth, ability to wire
  voice into ROS / Isaac stacks rather than only design the UX.

- **Small LLM-application shops** — LlamaIndex consulting
  partners, Cohere implementation partners, and the broader
  pool of LLM-application boutiques. Almost none specialize in
  robotics today.
  *Where we beat them:* robotics context (latency budgets,
  safety constraints, embodied grounding) that pure-software
  LLM shops lack.

- **NVIDIA Inception members focusing on Riva** — a small subset
  of Inception companies position around the Riva speech stack;
  some take agency-style engagements.
  *Where we beat them:* HRI-specific UX patterns rather than
  generic speech-stack integration.

- **Most "HRI services" today is bundled** into broader VLA or
  humanoid-integration engagements rather than sold as a
  standalone offering. This is both our opening (few specialists)
  and our risk (small standalone market).

---

## Partnership programs worth joining

Concrete programs where applying as an agency unlocks credits,
sales co-marketing, or a customer pipeline.

- **OpenAI API + Realtime API ecosystem** — there is no openly
  application-based formal partner program for voice / robotics,
  but named-partner relationships exist for case-study features
  and credit grants. Hedge: build a public Realtime-API robotics
  demo first, then approach.
- **Hugging Face Enterprise Hub / Expert Acceleration Program**
  — partner-tier discounts for our customers; co-marketing on
  customer stories; access to open speech and language model
  weights.
- **NVIDIA Inception** — free DGX cloud credits, NVIDIA Connect
  intros, GR00T and Riva access. Open to AI / robotics shops
  under ~$50M revenue. Apply at nvidia.com/en-us/startups.
- **ElevenLabs Partner / Affiliate Program** — TTS integration
  partner status; rev share on referred enterprise customers.
- **Deepgram Partner Program** — STT integration partner;
  co-selling into enterprise speech deployments.
- **Picovoice Partner Program** — for integrators building on
  the on-device wake-word + STT + intent stack; rev share and
  technical co-marketing.
- **ROS Industrial Consortium** — adjacent to HRI but relevant:
  membership ties us into the integrator community where
  conversational layers on industrial robots get specified.
- **Microsoft for Startups / AWS Activate / Google Cloud for
  Startups** — $25k-$200k of cloud credits available; useful
  for the LLM-inference costs of voice-agent prototyping during
  initial customer engagements.

The realistic high-value ones for an HRI / language services
shop are: NVIDIA Inception (for Riva and GR00T), Hugging Face
Enterprise, and one of Deepgram or ElevenLabs depending on the
deployment shape.

---

## Comp bands (for setting our own salaries)

Approximate TC bands for senior IC (3-7 years), 2025 Bay Area /
NYC. Sources: levels.fyi, 2025 Robotics Salary Guide, public
funding announcements. Startup TC is noisy because it includes
illiquid common shares. HRI / robotics-language roles run
slightly below core ML perception because the named-title
demand is thinner.

- **DeepMind Robotics, OpenAI (research):** $400-700k for senior
  ICs working on grounded language / VLA.
- **Humanoid startups (Figure, 1X, Apptronik) ML + voice:**
  $300-500k, equity-heavy.
- **Specialist NLP-for-robotics (NVIDIA Riva, Amazon Alexa+,
  Microsoft AI Frontiers):** $230-380k.
- **Smaller HRI startups (Diligent, Robust.AI, Hello Robot,
  service-robot vendors):** $180-280k.
- **Speech-stack vendors (Deepgram, ElevenLabs, Cartesia,
  Picovoice):** $200-330k with remote optionality.

Remote / EU usually 20-40% lower; London / Munich close the gap
on the high end.

**For our hires:** band our base salaries at the specialist-NLP
range or above. Below that and our offers read as low against
the speech-vendor market our candidates compare against. Equity-
heavy humanoid startups are not direct comp competitors for our
headcount; their candidates are taking lottery-ticket risk we
can't match.

---

## Hiring market signal

- "HRI Engineer" and "Robotics Language Engineer" are niche
  titles with low search volume on the major job boards
  (LinkedIn, Indeed). Most relevant roles are posted as
  "Conversational AI Engineer," "Speech Engineer," or "Multimodal
  ML Engineer" with robotics in the JD body rather than the
  title.
- From the 2025 Robotics Salary Guide (907 jobs analyzed): the
  Robotics Software Engineer median is $189k; HRI / language
  roles cluster below the median for non-humanoid employers and
  above it at the humanoid startups.
- Hiring volume for HRI-specific titles is small relative to
  perception or VLA; growth direction is up but from a low base.

Translation: a thin but growing specialty. Good for
differentiation, harder to staff against pure-named-title
search.

---

## Remote / hybrid posture by employer type

Useful for understanding which talent pools are accessible to us
(remote-friendly = larger candidate pool for our remote hires).

- **Big-tech research (DeepMind, Microsoft AI Frontiers, Amazon
  Alexa AI):** hybrid 3 days on-site; some research roles flex.
- **Humanoid startups (Figure, 1X, Apptronik, Sanctuary,
  Agility):** strictly on-site.
- **VLA startups (Physical Intelligence, Skild):** mostly
  on-site for ML; some remote for infra.
- **Speech vendors (Deepgram, ElevenLabs, Cartesia, Picovoice):**
  largely remote-friendly, globally distributed. Our biggest
  direct competitors for distributed-team voice talent.
- **Smaller HRI startups (Diligent, Robust.AI, Hello Robot):**
  mostly on-site in their respective cities.
- **Service-robot vendors (Bear, Pudu, Keenon, Knightscope):**
  on-site, often outside major tech hubs.

---

## Title decoder

The same role carries multiple names across companies. Use this
when reading job ads (competitor signaling) or when writing our
own postings.

- **HRI Engineer** — explicit but rare title (Diligent,
  Robust.AI, academic spinouts). Owns the human-side interaction
  loop end-to-end.
- **Conversational AI Engineer** — most common title for
  voice-agent work (Amazon Alexa, Microsoft, speech vendors,
  some humanoid startups). LLM + dialogue management focus.
- **Speech Engineer** — ASR / TTS specialty (NVIDIA Riva,
  Deepgram, ElevenLabs, Picovoice, Apple Siri). Signal-
  processing-leaning.
- **Robotics NLP Engineer** — niche title used at a few research
  labs and humanoid startups; grounded-language focus.
- **Voice UX Designer** — design-side counterpart, more common
  in consumer-voice teams than robotics; we hire this skill
  when shipping customer-facing robot voices.
- **VLA Engineer** — overlaps significantly with HRI when the
  VLA takes language conditioning (Pi, Skild, Figure Helix,
  Gemini Robotics). Owns model and training; the HRI / UX layer
  is usually separate.
- **Multimodal ML Engineer** — umbrella title (DeepMind, FAIR,
  OpenAI, humanoid startups). Vision + language + sometimes
  audio, trains and evaluates models.

---

## What this means for our positioning

Three short takeaways for the team:

1. **HRI services as a standalone offering is currently thin.**
   The standalone HRI startups of the 2010s mostly didn't make
   it; the current wave bundles language into VLA or humanoid
   plays. Better to position the conversational layer as a
   value-add on top of a manipulation or humanoid-integration
   engagement rather than as the lead offer.
2. **Specialize the conversational layer for a specific
   vertical.** Elderly-care companion robots, hospital service
   robots, restaurant / hospitality service robots, and
   industrial operator interfaces each have distinct UX
   constraints (privacy, latency, language coverage, safety
   acknowledgment) and willing buyers. Pick one and own it
   rather than pitching generic HRI.
3. **The leverage is in the speech-stack partnerships.** NVIDIA
   Inception (for Riva and GR00T), Deepgram or ElevenLabs or
   Picovoice (depending on deployment shape), and Hugging Face
   Enterprise. Joining these early matters more than a
   marketing budget for this specialty.
