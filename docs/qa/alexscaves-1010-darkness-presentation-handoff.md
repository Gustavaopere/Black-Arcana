# Darkness / presentation boundaries — discovery handoff (Alex's Caves Continued 1.0.10)

**State:** 🟡 discovery in progress; no static certification, no gameplay mutation, no physical QA. Source of authority: modlist sibling `neoforge-rpg-skilltree`, installed name `alexscaves-1.0.10-neoforge+1.21.1.jar`. Exact publisher JAR 75,279,314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.

Continuation from the merged PR #1134, `main@ca66c855d8d8c466f8c10c6113e2bf4429edaf73`: 105/105 individual static contracts in the observed catalog, not proof of the complete provider universe. New candidate family: `CustomArmorPostRender`, `CustomTabBehavior` and Darkness-related objects. A prior Codex screenshot reports presentation-only interfaces and an Apple/armor Darkness effect, but exact class names, owners and behavior require verifying the installed JAR before a new static certification.

## Capture procedure

CI runs `docs/qa/alexscaves_1010_darkness_presentation_probe.py` against the publisher SHA-exact JAR, enumerates 1,555 classfiles, seals both interface identities and typed implementers/consumers, enumerates Darkness/Apple/Hood/Cloak class candidates and resource paths, and archives bounded full `javap -p -c -v -s` transcripts. Full bytecode is a temporary CI artifact; no third-party implementation is copied into the repo.

## Status and next decision

- Interfaces may be **technical support/presentation components** and do not automatically count as independent magical roots.
- The two possible gear pieces and the apple effect must be separated by item identity, registry binding, owner, duration, amplifier, durability/charge, persistence and exact downstream consumption.
- Static observations never prove accepted effects, packet authority, claim/PvP behavior, or a safe hook. Mutations remain `NO_MUTATION`; mutating hook `NOT_VERIFIED`; physical QA `NOT_TESTED`; provider universe `OPEN`.
- Add object-specific technical cards and update all alphabetical indexes only after the evidence confirms the actual IDs and method contracts. No counter promotion from class-name discovery alone.

## Consolidação de evidências

Após a auditoria ampliada do run [44864573972](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44864573972), 18 transcrições de classes e 17 recursos JSON foram capturados. O [manifesto SHA-exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DARKNESS-PRESENTATION-DISCOVERY-1.0.10.json) registra hashes, as duas interfaces de apresentação e seus consumidores; as três [fichas de itens](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/items/INDEX.md) são ⚠️ parciais. O único efeito e cast Darkness Incarnate já consta do catálogo anterior; não houve nova raiz. O verificador de métodos/consumers confirma apenas caminhos estáticos, sem QA, hook ou mutação.
