# Cobertura global de dossiês técnicos para perks — base rastreável

**Fonte:** árvore `Gustavaopere/Black-Arcana/main@465593694120c80db576344fc51de0d52d68d541`; auditoria estrutural de arquivos Markdown sob `wiki/modpack-catalog/providers/`, 2026-10-13.

- Diretórios com Markdown: **165**.
- Arquivos `.md` em providers: **2899**.
- **Isto não significa 2899 feitiços**: inclui índices, metadados, auditorias, arquivos de suporte, guias e objetos com classificação condicional.
- A meta é que **cada ficha real de objeto mágico** contenha o dossiê definido em [PERK-READY-TECHNICAL-STANDARD.md](PERK-READY-TECHNICAL-STANDARD.md); arquivos agregados ficam como índices ou provas.
- O Iron's base possui 110 fichas anotadas em [PR #795 (draft)](https://github.com/Gustavaopere/Black-Arcana/pull/795), **fora da main de referência**; não contam como conteúdo fundido.
- O Apprentice's Codex 0.9.7.1 possui 83 fichas de spells previamente source-catalogadas. Nesta branch, as **83/83 fichas receberam localizadores exatos** de classe/registro; seis tiveram rastreio causal específico (Higanbana, Blood Brand, Mist Form, Arcane Blast, Thermal Process, Echo Cast). É localização source-pinned, não prova de hooks ou runtime.
- Este inventário **não** modifica o estado de catalogação semântica vigente (mínimos 1857 global / 1855 escopo) nem a campanha de prova binária 25/39.

## Convenção de acompanhamento

A terceira coluna indica **a situação incremental nesta branch a partir da baseline da `main`**, não diz que o provider esteja ❌ não catalogado. Os registros podem já possuir valores/fórmulas validados por outras auditorias: esses dados devem ser aproveitados e os gaps calculados arquivo a arquivo. Conferência de completude por provider requer filtrar fichas de identidade semântica e validar prova por campo; uma quantidade de Markdown não substitui essa operação.

| Diretório do provider | Arquivos `.md` existentes | Gaps de dossiê técnico |
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
| `✅-apprentice-codex` | 101 | 🟡 83/83 fichas de spell com source class; 6 com causalidade aprofundada; hooks/QA pendentes |
| `✅-ars-additions` | 48 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-controle` | 25 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-creo` | 14 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-elemancy` | 11 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-elemental` | 59 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-hex` | 10 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-morph` | 7 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-n-spells` | 15 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-nouveau` | 149 | 🟡 4 fichas (Projectile, Ignite, Heal, Flight ritual) aprofundadas; demais pendentes |
| `✅-ars-polymorphia` | 3 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-sable` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-sophisticated-compat` | 4 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
| `✅-ars-technica` | 8 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
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
| `✅-not-enough-glyphs` | 49 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
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
| `✅-reliquified-ars-nouveau` | 21 | Não auditado em escala para perks; requer conferência de fichas de objetos mágicos |
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

## Priorização para próximos lotes

1. Spells do Apprentice's Codex (`apprenticecodex`), 83 identidades source-pinned; depois validar as classes de entidades/helpers e a versão binária instalada.
2. Ars Nouveau 5.13.1 (form, effect, augment, ritual), que exige auditoria de composição e modificadores semânticos diferentes de Iron's.
3. Goety 3.1.4, cujo catálogo dos 123 Focuses é exact-binary, mas muitos arquivos não comprovam método, custo, raio e hook.
4. Outros 162 diretórios conforme relevância de spells, glifos, rituais, habilidades e riscos/capacidade de implementação, sempre preservando as fontes instaladas.

**Não usar este ledger como contagem de spells** e não marcar implementação nem CI como completos.
