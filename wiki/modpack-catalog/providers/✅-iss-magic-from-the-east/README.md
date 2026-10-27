# ISS: Magic From The East — provider canônico

**Checkpoint histórico de identidade (2026-10-13):** ✅ [22/22 registros estáticos](EXACT-BINARY-SPELLS-1.1.5.md), [Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162) **SUCCESS**; CurseForge file `7385201`, **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0` = JAR da modlist física #346. `MFTESpellRegistries` tem **11 Symmetry + 11 Spirit**, classes e IDs literais verificados sem branches; `ISS_MagicFromTheEast` liga o registrar no bootstrap. **COUNTED_EXACT** apenas para registro binário: **20/39 exatos / 19/39 pendentes**, **+0** raízes, mínimos **1857 global / 1855 escopo**. Fonte de parâmetros, runtime, Iron's 3.16.3, configuração e Survival continuam ⚠️. O workflow de auditoria fica fora da `main`.


## Estado atual — 27/10/2026

**Fichas source-causais reconciliadas: 22/22 spells observadas.**
**Barra editorial deste lote:** `████████████████████ 100.0%`
**Certificação técnica estrita MFTE: 0/22.** `░░░░░░░░░░░░░░░░░░░░ 0.0%`
**Recorte certificado global: 138/2075 fichas observadas.** `█░░░░░░░░░░░░░░░░░░░ 6.7%`
**Providers integralmente certificados: 0/164.** O universo de todo o conteúdo integrável permanece aberto; 22 spells não fecham atributos, equipamentos e demais sistemas do mod.

Os 100% editoriais medem as fichas deste lote, não execução de perks, equivalência integral source↔JAR ou aceite no jogo. Ver [índice estrito](INDEX.md), [painel global](../INDEX.md) e [progresso por mod](../../meta/PROGRESSO-CATALOGO-ATUAL.md).

- **Mod ID:** `iss_magicfromtheeast`.
- **JAR:** `iss_magicfromtheeast-1.1.5.jar`, 1680780 bytes, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`, publicação CurseForge `7385201`, mesmo hash do registro físico histórico #346.
- **Fonte candidata:** `WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`, **RELEASE_BOUNDED_SOURCE**. A fonte posterior `13208302c9fdf5beb171a328558cbef07a25ba46` deixa de ser a referência geral do comportamento instalado.
- **Build da fonte candidata:** MC 1.21.1, NeoForge 21.1.187, Iron’s 3.14.8; **pack de referência:** NeoForge 21.1.250, Iron’s 3.16.3.
- **Proveniência e diferenças:** [reconciliação da release](RELEASE-SOURCE-RECONCILIATION-1.1.5.md).
- **Contratos de eventos, fórmulas herdadas e integração:** [limites comuns para perks](SPELL-PERK-BOUNDARIES-1.1.5.md).
- **Achados e testes pendentes:** [auditoria técnica](TECHNICAL-AUDIT.md).

## As 22 fichas

[Symmetry](symmetry/README.md) tem 11 spells: Sword Dance, Bagua Array Circle, Dragon Glide, Jade Judgement, Jiangshi Invoke, Underworld Aid, Punishing Heaven, Drapes of Reflection, Cloud Ride, Nephrite Slash e Jade Bullet. [Índice das fichas](symmetry/INDEX.md).

[Spirit](spirit/README.md) tem 11 spells: Soul Catalyst, Soul Burst, Spirit Challenging, Bone Hands, Calamity Cut, Kitsune Pack, Revenant of Honor, Ashigaru Squad, Phantom Charge, Anchoring Kunai e Splitting Shuriken. [Índice das fichas](spirit/INDEX.md).

Cada ficha distingue identidade binária, fórmulas da fonte candidata, parâmetros do host, consumidores de dano/área/estado, geometria e hitbox, custos/cooldowns, lifecycle, limites de mutação e casos de QA. Projéteis, efeitos, summons e callbacks filhos não acrescentam novas identidades.

`LaunchSpell` e `QigongControllingSpell` estão comentadas no registry candidato e ausentes das inscrições ativas comprovadas. **Dune está registrada como escola no JAR**, com zero spells no roster das 22. A declaração antiga de que a escola estava comentada vinha de uma fonte posterior divergente.

## Autoria e integração

MFTE/Iron’s continuam donos de suas magias, mana, efeitos, summons e cleanup. Black Arcana mantém seu runtime e política de mundo; RPG Skill Tree mantém progressão/Mastery/perks/gates; Enshrouded mantém seus próprios sistemas. A escola custom não é automaticamente uma lane Mastery aceita ou um DamageType reconhecido pelo Enshrouded. Ausência de hook real mantém a alteração bloqueada; não substituir por cast ou dano paralelo.

Consulta factual e paráfrases com permalinks, sem importar código/assets do provider. Todos os testes físicos e adapters permanecem condicionados; nenhum Stage foi promovido.
