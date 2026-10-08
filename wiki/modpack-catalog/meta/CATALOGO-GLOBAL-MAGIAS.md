# Catálogo Global de Magias e Sistemas Sobrenaturais — Black Arcana

> **Estado auditado em 2026-10-08.** Referências: `Black-Arcana/main@a131ca1d1bc00049178977b3d60ff3ee017d7194`, modlist física certificada `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`. Este índice é uma visão agregada da árvore e não uma nova extração física de registries.

## Pendências de validação e cobertura global

O quadro operacional dos cinco itens solicitados encontra-se em [PENDENCIAS-MAGICAS-ATUAIS.md](PENDENCIAS-MAGICAS-ATUAIS.md). O [segundo ciclo cross-domain](AUDITORIA-CROSS-DOMAIN-2026-10-08.md) fixou 489/489 JARs fora da categoria física Magic (o loader NeoForge é a 587ª entrada total, mas não é JAR de mod), com 142 candidatos prioritários (46 por nome + 96 por categoria). A [varredura read-only de JARs](../../../docs/qa/nonmagic_physical_jar_triage.md) está implementada, ainda não executada na instância. Os outros 347 JARs permanecem no universo de auditoria; 39 providers source/release-bounded continuam aguardando prova binária de registry. Consulte os checkpoints antes de afirmar cobertura total de feitiços.

## Situação da catalogação

- **164/164 diretórios canônicos** de providers com prefixo `✅-` e `README.md` presente; **0 ❌, 0 🟡, 0 ⚠️ ou ⛔ no prefixo de catálogo**.
- **97/97 dossiês da categoria física `Magic`** reconciliados com diretórios canônicos, incluindo aliases documentados no [checkpoint de correspondência](PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md). A categoria `Magic` não inclui todos os providers sobrenaturais cross-domain.
- **162 diretórios** fazem parte do escopo explicitamente definido pelo usuário: foram excluídos aqui **Traveloptics / T.O Magic n' Extras** e **Deeper and Darker, mod-base**. O addon **Deeper & Darker Spellbooks** permanece dentro do escopo.
- **Atenção à presença física:** o índice de 164 diretórios é um inventário histórico/canônico de catálogos, não uma afirmação de 164 JARs instalados. **Ars Morph** e **Woodwalkers SpellBooks** constam em pastas históricas, mas estão **ausentes** no snapshot físico certificado; não integram a soma semântica atual.
- **Mínimo estrito semântico global 1851** e **mínimo do escopo do usuário 1849**. São mínimos fundamentados no [ledger](SEMANTIC-MAGIC-COVERAGE.md); o denominador semântico final permanece aberto. Não há declaração de 100% dos registries físicos do pack.
- ✅ significa **identidades catalogadas / materializadas no limite da evidência disponível**. Não equivale a magia habilitada, adquirível em Survival ou compatível com todos os outros mods em runtime.
- As condições de configuração e os candidatos condicionais estão no [ledger de fechamento condicional](CONDITIONAL-PROVIDER-CLOSURE.md), nos README de cada provider e no [coletor de evidências](../../../docs/qa/provider-catalog-deployed-evidence.md). Não converter condições não verificadas em PASS.

## Fichas e inventários de alta cardinalidade

| Provider | Catálogo já disponível | Situação da evidência |
|---|---|---|
| Ars Nouveau | [Inventário Ars](../providers/✅-ars-nouveau/README.md) | 109 componentes/rituais distintos no ledger; composições arbitrárias não duplicadas |
| Iron's Spells 'n Spellbooks | [Inventário Iron's](../providers/✅-irons-spells/README.md) | base e addons segregados por autoria |
| Apprentice's Codex | [83 feitiços/fichas](../providers/✅-apprentice-codex/README.md) | versão 0.9.7.1 source-pinned |
| Monsters & Spellbooks | [98 feitiços](../providers/✅-monsters-spellbooks/SPELL-CATALOG.md) | fonte pública contemporânea; registry binário 0.0.16.3 ainda não provado |
| Somake Spells | [83 registros e 83 fichas](../providers/✅-somake-spells/MAGIC-CARDS-1.0.9.md) | exato 1.0.9; alcance/configuração separados |
| Not Enough Glyphs | [40 glifos](../providers/✅-not-enough-glyphs/README.md) | 39 candidatos source-enabled; config ativa ainda condicionada |
| Ars Zero | [12 glifos/capacidades](../providers/✅-ars-zero/GLYPH-CATALOG.md) | evidência da release 2.0.2, sem inventar IDs |
| Tunes n' Tomes | [16 fichas de spells](../providers/✅-tunes-n-tomes/SPELL-CARDS-1.1.0-HOTFIX.md) | 16 nomes da página da editora, ids/classes/custos internos não verificados |
| Simply Swords | [66 ações individualizadas](../providers/✅-simply-swords/ACTION-CARDS-1.70.2.md) | alcance e Awakening ainda condicionados |
| Simply More | [24 ações sobrenaturais](../providers/✅-simply-more/README.md) | alcance, configuração e Mimicry ainda condicionados |

## Inventário completo de providers da árvore canônica

Cada README é a entrada principal do provider. Ali ficam os links para spell registries, fichas individuais, rituais, efeitos, sistemas, exclusões e fontes quando aplicáveis. Um provider com **+0 objetos mágicos próprios** pode constar aqui para registrar explicitamente que sua contribuição é de biblioteca, compatibilidade, progressão, equipamento, efeito passivo ou infraestrutura: isso **não** cria uma magia fictícia.

| Provider/diretório | Catálogo | Evidência / README | Relação com o escopo |
|---|---|---|---|
| `a-good-place` | ✅ | [README](../providers/✅-a-good-place/README.md) | Dentro do inventário global |
| `aces-spell-utils` | ✅ | [README](../providers/✅-aces-spell-utils/README.md) | Dentro do inventário global |
| `acolyte` | ✅ | [README](../providers/✅-acolyte/README.md) | Dentro do inventário global |
| `aeromancy-additions` | ✅ | [README](../providers/✅-aeromancy-additions/README.md) | Dentro do inventário global |
| `alexs-caves-continued` | ✅ | [README](../providers/✅-alexs-caves-continued/README.md) | Dentro do inventário global |
| `alexs-mobs-continued` | ✅ | [README](../providers/✅-alexs-mobs-continued/README.md) | Dentro do inventário global |
| `alshanex-familiars` | ✅ | [README](../providers/✅-alshanex-familiars/README.md) | Dentro do inventário global |
| `apokinetics` | ✅ | [README](../providers/✅-apokinetics/README.md) | Dentro do inventário global |
| `apotheosis` | ✅ | [README](../providers/✅-apotheosis/README.md) | Dentro do inventário global |
| `apotheotic-creation` | ✅ | [README](../providers/✅-apotheotic-creation/README.md) | Dentro do inventário global |
| `apothic-attributes` | ✅ | [README](../providers/✅-apothic-attributes/README.md) | Dentro do inventário global |
| `apothic-compat` | ✅ | [README](../providers/✅-apothic-compat/README.md) | Dentro do inventário global |
| `apothic-compats` | ✅ | [README](../providers/✅-apothic-compats/README.md) | Dentro do inventário global |
| `apothic-enchanting` | ✅ | [README](../providers/✅-apothic-enchanting/README.md) | Dentro do inventário global |
| `apothic-spawners` | ✅ | [README](../providers/✅-apothic-spawners/README.md) | Dentro do inventário global |
| `apprentice-codex` | ✅ | [README](../providers/✅-apprentice-codex/README.md) | Dentro do inventário global |
| `ars-additions` | ✅ | [README](../providers/✅-ars-additions/README.md) | Dentro do inventário global |
| `ars-controle` | ✅ | [README](../providers/✅-ars-controle/README.md) | Dentro do inventário global |
| `ars-creo` | ✅ | [README](../providers/✅-ars-creo/README.md) | Dentro do inventário global |
| `ars-elemancy` | ✅ | [README](../providers/✅-ars-elemancy/README.md) | Dentro do inventário global |
| `ars-elemental` | ✅ | [README](../providers/✅-ars-elemental/README.md) | Dentro do inventário global |
| `ars-hex` | ✅ | [README](../providers/✅-ars-hex/README.md) | Dentro do inventário global |
| `ars-morph` | ✅ | [README](../providers/✅-ars-morph/README.md) | Dentro do inventário global |
| `ars-n-spells` | ✅ | [README](../providers/✅-ars-n-spells/README.md) | Dentro do inventário global |
| `ars-nouveau` | ✅ | [README](../providers/✅-ars-nouveau/README.md) | Dentro do inventário global |
| `ars-polymorphia` | ✅ | [README](../providers/✅-ars-polymorphia/README.md) | Dentro do inventário global |
| `ars-sable` | ✅ | [README](../providers/✅-ars-sable/README.md) | Dentro do inventário global |
| `ars-sophisticated-compat` | ✅ | [README](../providers/✅-ars-sophisticated-compat/README.md) | Dentro do inventário global |
| `ars-technica` | ✅ | [README](../providers/✅-ars-technica/README.md) | Dentro do inventário global |
| `ars-two-way-portals` | ✅ | [README](../providers/✅-ars-two-way-portals/README.md) | Dentro do inventário global |
| `ars-zero` | ✅ | [README](../providers/✅-ars-zero/README.md) | Dentro do inventário global |
| `arsdelight` | ✅ | [README](../providers/✅-arsdelight/README.md) | Dentro do inventário global |
| `artifacts` | ✅ | [README](../providers/✅-artifacts/README.md) | Dentro do inventário global |
| `asterism-arcanum` | ✅ | [README](../providers/✅-asterism-arcanum/README.md) | Dentro do inventário global |
| `backported-spellbooks` | ✅ | [README](../providers/✅-backported-spellbooks/README.md) | Dentro do inventário global |
| `betterend` | ✅ | [README](../providers/✅-betterend/README.md) | Dentro do inventário global |
| `betternether` | ✅ | [README](../providers/✅-betternether/README.md) | Dentro do inventário global |
| `bloodlines` | ✅ | [README](../providers/✅-bloodlines/README.md) | Dentro do inventário global |
| `born-in-chaos` | ✅ | [README](../providers/✅-born-in-chaos/README.md) | Dentro do inventário global |
| `bosses-of-mass-destruction` | ✅ | [README](../providers/✅-bosses-of-mass-destruction/README.md) | Dentro do inventário global |
| `bosses-rise` | ✅ | [README](../providers/✅-bosses-rise/README.md) | Dentro do inventário global |
| `cataclysm` | ✅ | [README](../providers/✅-cataclysm/README.md) | Dentro do inventário global |
| `cataclysm-spellbooks` | ✅ | [README](../providers/✅-cataclysm-spellbooks/README.md) | Dentro do inventário global |
| `cold-sweat` | ✅ | [README](../providers/✅-cold-sweat/README.md) | Dentro do inventário global |
| `companions` | ✅ | [README](../providers/✅-companions/README.md) | Dentro do inventário global |
| `corail-tombstone` | ✅ | [README](../providers/✅-corail-tombstone/README.md) | Dentro do inventário global |
| `create-chromatic-return` | ✅ | [README](../providers/✅-create-chromatic-return/README.md) | Dentro do inventário global |
| `create-cold-sweat` | ✅ | [README](../providers/✅-create-cold-sweat/README.md) | Dentro do inventário global |
| `create-deep-dark` | ✅ | [README](../providers/✅-create-deep-dark/README.md) | Dentro do inventário global |
| `create-dragons-plus` | ✅ | [README](../providers/✅-create-dragons-plus/README.md) | Dentro do inventário global |
| `create-dreams-n-desires` | ✅ | [README](../providers/✅-create-dreams-n-desires/README.md) | Dentro do inventário global |
| `create-enchantable-machinery` | ✅ | [README](../providers/✅-create-enchantable-machinery/README.md) | Dentro do inventário global |
| `create-enchantment-industry` | ✅ | [README](../providers/✅-create-enchantment-industry/README.md) | Dentro do inventário global |
| `create-enchantment-industry-plus` | ✅ | [README](../providers/✅-create-enchantment-industry-plus/README.md) | Dentro do inventário global |
| `create-ender-transmission` | ✅ | [README](../providers/✅-create-ender-transmission/README.md) | Dentro do inventário global |
| `create-fantasizing-again` | ✅ | [README](../providers/✅-create-fantasizing-again/README.md) | Dentro do inventário global |
| `create-mechanical-companion` | ✅ | [README](../providers/✅-create-mechanical-companion/README.md) | Dentro do inventário global |
| `create-mechanical-spawner` | ✅ | [README](../providers/✅-create-mechanical-spawner/README.md) | Dentro do inventário global |
| `create-mobile-packages` | ✅ | [README](../providers/✅-create-mobile-packages/README.md) | Dentro do inventário global |
| `create-more-automation` | ✅ | [README](../providers/✅-create-more-automation/README.md) | Dentro do inventário global |
| `create-more-features` | ✅ | [README](../providers/✅-create-more-features/README.md) | Dentro do inventário global |
| `create-teleporters-remastered` | ✅ | [README](../providers/✅-create-teleporters-remastered/README.md) | Dentro do inventário global |
| `create-wizardry` | ✅ | [README](../providers/✅-create-wizardry/README.md) | Dentro do inventário global |
| `creating-space` | ✅ | [README](../providers/✅-creating-space/README.md) | Dentro do inventário global |
| `crystal-chronicles` | ✅ | [README](../providers/✅-crystal-chronicles/README.md) | Dentro do inventário global |
| `deeper-and-darker` | ✅ | [README](../providers/✅-deeper-and-darker/README.md) | Fora do escopo específico |
| `deeper-and-darker-spellbooks` | ✅ | [README](../providers/✅-deeper-and-darker-spellbooks/README.md) | Dentro do inventário global |
| `dimensional-sable` | ✅ | [README](../providers/✅-dimensional-sable/README.md) | Dentro do inventário global |
| `dis-enchanting-table` | ✅ | [README](../providers/✅-dis-enchanting-table/README.md) | Dentro do inventário global |
| `discerning-the-eldritch` | ✅ | [README](../providers/✅-discerning-the-eldritch/README.md) | Dentro do inventário global |
| `dragon-care` | ✅ | [README](../providers/✅-dragon-care/README.md) | Dentro do inventário global |
| `dreamless-spells` | ✅ | [README](../providers/✅-dreamless-spells/README.md) | Dentro do inventário global |
| `dungeons-delight` | ✅ | [README](../providers/✅-dungeons-delight/README.md) | Dentro do inventário global |
| `dynamic-rpg-resource-bars` | ✅ | [README](../providers/✅-dynamic-rpg-resource-bars/README.md) | Dentro do inventário global |
| `efiscompat` | ✅ | [README](../providers/✅-efiscompat/README.md) | Dentro do inventário global |
| `eidolon-repraised` | ✅ | [README](../providers/✅-eidolon-repraised/README.md) | Dentro do inventário global |
| `emf-compat-iron-spells` | ✅ | [README](../providers/✅-emf-compat-iron-spells/README.md) | Dentro do inventário global |
| `enchantment-descriptions` | ✅ | [README](../providers/✅-enchantment-descriptions/README.md) | Dentro do inventário global |
| `enders-spells-and-stuff-requiem` | ✅ | [README](../providers/✅-enders-spells-and-stuff-requiem/README.md) | Dentro do inventário global |
| `epic-fight` | ✅ | [README](../providers/✅-epic-fight/README.md) | Dentro do inventário global |
| `familiarslib` | ✅ | [README](../providers/✅-familiarslib/README.md) | Dentro do inventário global |
| `fantasy-armor` | ✅ | [README](../providers/✅-fantasy-armor/README.md) | Dentro do inventário global |
| `farmers-spell` | ✅ | [README](../providers/✅-farmers-spell/README.md) | Dentro do inventário global |
| `fires-ender-expansion` | ✅ | [README](../providers/✅-fires-ender-expansion/README.md) | Dentro do inventário global |
| `gaze` | ✅ | [README](../providers/✅-gaze/README.md) | Dentro do inventário global |
| `goety` | ✅ | [README](../providers/✅-goety/README.md) | Dentro do inventário global |
| `goety-cataclysm` | ✅ | [README](../providers/✅-goety-cataclysm/README.md) | Dentro do inventário global |
| `goety-iron` | ✅ | [README](../providers/✅-goety-iron/README.md) | Dentro do inventário global |
| `grapplemod-skybound` | ✅ | [README](../providers/✅-grapplemod-skybound/README.md) | Dentro do inventário global |
| `gtbcs-geomancy-plus` | ✅ | [README](../providers/✅-gtbcs-geomancy-plus/README.md) | Dentro do inventário global |
| `gtbcs-spelllib` | ✅ | [README](../providers/✅-gtbcs-spelllib/README.md) | Dentro do inventário global |
| `hazen-n-stuff` | ✅ | [README](../providers/✅-hazen-n-stuff/README.md) | Dentro do inventário global |
| `hazentouvelib` | ✅ | [README](../providers/✅-hazentouvelib/README.md) | Dentro do inventário global |
| `hexalia` | ✅ | [README](../providers/✅-hexalia/README.md) | Dentro do inventário global |
| `ice-and-fire-ce` | ✅ | [README](../providers/✅-ice-and-fire-ce/README.md) | Dentro do inventário global |
| `ice-and-fire-dread-land` | ✅ | [README](../providers/✅-ice-and-fire-dread-land/README.md) | Dentro do inventário global |
| `ignis-soulfires` | ✅ | [README](../providers/✅-ignis-soulfires/README.md) | Dentro do inventário global |
| `ignis-soulfires-spellbooks` | ✅ | [README](../providers/✅-ignis-soulfires-spellbooks/README.md) | Dentro do inventário global |
| `immersive-portal-irons-spells-addon` | ✅ | [README](../providers/✅-immersive-portal-irons-spells-addon/README.md) | Dentro do inventário global |
| `immersive-portals-true-immersion` | ✅ | [README](../providers/✅-immersive-portals-true-immersion/README.md) | Dentro do inventário global |
| `integrated-villages` | ✅ | [README](../providers/✅-integrated-villages/README.md) | Dentro do inventário global |
| `irons-apothic` | ✅ | [README](../providers/✅-irons-apothic/README.md) | Dentro do inventário global |
| `irons-gems-n-jewelry` | ✅ | [README](../providers/✅-irons-gems-n-jewelry/README.md) | Dentro do inventário global |
| `irons-lib` | ✅ | [README](../providers/✅-irons-lib/README.md) | Dentro do inventário global |
| `irons-spellbooks-kubejs` | ✅ | [README](../providers/✅-irons-spellbooks-kubejs/README.md) | Dentro do inventário global |
| `irons-spells` | ✅ | [README](../providers/✅-irons-spells/README.md) | Dentro do inventário global |
| `irons-spells-recolor` | ✅ | [README](../providers/✅-irons-spells-recolor/README.md) | Dentro do inventário global |
| `ironsable` | ✅ | [README](../providers/✅-ironsable/README.md) | Dentro do inventário global |
| `ironsable-x-winds-spellbooks` | ✅ | [README](../providers/✅-ironsable-x-winds-spellbooks/README.md) | Dentro do inventário global |
| `iss-magic-from-the-east` | ✅ | [README](../providers/✅-iss-magic-from-the-east/README.md) | Dentro do inventário global |
| `kubejs-ars-nouveau` | ✅ | [README](../providers/✅-kubejs-ars-nouveau/README.md) | Dentro do inventário global |
| `legendary-monsters` | ✅ | [README](../providers/✅-legendary-monsters/README.md) | Dentro do inventário global |
| `legendary-spellbooks` | ✅ | [README](../providers/✅-legendary-spellbooks/README.md) | Dentro do inventário global |
| `leyline-spellbooks` | ✅ | [README](../providers/✅-leyline-spellbooks/README.md) | Dentro do inventário global |
| `malum` | ✅ | [README](../providers/✅-malum/README.md) | Dentro do inventário global |
| `mobstein` | ✅ | [README](../providers/✅-mobstein/README.md) | Dentro do inventário global |
| `monsters-spellbooks` | ✅ | [README](../providers/✅-monsters-spellbooks/README.md) | Dentro do inventário global |
| `more-relics` | ✅ | [README](../providers/✅-more-relics/README.md) | Dentro do inventário global |
| `mowzies-cataclysm` | ✅ | [README](../providers/✅-mowzies-cataclysm/README.md) | Dentro do inventário global |
| `mowzies-mobs` | ✅ | [README](../providers/✅-mowzies-mobs/README.md) | Dentro do inventário global |
| `northstar-redux` | ✅ | [README](../providers/✅-northstar-redux/README.md) | Dentro do inventário global |
| `not-enough-glyphs` | ✅ | [README](../providers/✅-not-enough-glyphs/README.md) | Dentro do inventário global |
| `ozymandias-sundries` | ✅ | [README](../providers/✅-ozymandias-sundries/README.md) | Dentro do inventário global |
| `paladin-spells` | ✅ | [README](../providers/✅-paladin-spells/README.md) | Dentro do inventário global |
| `photon` | ✅ | [README](../providers/✅-photon/README.md) | Dentro do inventário global |
| `pickable-orbs` | ✅ | [README](../providers/✅-pickable-orbs/README.md) | Dentro do inventário global |
| `portable-hole` | ✅ | [README](../providers/✅-portable-hole/README.md) | Dentro do inventário global |
| `protection-pixel` | ✅ | [README](../providers/✅-protection-pixel/README.md) | Dentro do inventário global |
| `pufferfishs-attributes` | ✅ | [README](../providers/✅-pufferfishs-attributes/README.md) | Dentro do inventário global |
| `pufferfishs-skills` | ✅ | [README](../providers/✅-pufferfishs-skills/README.md) | Dentro do inventário global |
| `pufferfishs-unofficial-additions` | ✅ | [README](../providers/✅-pufferfishs-unofficial-additions/README.md) | Dentro do inventário global |
| `relics` | ✅ | [README](../providers/✅-relics/README.md) | Dentro do inventário global |
| `reliquified-ars-nouveau` | ✅ | [README](../providers/✅-reliquified-ars-nouveau/README.md) | Dentro do inventário global |
| `reliquified-artifacts` | ✅ | [README](../providers/✅-reliquified-artifacts/README.md) | Dentro do inventário global |
| `reliquified-irons-spells-n-spellbooks` | ✅ | [README](../providers/✅-reliquified-irons-spells-n-spellbooks/README.md) | Dentro do inventário global |
| `reliquified-l-enders-cataclysm` | ✅ | [README](../providers/✅-reliquified-l-enders-cataclysm/README.md) | Dentro do inventário global |
| `reliquified-lenders-cataclysm-new-relics-fix` | ✅ | [README](../providers/✅-reliquified-lenders-cataclysm-new-relics-fix/README.md) | Dentro do inventário global |
| `runiclib` | ✅ | [README](../providers/✅-runiclib/README.md) | Dentro do inventário global |
| `shadowsz` | ✅ | [README](../providers/✅-shadowsz/README.md) | Dentro do inventário global |
| `simply-more` | ✅ | [README](../providers/✅-simply-more/README.md) | Dentro do inventário global |
| `simply-swords` | ✅ | [README](../providers/✅-simply-swords/README.md) | Dentro do inventário global |
| `simply-swords-cataclysm` | ✅ | [README](../providers/✅-simply-swords-cataclysm/README.md) | Dentro do inventário global |
| `sky-aesthetics` | ✅ | [README](../providers/✅-sky-aesthetics/README.md) | Dentro do inventário global |
| `snow-real-magic` | ✅ | [README](../providers/✅-snow-real-magic/README.md) | Dentro do inventário global |
| `somake-spells` | ✅ | [README](../providers/✅-somake-spells/README.md) | Dentro do inventário global |
| `soul-fire-d` | ✅ | [README](../providers/✅-soul-fire-d/README.md) | Dentro do inventário global |
| `spell-actionbar` | ✅ | [README](../providers/✅-spell-actionbar/README.md) | Dentro do inventário global |
| `spell-codex-specs` | ✅ | [README](../providers/✅-spell-codex-specs/README.md) | Dentro do inventário global |
| `starbunclemania` | ✅ | [README](../providers/✅-starbunclemania/README.md) | Dentro do inventário global |
| `toxony` | ✅ | [README](../providers/✅-toxony/README.md) | Dentro do inventário global |
| `traveloptics` | ✅ | [README](../providers/✅-traveloptics/README.md) | Fora do escopo específico |
| `tunes-n-tomes` | ✅ | [README](../providers/✅-tunes-n-tomes/README.md) | Dentro do inventário global |
| `vampire-spells-addon` | ✅ | [README](../providers/✅-vampire-spells-addon/README.md) | Dentro do inventário global |
| `vampiric-ageing` | ✅ | [README](../providers/✅-vampiric-ageing/README.md) | Dentro do inventário global |
| `vampirism` | ✅ | [README](../providers/✅-vampirism/README.md) | Dentro do inventário global |
| `vampirism-integrations` | ✅ | [README](../providers/✅-vampirism-integrations/README.md) | Dentro do inventário global |
| `waystones` | ✅ | [README](../providers/✅-waystones/README.md) | Dentro do inventário global |
| `weapons-of-miracles` | ✅ | [README](../providers/✅-weapons-of-miracles/README.md) | Dentro do inventário global |
| `werewolves` | ✅ | [README](../providers/✅-werewolves/README.md) | Dentro do inventário global |
| `winds-spellbooks` | ✅ | [README](../providers/✅-winds-spellbooks/README.md) | Dentro do inventário global |
| `woodwalkers-spellbooks` | ✅ | [README](../providers/✅-woodwalkers-spellbooks/README.md) | Dentro do inventário global |
| `ypsilons-fundamentalism` | ✅ | [README](../providers/✅-ypsilons-fundamentalism/README.md) | Dentro do inventário global |
| `yungs-better-end-island` | ✅ | [README](../providers/✅-yungs-better-end-island/README.md) | Dentro do inventário global |
| `yungs-better-witch-huts` | ✅ | [README](../providers/✅-yungs-better-witch-huts/README.md) | Dentro do inventário global |

## Interpretação obrigatória e continuidade

- Não há diretórios canônicos da árvore atual faltando README. Os **97/97** da categoria física `Magic` e o inventário cross-domain atual estão catalogados estruturalmente.
- O **universo físico completo dos 587 mods** contém categorias não-mágicas. A declaração de que *não exista mais nenhum* poder semântico oculto em um desses JARs exigiria uma nova auditoria física integral, não uma inferência a partir de nomes/prefixos.
- Os **281 objetos/famílias de ações condicionais** registrados na auditoria são identidades já catalogadas, não 281 feitiços sem ficha a serem inventados. Sua confirmação em Survival/runtime exige configuração e evidência da instância.
- A discrepância entre NeoForge físico **21.1.250** e baseline Gradle **21.1.248** permanece identificada, sem alterar o build automaticamente.
- Black Arcana detém autoridade sobre seu casting, rituais, domains, Arcane Danger, Corruption, Strain, persistência e world safety. O RPG Skill Tree continua sibling de atributos, perks, Mastery e gates via contrato verificado.
