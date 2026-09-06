# Iron's Spells 3.16.3 — Auditoria Holy

## Estado

`13/13 SPELLS DO REGISTRY INDIVIDUALIZADOS / SOURCE AUDITADO`

Esta auditoria usa o branch `1.21` do source oficial que declara exatamente `mod_version=1.21.1-3.16.3`, correspondente ao provider instalado no pack.

| Spell | ID | Raridade | Max Lv | Mana base | Mana/Lv | CD | Cast | Função-chave |
|---|---|---:|---:|---:|---:|---:|---|---|
| Angel Wing | `angel_wing` | Legendary | 5 | 80 | 20 | 120s | Instant | voo temporário |
| Blessing of Life | `blessing_of_life` | Common | 10 | 10 | 5 | 10s | Long 30t | cura de alvo |
| Cloud of Regeneration | `cloud_of_regeneration` | Common | 5 | 10 | 3 | 35s | Continuous 200t | cura em área; **deprecated** |
| Fortify | `fortify` | Common | 10 | 80 | 10 | 180s | Long 60t | absorção/fortificação em grupo |
| Greater Heal | `greater_heal` | Rare | 1 | 100 | 0 | 45s | Long 120t | full self-heal |
| Guiding Bolt | `guiding_bolt` | Common | 10 | 20 | 5 | 8s | Instant | projétil Holy |
| Healing Circle | `healing_circle` | Common | 10 | 40 | 10 | 25s | Long 20t | healing AoE persistente |
| Heal | `heal` | Uncommon | 8 | 30 | 15 | 30s | Instant | self-heal |
| Sunbeam | `sunbeam` | Uncommon | 10 | 40 | 10 | 20s | Instant | beam/strike Holy a distância |
| Wisp | `wisp` | Common | 10 | 15 | 2 | 3s | Long 20t | entidade Holy direcionada |
| Divine Smite | `divine_smite` | Common | 5 | 30 | 15 | 15s | Long 16t | smite melee + weapon damage |
| Haste | `haste` | Epic | 4 | 50 | 10 | 80s | Long 30t | Hastened buff |
| Cleanse | `cleanse` | Epic | 1 | 100 | 0 | 60s | Long 60t | remove harmful effects em aliados |

## Hook de cura confirmado

`Heal`, `Greater Heal`, `Blessing of Life` e `Cloud of Regeneration` publicam `SpellHealEvent` antes de aplicar a cura. Este evento é preferível para integração causal com RPG/Black Arcana quando a pergunta for “qual spell/provider gerou esta cura?”.

`Healing Circle` delega cura a `HealingAoe`; a causalidade detalhada desse entity runtime deve ser auditada antes de afirmar o mesmo event path.

## Consequência para Magia Divina/Celestial

A nova disciplina não deve competir com Holy base nos nichos já ocupados:

- self-heal;
- full heal;
- heal de aliado;
- healing circle;
- regen cloud;
- absorção/fortify;
- haste;
- cleanse;
- asas/voo;
- bolt Holy;
- Sunbeam;
- melee smite.

O delta aprovado para pesquisa Divine/Celestial passa a concentrar-se em:

1. **Sanctum / Ressonância Celestial** como infraestrutura para Miracle-tier, sem Aether;
2. **consagração** de área/objeto/estrutura;
3. **exorcismo** contra possession/demon/spirit semanticamente reconhecido;
4. **julgamento** condicionado por natureza/estado do alvo, não outro smite genérico;
5. **intercessão/proteção milagrosa** com custo e gates altos, sem duplicar Fortify/Paladin;
6. **celestial law/ward** quando houver delta contra Ordem;
7. efeitos de céu/Sol/Lua/estrelas como gates e amplificadores bounded, não mana gratuita.

## Paladin addon

Paladin Spells continua como segundo provider Holy a deduplicar. Seus cinco spells já estão documentados separadamente, com QA pendente para `Sworn Protector` e `Bulwark` por problemas encontrados no source 1.21.

## Próximos cruzamentos antes de fechar Divine

- Asterism Arcanum — Astral;
- Eidolon — Theurgy/ritual;
- Cataclysm Spellbooks — Holy summons;
- demais Iron's addons com Holy;
- RPG Skill Tree HOLY;
- possíveis effects/rituals de Goety/Malum/Hexalia que sejam funcionalmente equivalentes.
