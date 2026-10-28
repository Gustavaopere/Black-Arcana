# Acolyte 1.0.3 — catálogo técnico

Acolyte acrescenta NPCs, IA, recrutamento, equipamentos, comércio e encontros sobre Iron's. **0 spells standalone próprios; +0 novas identidades de magia no ledger semântico.** Seus sistemas têm contratos integráveis e não são classificados como um provider sem conteúdo apenas por não registrar `AbstractSpell`.

## Evidência e escopo

O artefato publisher `acolyte-1.0.3.jar`, CurseForge projeto/file `1534642 / 8098233`, tem 621837 bytes, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275` e SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`. O Modrinth `S1u5j9dB / r0BSsxdc` confirma o mesmo release/hash.

O catálogo de interoperabilidade examina **359 arquivos dentro de 469 entradas ZIP**, incluindo **93 classes (66 externas e 27 internas)**. Referências de código identificam classes, métodos/descriptors e offsets PC do binário. Não foi identificada fonte oficial vinculada pelos publishers; não se presume uma revisão Git.

O índice físico sibling conserva o filename/runtime instalado `1.0.3`, mas não fornece hash independente da cópia local. **Igualdade publisher↔instalado não comprovada.** A declaração embarcada MIT conflita com ARR dos projetos oficiais. [Proveniência, reprodução e limites](BINARY-CONTRACTS-1.0.3.md).

## Conteúdo útil para perks e sistemas

| Frente | Contratos documentados |
|---|---|
| [Entidades](entities/INDEX.md) | Seis papéis human/demon, Horn Merchant e Lieutenant; atributos, casting e ciclos de vida. Bases compartilhadas não são registros extras. |
| [Goals](goals/INDEX.md) | Alvo, distâncias, movimento, melee/ranged, casting single-use e ordens. |
| [Perfis](profiles/INDEX.md) | Seis pools de archetype, 50 entradas com stats, pesos, spells e equipamento; skins de bioma não criam pools novos. |
| [Sistemas](systems/INDEX.md) | Recrutamento/owner/NBT, emeralds, payload C2S/menu, archetype/reload e cinco gamerules. |
| [Itens](items/INDEX.md) | Dois horns consumíveis, quatro formas vestíveis, 15 peças de armadura e dez eggs; slots, efeitos e brewing. |
| [Economia](economy/INDEX.md) | Contratos de ofertas, moedas, seleção aleatória, limites e delegações ao host. |
| [Encontros](encounters/INDEX.md) | Marcadores, spawning e 18 superfícies de estruturas/tavernas, com dados e aquisição. |
| [Configuração](config/INDEX.md) | Knobs existentes e seu consumo; specs vazias explicitamente delimitadas. |

As [31 referências explícitas a spells Iron's](EXACT-1.0.3-HOST-SPELL-REFERENCES.md) permanecem sob Iron's. A seleção dinâmica e os datapacks impedem usar essa lista como limite universal dos spells que NPCs podem conjurar. Não contar os mesmos spells novamente sob Acolyte.

## Fechamento documental e gates

O [manifesto](ARTIFACT-CATALOG-MANIFEST-1.0.3.json) associa todos os arquivos do artefato a fichas ou a suporte justificado e fixa os hashes das fichas. A [prova de fechamento](ARTIFACT-CATALOG-CLOSURE-1.0.3.md) estabelece o escopo publisher; o [índice](INDEX.md) distingue essa barra de documentação da certificação de perks.

`CATALOG_PUBLISHER_ARTIFACT_SCOPE_ONLY`: **`installed_artifact_identity=NOT_VERIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.** O ledger de certificações não é promovido. Valores de atributo ou limiares de IA não equivalem a dano final, range/cooldown do spell ou hook seguro de perk.

Permanecem pendentes host Iron's 3.16.3/NeoForge físico, configurações efetivas, boot e comportamento representativo, cliente/multiplayer, autorização do recrutamento, persistência, loot/trades, proteção de mundo e processamento exatamente uma vez. Os testes CI de Black Arcana não substituem QA física de Acolyte.

Acolyte mantém autoridade sobre seus NPCs, recrutamento, comércio e encontros. Iron's controla spells/casting/mana/cooldown nativos; RPG Skill Tree controla progressão por contrato; Black Arcana mantém casting, Corruption, Strain, Arcane Danger e WorldEffectPolicy próprios. Nenhum runtime, Stage, perk ou adapter foi alterado por esta catalogação.
