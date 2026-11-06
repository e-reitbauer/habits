---
id: openspec
title: OpenSpec
markers: ["openspec/specs", "*/openspec/specs", "*/*/openspec/specs"]
commands: ["openspec"]
script: openspec.py
---
This project uses OpenSpec. Its specs replace a CLAUDE.md as the source of truth for architecture, conventions and behaviour.
- Before changing code, read the spec(s) for the area the task touches.
- Treat requirements as constraints. If a request contradicts a spec, say so before coding and suggest a change proposal instead of silently diverging.
- Changes to specified behaviour go through an OpenSpec change (/opsx:propose, then /opsx:apply and /opsx:archive, or the openspec CLI). Never edit the main specs directly. Small fixes within existing requirements need no proposal.
- For a large or unclear change, load the `research` skill before proposing: specs first, code only for what they don't answer, then /opsx:explore to weigh options. Record the alternatives considered in the change's design.md.
- To continue an active change, use /opsx:apply.
- Facts an agent can't infer from the code (how to run the app, devices, environments) belong in the root's config.yaml `context`. When you discover one, suggest adding it there.
