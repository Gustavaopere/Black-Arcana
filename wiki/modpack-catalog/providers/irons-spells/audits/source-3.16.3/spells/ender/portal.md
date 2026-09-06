# Portal — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE AUDITADO — TESTE DO JAR DO PACK AINDA NECESSÁRIO PARA BRIDGE IMMERSIVE PORTALS`

## Identidade

- **ID:** `irons_spellbooks:portal`
- **Provider:** Iron's Spells 'n Spellbooks 1.21.1-3.16.3
- **Escola:** Ender
- **Raridade mínima:** Uncommon
- **Max level:** 3
- **Função:** portal pareado / mobilidade

## Custo e casting

- **Mana base:** 200
- **Mana por nível:** +10
- **Cooldown:** 180 s
- **Cast type:** Instant
- **Recasts:** 2 endpoints
- **Alcance de colocação:** 48 blocos
- **Janela para segundo endpoint:** 120 s
- **Duração do portal:** `spellPower * 20 ticks`
- **Spell power base:** 300
- **Spell power/level:** +120

## Efeito

O primeiro cast cria/registra o primeiro endpoint; o segundo fecha o par. O spell suporta portal entities e Portal Frame block entities, com `PortalManager`/`PortalData` mantendo identidade e ligação.

Não pode ser lançado de dentro da Pocket Dimension.

## Immersive Portals

O pack possui `immersive_portal_irons_spells_n_spellbooks_addon-1.0.1.jar`. A arquitetura Black Arcana preserva:

- **Iron's** como owner de spell, mana, cooldown, recasts, progressão e destino;
- **Immersive Portals bridge** como apresentação/travessia contínua;
- **Black Arcana** apenas como integração/safety adicional quando houver hook necessário.

Caos, Ordem, Divine e Infernal podem ter **skins/VFX/frames distintos**, mas não criam quatro motores de portal.

## Deduplicação

Bloqueia:

- portal genérico de Ordem;
- portal genérico de Caos;
- portal genérico Divine;
- portal genérico Infernal.

Um novo spell precisa mudar a semântica — por exemplo restrição, one-way law gate, vínculo com estrutura/recurso, destination policy ou outro contrato real — e ainda deve preferir este provider quando possível.

## Authority

A criação é feita no servidor para `Player`/`ServerLevel`. Endpoints têm UUID/owner e são registrados no manager do provider.

## VFX

O visual do Black Arcana/bridge pode ser aprimorado, mas partículas/renderização não decidem destino, duração ou ownership.

## Fonte técnica

`PortalSpell.java` no branch 1.21 do provider, versão declarada 3.16.3.
