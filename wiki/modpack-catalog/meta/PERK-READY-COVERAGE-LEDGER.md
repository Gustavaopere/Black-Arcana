# Cobertura global de dossiês técnicos para perks — base rastreável

**Fonte:** árvore `Gustavaopere/Black-Arcana/main@465593694120c80db576344fc51de0d52d68d541`; auditoria estrutural de arquivos Markdown sob `wiki/modpack-catalog/providers/`, 2026-10-13.

- Diretórios com Markdown: **165**.
- Arquivos `.md` em providers: **2899**.
- **Isto não significa 2899 feitiços**: inclui índices, metadados, auditorias, arquivos de suporte, guias e objetos com classificação condicional.
- A meta é que **cada ficha real de objeto mágico** contenha o dossiê definido em [PERK-READY-TECHNICAL-STANDARD.md](PERK-READY-TECHNICAL-STANDARD.md); arquivos agregados ficam como índices ou provas.
- O Iron's base possui **110/110 fichas com anotações técnicas source-pinned integradas** pelo [PR #795](https://github.com/Gustavaopere/Black-Arcana/pull/795) em `main@c8ff878c8aab96bd546e4beb4d62ea08e94c5f94`. Isso **não** homologa 110 auditorias causais completas, hooks de perks, adapters ou QA provider-real. Os **2899** arquivos e **165** diretórios acima continuam sendo medidas históricas da baseline de 13/10, não uma nova contagem de magia.
- O Apprentice's Codex 0.9.7.1 possui 83 fichas de spells previamente source-catalogadas. Nesta branch, as **83/83 fichas receberam localizadores exatos** de classe/registro; seis tiveram rastreio causal específico (Higanbana, Blood Brand, Mist Form, Arcane Blast, Thermal Process, Echo Cast). É localização source-pinned, não prova de hooks ou runtime.
- Este inventário **não** modifica o estado de catalogação semântica vigente (mínimos 1857 global / 1855 escopo) nem a campanha de prova binária 25/39.

## Convenção de acompanhamento

A terceira coluna indica **a situação incremental nesta branch a partir da baseline da `main`**, não diz que o provider esteja ❌ não catalogado. Os registros podem já possuir valores/fórmulas validados por outras auditorias: esses dados devem ser aproveitados e os gaps calculados arquivo a arquivo. Conferência de completude por provider requer filtrar fichas de identidade semântica e validar prova por campo; uma quantidade de Markdown não substitui essa operação.

| Diretório do provider | Arquivos `.md` na `main` baseline | Gaps de dossiê técnico |
|---|---:|---|
| `✅-a-good-place` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-aces-spell-utils` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-acolyte` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-aeromancy-additions` | 16 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-alexs-caves-continued` | 13 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-alexs-mobs-continued` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-alshanex-familiars` | 20 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apokinetics` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apotheosis` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apotheotic-creation` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-attributes` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-compat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-compats` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-enchanting` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apothic-spawners` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-apprentice-codex` | 101 | ✅ 83/83 source-catalogadas + 83/83 callsites de registry confirmados no JAR exato; 🟡 83/83 dossiês causais documentados; ⚠️ método/config/Survival/5 casos provider-real PENDING; ⛔ RPG perk adapter |
| `✅-ars-additions` | 48 | ✅ 5/5 magias/rituais (3 glyphs, 2 rituals) com cadeia e source exato; ⚠️ compatibilidade host/config/QA; ⛔ adapter RPG |
| `✅-ars-controle` | 25 | ✅ 9/9 glyphs com source 1.6.16 causal exato; ⚠️ runtime/concurrency/scheduler; ⛔ perk adapter RPG |
| `✅-ars-creo` | 14 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-elemancy` | 11 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-elemental` | 59 | ✅ 47/47 objetos core (23 effects, 2 methods, 2 propagators, 12 filtros, 8 rituais) com dossiês source-located; ⚠️ config/QA; ⛔ adapter RPG |
| `✅-ars-hex` | 10 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-morph` | 7 | ✅ 1/1 glyph Morph com dossiê standalone source 2.0.0; ⚠️ host Identity2/current runtime; ⛔ adapter RPG |
| `✅-ars-n-spells` | 15 | ✅ 5/5 rituais com IDs binários 3.3.4 e métodos source 3.3.3; ⚠️ semântica método/JAR 3.3.4; ⛔ adapter RPG |
| `✅-ars-nouveau` | 149 | ✅ 85/85 glyph parts (5 Forms, 67 Effects, 13 Augments) + 24/24 rituais com dossiê source-located; ⚠️ runtime/hooks/QA e ⛔ adapter RPG não validados; eventos públicos reais source-pinned, adapter RPG e QA pendentes |
| `✅-ars-polymorphia` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-sable` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-sophisticated-compat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-technica` | 8 | ✅ 11/11 objetos (10 effects + 1 augment) em 11 fichas novas com source 2.7.6; ⚠️ Ars/Create host/QA; ⛔ perk adapter RPG |
| `✅-ars-two-way-portals` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-zero` | 24 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-arsdelight` | 6 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-artifacts` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-asterism-arcanum` | 18 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-backported-spellbooks` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-betterend` | 53 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-betternether` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-bloodlines` | 39 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-born-in-chaos` | 21 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-bosses-of-mass-destruction` | 9 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-bosses-rise` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-cataclysm` | 31 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-cataclysm-spellbooks` | 67 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-cold-sweat` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-companions` | 13 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-corail-tombstone` | 30 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-chromatic-return` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-cold-sweat` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-deep-dark` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-dragons-plus` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-dreams-n-desires` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-enchantable-machinery` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-enchantment-industry` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-enchantment-industry-plus` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-ender-transmission` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-fantasizing-again` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-mechanical-companion` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-mechanical-spawner` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-mobile-packages` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-more-automation` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-more-features` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-teleporters-remastered` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-create-wizardry` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-creating-space` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-crystal-chronicles` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-deeper-and-darker` | 17 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-deeper-and-darker-spellbooks` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dimensional-sable` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dis-enchanting-table` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-discerning-the-eldritch` | 32 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dragon-care` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dreamless-spells` | 10 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dungeons-delight` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-dynamic-rpg-resource-bars` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-efiscompat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-eidolon-repraised` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-emf-compat-iron-spells` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-enchantment-descriptions` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-enders-spells-and-stuff-requiem` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-epic-fight` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-familiarslib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-fantasy-armor` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-farmers-spell` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-fires-ender-expansion` | 15 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-gaze` | 34 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-goety` | 375 | ⚠️ 2 Focuses com boundary técnico e bloqueio explícito; código exato pendente |
| `✅-goety-cataclysm` | 60 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-goety-iron` | 23 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-grapplemod-skybound` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-gtbcs-geomancy-plus` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-gtbcs-spelllib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-hazen-n-stuff` | 41 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-hazentouvelib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-hexalia` | 53 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ice-and-fire-ce` | 16 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ice-and-fire-dread-land` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ignis-soulfires` | 12 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ignis-soulfires-spellbooks` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-immersive-portal-irons-spells-addon` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-immersive-portals-true-immersion` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-integrated-villages` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-apothic` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-gems-n-jewelry` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-lib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-spellbooks-kubejs` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-spells` | 150 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-irons-spells-recolor` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ironsable` | 13 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ironsable-x-winds-spellbooks` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-iss-magic-from-the-east` | 27 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-kubejs-ars-nouveau` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-legendary-monsters` | 26 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-legendary-spellbooks` | 33 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-leyline-spellbooks` | 21 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-malum` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-mobstein` | 78 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-monsters-spellbooks` | 6 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-more-relics` | 65 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-mowzies-cataclysm` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-mowzies-mobs` | 17 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-northstar-redux` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-not-enough-glyphs` | 49 | ✅ 40/40 fichas source-located (39 source-enabled condicionais + Momentum disabled); ⚠️ config SERVER/bytecode/QA; ⛔ RPG perk adapter |
| `✅-ozymandias-sundries` | 6 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-paladin-spells` | 9 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-photon` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pickable-orbs` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-portable-hole` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-protection-pixel` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pufferfishs-attributes` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pufferfishs-skills` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-pufferfishs-unofficial-additions` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-relics` | 45 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-ars-nouveau` | 21 | ✅ 19/19 habilidades com dossiês source-located 0.8.1 e identidades estáticas físico-exatas; ⚠️ config/bytecode de métodos/QA; ⛔ RPG perk adapter |
| `✅-reliquified-artifacts` | 55 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-irons-spells-n-spellbooks` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-l-enders-cataclysm` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-reliquified-lenders-cataclysm-new-relics-fix` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-runiclib` | 2 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-shadowsz` | 16 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-simply-more` | 28 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-simply-swords` | 71 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-simply-swords-cataclysm` | 9 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-sky-aesthetics` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-snow-real-magic` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-somake-spells` | 178 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-soul-fire-d` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-spell-actionbar` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-spell-codex-specs` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-starbunclemania` | 5 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-toxony` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-traveloptics` | 61 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-tunes-n-tomes` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampire-spells-addon` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampiric-ageing` | 24 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampirism` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-vampirism-integrations` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-waystones` | 9 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-weapons-of-miracles` | 18 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-werewolves` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-winds-spellbooks` | 11 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-woodwalkers-spellbooks` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ypsilons-fundamentalism` | 26 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-yungs-better-end-island` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-yungs-better-witch-huts` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `README.md` | 1 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |

## Ars Nouveau — checkpoint 2026-10-13

**85/85 Glyph Parts** e **24/24 rituais** com mapeamento de perks/cadeia causal source-pinned nesta branch; sendo 5 Forms, 67 Effects, 13 Augments e 24 rituais. [Matriz técnica Ars 5.13.1](../providers/✅-ars-nouveau/PERK-ENGINEERING-MATRIX-5.13.1.md) com métodos, fórmulas, provas auxiliares e bloqueios. [Eventos reais do Ars 5.13.1](../providers/✅-ars-nouveau/VERIFIED-EVENT-SURFACES-5.13.1.md) foram localizados, mas não constituem adapter implementado. A cobertura semântica de identidade preexistente é diferente da profundidade técnica para perks. **✅ source-located** nesta branch não implica **✅ adapter implementado**, **✅ QA**, **✅ hooks em todos os efeitos** ou merge na main.

## Continuação — Ars Additions e Ars Elemental 2026-10-13

- ✅ [Ars Additions 21.3.0](../providers/✅-ars-additions/PERK-ENGINEERING-MATRIX-21.3.0.md): 5/5 objetos de magias/rituais com métodos source-pinned, fórmulas e limites de perks. Fonte é 21.3.0; build baseline publica Ars 5.11.2, pack usa host 5.13.1 — compatibilidade ⚠️.
- ✅ [Ars Elemental 0.7.10.1](../providers/✅-ars-elemental/PERK-ENGINEERING-MATRIX-0.7.10.1.md): 47/47 objetos (39 Glyph Parts + 8 Rituals) com classes source-pinned e dossiês por ficha. ID no JAR físico foi comprovado anteriormente; igualdade entre implementação do source pin e JAR não foi provada.
- Este lote é +0 no denominador semântico; mantém mínimos 1857 global / 1855 escopo e 25/39 providers com prova binária. Nenhum teste de runtime/CI/Survival, adapter RPG, merge ou promoção de Stage por este lote.

## Continuação — Ars Controle e Ars Technica (2026-10-13)

- ✅ [Ars Controle 1.6.16](../providers/✅-ars-controle/PERK-ENGINEERING-MATRIX-1.6.16.md): 9/9 glifos existentes receberam source pin da release e detalhes de parser, efeitos de Delay, fórmulas de Random, operadores booleanos, validação e risco de estado singleton. IDs físicos anteriormente comprovados.
- ✅ [Ars Technica 2.7.6](../providers/✅-ars-technica/PERK-ENGINEERING-MATRIX-2.7.6.md): os 11 objetos **já contados no catálogo** foram materializados pela primeira vez em 11 novos `glyphs/*.md` individuais com receitas Create, mana default, compatibilidade, cadeia causal e riscos de conservação. **+11 arquivos `.md`**, **+0 novas identidades de magia**.
- As quantidades de `.md` na tabela e o total de 2899 são a contagem de arquivos que já existiam na main baseline. A branch draft adicionou fichas/matrizes, portanto seus números de arquivo são maiores; não atualizar o denominador semântico para refletir documentação nova.
- Nenhum adapter Java, CI, GameTest, Survival ou Stage foi promovido. Testes de equivalência método↔JAR, config real, concorrência, claims e integração Create/Ars permanecem ⚠️ e adaptações de perks RPG ⛔.

## Continuação — Ars 'n' Spells e Ars Morph (2026-10-13)

- ✅ [Ars 'n' Spells 3.3.4](../providers/✅-ars-n-spells/PERK-ENGINEERING-MATRIX-3.3.4.md): cinco rituais com IDs e gates estáticos comprovados no JAR 3.3.4; cinco fichas ampliadas com source público exato **3.3.3**, preflight, receipt/settlement, configuração e boundary da bridge. **⚠️ sem prova de corpo de método exato da release instalada 3.3.4**.
- ✅ [Ars Morph 2.0.0](../providers/✅-ars-morph/PERK-ENGINEERING-MATRIX-2.0.0.md): uma ficha nova individual `glyphs/morph.md` com seleção de target/form, Max HP, Identity2 e condições de sucesso. Release-aligned source não equivale a bytecode físico nem a teste da versão atual Identity2.
- +0 identidades semânticas. O ledger de provider `.md` da main baseline (2899) não é métrica de cobertura de perks desta branch. Sem alterações runtime, adapters, CI, GameTests, QA/Survival ou promoção do Stage 06.05.

## Priorização para próximos lotes

1. Spells do Apprentice's Codex (`apprenticecodex`), 83 identidades source-pinned; depois validar as classes de entidades/helpers e a versão binária instalada.
2. Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1 e Ars Additions 21.3.0: objetos source-located no PR draft; aprofundar auxiliares/eventos/versões e QA, sem repetir fichas.
3. Goety 3.1.4, cujo catálogo dos 123 Focuses é exact-binary, mas muitos arquivos não comprovam método, custo, raio e hook.
4. Outros 162 diretórios conforme relevância de spells, glifos, rituais, habilidades e riscos/capacidade de implementação, sempre preservando as fontes instaladas.

**Não usar este ledger como contagem de spells** e não marcar implementação nem CI como completos.

## Continuação NEG 4.6.2 — 2026-10-13

- **8/40** fichas aprofundadas, com links Java e causalidade no novo `PERK-ENGINEERING-MATRIX-4.6.2.md`. IDs completos `glyph_` confirmados por `CompatRL`.
- Defaults retificados: Plow **0** (antes 5), Flatten **30** (antes 100), Echoing Trail **200, Tier III** (antes 50, Tier II). Os 40 registros incluem Momentum **source-disabled**, não 40 spells ativas.
- Perks e Mastery **⛔** fail-closed até hooks, custo/debit real e deduplicação. O source 4.6.2 e a estrutura da modlist são provas documentais, **não** execução de bytecode/GameTest/Survival. Delta semântico **+0**.

## Continuação Not Enough Glyphs — contingências/filtros, 2026-10-13

- **+22 fichas** individuais de engenharia (7 contingências e 15 filtros), cobertura de **8/40 a 30/40**; permanecem 10 perfis. Nova `PERK-ENGINEERING-MATRIX-FILTERS-CONTINGENCIES-4.6.2.md` e READMEs vinculados.
- Source pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`, `Events.java` para handlers de `LivingHealEvent`, `LivingDeathEvent`, `LivingUseTotemEvent`, `EntityTeleportEvent`; `ContingencyTriggers` para fall/fire/health; expiry pertence a Sauce. Semântica do cast armazenado e custos ainda exigem auditoria da dependência real.
- Retificações: `FilterLight` usa SKY e `FilterDark` usa BLOCK, limiar `8+ampMultiplier` (`>=` versus `<`); `EntityDummy` é incluído como player; `FilterSelf.onResolve` possui predicado local incompleto para exclusão de outros alvos (hipótese source-level, não falha física confirmada). Todas as identidades ganharam ID completo `glyph_` e links Java.
- Mantêm-se ⚠️ config ativa, bytecode instalado, GameTest/Survival e ⛔ hooks/adapters RPG. **+0 identidades semânticas**.

## Fechamento documental Not Enough Glyphs 4.6.2 — 2026-10-13

- **+10 fichas finais** atualizadas a partir do source público 4.6.2: Ride, Feed, Chaining, Reverse Direction, Resize, Propagate Missile/Overhead/Projectile/Self e Overhead form. A cobertura de engenharia chega a **40/40 (39 source-enabled condicionais; 1 source-disabled Momentum)** com três matrizes de controle.
- Observações: `EffectFeed` demanda custo item-side/explosão Crush e cuidado com eventos `Pre`; `EffectChaining` cria child resolvers e defaults 16 blocos/8 entidades; `EffectResize` exige auditoria de unidades `IPotionEffect`; `PropagateMissile` menciona Extract mas a lista de augments parece não incluí-lo na fonte.
- **+0** no denominador mágico global. Todos os 40 registros já existiam. Nenhum adapter, dano, mundo, receita, core Java, GameTest ou validação física foi implementado. Config ativa e equivalência source/binário ficam ⚠️; hooks de perks e Mastery permanecem ⛔.

## Dossiês Reliquified Ars Nouveau 0.8.1 — source 2026-10-13

- 3/19 `AbilityTemplate` roots aprofundadas em `PERK-ENGINEERING-MATRIX-0.8.1.md`; source declarado 0.8.1 `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`. **19/19 identidades estáticas já eram COUNTED_EXACT** no JAR hash-matched. +0 raízes semânticas.
- Archmage Glove: `SpellCastEvent` primário + `AugmentMulticast` posicional, filhos a cada 5 ticks, tag de custo 0 de filhos, chance de refund condicionada a resolução.
- Mana Ring: max mana/regeneration Ars, heal-to-mana, custo `SpellCostCalcEvent.Pre` com dívida `MANA_RING_DEBT`, repagamento pelo tick.
- Last Will: intercepta `LivingIncomingDamageEvent`, enfileira `RewindEvent` 60 ticks, cancela dano, registra cooldown, vingança por UUID e synergy dummy/vanishing.
- Implementação física exata de métodos / config atual / GameTests/Survival ⚠️; Black Arcana/RPG perk adapter ⛔.

## Fechamento documental Reliquified Ars Nouveau 0.8.1 — 2026-10-13

- Na continuação do PR #797, **+16 fichas** aprofundadas sobre as **3 prévias**, atingindo **19/19** em `PERK-ENGINEERING-MATRIX-0.8.1.md`. **+0 identidades**; as 19 roots já integravam a métrica global (mínimos mantidos).
- Bytecode/JAR físico verificado para registro `AbilityTemplate.builder` (Java 21 #38461801129), enquanto a engenharia de handlers/callbacks usa apenas source `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`. NÃO promover corpos compilados, config efetiva ou QA/Survival a PASS.
- Riscos mais importantes: `RingOfThrift` Pre/Post com free-cast token e refunds, `QuantumBubble` owner e lifecycle de projéteis, `ArchitectsStaff` MageBlock placement, `SpectralWalker` IntangibleAir e claims, `HornOfWildHunter` UUIDs de wolves, `IllusionistsMantle` death swap e `LastWill` rewind simultâneos.
- Interoperabilidade RPG **⛔** sem hook seguro; world/resource authority externa preservada. Stage 06.05 não avançou.

## Apprentice's Codex 0.9.7.1 — incremento de engenharia 2026-10-13

- `main` de partida `a6ccf7fd1d4ea6a18e5ff697f4e5abc82a197248`; versão física do sibling modlist `0.9.7.1`, JAR `apprentice_codex-0.9.7.1+mc1.21.1.jar`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`, mod ID `apprenticecodex`.
- **+8** dossiês causais profundos: [matriz técnica](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md), elevando **6/83→14/83**. **83/83** identidades permanecem catalogadas; **69/83** pendentes da mesma profundidade; **+0** ao denominador global.
- Auditoria source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` em eventos, auxiliares, managers e entidades; corpos do JAR/config/QA não provados. O provider/Iron's preserva ownership do cast/mana e world mutations; BA só do próprio runtime.
- **Perks/Mastery ⛔** sem contrato real; **Stage 06.05** não promovido. Alterações exclusivas em Markdown; sem GameTest físico de conteúdo Apprentice's Codex.

## Apprentice's Codex — entidades/jobs: +10 dossiês, 2026-10-13

- `main` de partida: `61696cd5ec7589c5f42a461d6c5ef4c2599e88c0`. Modlist sibling `main@f5d31633186a004ada41557220dcafa94a75546e` confirma `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.
- Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; **+10** dossiês em Auto Turret, Companion Trunk, Call Broom, Bound Sword, Bound Bow, Archer Multiple, Search Beacon, Tamer's Pocket, Personal Shelf e Tiny Lumberjack. [Matriz técnica lifecycle](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md).
- Cobertura de **engenharia causal** progride **14/83 → 24/83**, restam **59/83** sem a mesma profundidade. **Identidades catalogadas 83/83, +0 ao denominador semântico global**. Arquivos Markdown podem crescer, mas não são novas magias.
- Riscos ⚠️: cobrança de restock, cleanup varrendo níveis, item inventory/cursor, UUID e NBT de pets, item reservation/refund, transferência via item handler e jobs sem cap agregado neste manager. Bytecode exato do JAR, pack config e QA físico não provados.
- **Black Arcana e RPG Skill Tree:** nenhum adapter, cast replay, segunda liquidação, reward, claim policy ou world effect externo implementado; RPG perks/Mastery ⛔. Stage 06.05 permanece sem promoção.


## Apprentice's Codex 0.9.7.1 — persistência, combate e mundo (+10), 2026-10-14

- Baseline `Black-Arcana/main@504e00b83c1f4a09d4f265042af93369736d7a28`. Sibling modlist `main@82d7b7a8d15ab96ed7c59cc0c3e870edfe02cf4d` mantém `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.
- Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; **10 dossiês**: Assist Wings, Manifestation Grimoire, Bullet Stream, Healing Bloom, Heavenly Fist, Edge Dancer, World Flatter, Divine Possession, Otherworld Lens e Totem of Permafrost. [Matriz de alta fidelidade source-located](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
- Cobertura profunda avança **24/83→34/83**, restam **49/83**. **83/83 identidades já catalogadas, +0 raiz semântica**. Os eventos de entidades, visualização, timers e limpeza não ampliam o inventário de magias.
- **⚠️** Source não certifica bytecode do JAR nem execução de addon físico, configuração, world claim checks, Survival, client/dedicated, NBT ou incompatibilidade com outros mods. **⛔** nenhum adapter RPG perks/Mastery implementado e homologado. Sem código runtime BA ou Stage 06.05 promotion.


## Apprentice's Codex — ofensiva/movimento/detecção (+10), 2026-10-14

- Baseline `Black-Arcana/main@94f19f9ecf2959cb30fc6fa3195d3a71ca27bf9c`; source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; sibling modlist `main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46`.
- ✅ 83/83 catalogadas; 🟡 74/83 com engenharia causal, 9 pendentes; +10 dossiês anexados a fichas existentes, [matriz](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-OFFENSE-MOVEMENT-0.9.7.1.md), +0 raízes semânticas.
- Achado de auditoria: `ArcaneBeamEntity.tick` tem condição de frequência distinta do comentário. `MantisLeapMovementEvent` preserva fallback de pouso ao destino se os offsets falham; `SenseEvil` não apresenta cap explícito no coletor de highlights.
- ⚠️ QA do JAR/config, claims/PvP, dedicated, client e packets pendente. ⛔ RPG adapter sem contrato; Black Arcana não alterou pipeline mágico nem promoveu Stage.


## Apprentice's Codex — nove dossiês finais de source-level, 2026-10-14

- Dependência base `Black-Arcana catalog/apprentice-codex-offense-motion-sensing-20261014@e44a2aab5a6ff1b56b2aad36246f471d35cdf8cc` (PR #804); modlist sibling `main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46`; source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.
- ✅ 83/83 identidades + 🟡 **83/83 dossiês causais** com class/method tracing source-level, +9 sobre os 74 de #804, zero magias novas. [Matriz final](../providers/✅-apprentice-codex/PERK-ENGINEERING-MATRIX-FINAL-NINE-0.9.7.1.md).
- Riscos estáticos: `UniteLunaMoonEntity.explodeByAntiMagic` com multiplicador 3×; `PaletteShiftReceptionEvent.onSpellPreCast` cancela magia receptora; `ManaMendingCastData.matchesTarget` exige mesma instância de ItemStack; listener `DeepSensor` limita display a 8.
- ⚠️ Leitura source concluída **não** equivale a QA binário/Survival/dedicated/claims/PvP/config; ⛔ perks/Mastery ainda não implementáveis sem contrato homologado com RPG Skill Tree. Nenhuma promoção Stage 06.05.


## Apprentice's Codex — prova dos 83 registros no JAR exato, 2026-10-14

- [CI binária #38576975705](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38576975705): SHA-1 e SHA-256 do JAR oficial 0.9.7.1 coincidem com a modlist sibling; `SpellRegistry` contém **83/83** pares `ID → Supplier → reg() → DeferredHolder`, sem faltas, extras ou duplicações. [Relatório técnico](../providers/✅-apprentice-codex/README.md) e [evidência QA](../../../docs/qa/apprentice-codex-registry-binary-2026-10-14.md).
- **✅** igualdade documental/callsite de registro; **⚠️** não confirma registry carregado, classes de todos os spells em runtime, disponibilidade em Survival, configs nem comportamento real. `AC-P01–AC-P05` ainda **PENDING**. **⛔** nenhuma integração Mastery/perks sem contrato real RPG Skill Tree. Stage 06.05 inalterado.
