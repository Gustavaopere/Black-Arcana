# Somake Spells — inventário nominal público da linha 1.0.x

## Regra de leitura

Este arquivo **não é o registry inventory completo**. O publisher afirma que Somake possui `over 50 new spells`, mas a documentação pública não expõe uma tabela completa e confiável de IDs/valores para o artefato instalado `1.0.8-fix`.

Os nomes abaixo entram somente quando aparecem explicitamente em changelogs oficiais 1.21.1. O estado diferencia:

- `CURRENT-LINE DIRECT` — citado/retrabalhado na release base 1.0.8, imediatamente anterior ao fix instalado;
- `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` — introduzido em release anterior, sem remoção pública localizada, mas não promovido a presença exata 1.0.8-fix sem registry/source;
- `REMOVED` — publisher registrou remoção explícita;
- `RENAMED` — nome antigo substituído explicitamente.

## 1.0.8 — nomes diretamente presentes na release base atual

| Nome público | Escola publicada | Semântica pública | Estado |
|---|---|---|---|
| Ritual Flame | Fire | lança chama ritual; pode ativar rituais de pedestais de fogo e evoluir variantes elementais de blaze | `CURRENT-LINE DIRECT` |
| Custodia Caeli | Holy | marca círculo no chão, chama sigilo e concede buff defensivo a jogadores dentro | `CURRENT-LINE DIRECT` |
| Bloody Legacy | não publicada no item do changelog | golpeia o chão e causa dano aos inimigos em linha reta | `CURRENT-LINE DIRECT / SCHOOL UNVERIFIED` |
| Fragmented Requiem | Blood | anel de espadas fragmentadas ataca na subida e novamente na queda | `CURRENT-LINE DIRECT` |
| The Rose's Secret | Blood | pétalas murchas envolvem o caster e negam brevemente dano recebido | `CURRENT-LINE DIRECT` |
| Jingle Bell | Melody/Evocation no changelog 1.21.1 | sino causa dano em área a cada toque | `CURRENT-LINE DIRECT`; registry school exato continua não verificado |
| Chain Connection | Aqua | liga dois alvos e limita a distância entre eles; movido de Evocation para Aqua em 1.0.8 | `CURRENT-LINE DIRECT VIA MOVE` |
| Fire Orbs | Fire por contexto do provider, registry individual não auditado | recebeu novo rework de impacto em 1.0.8 | `CURRENT-LINE DIRECT / VALUES UNVERIFIED` |
| Ignis Shield | escola não reconfirmada pelo trecho 1.0.8 | refeito como spell ofensivo-defensivo que retaliaria quando o usuário é atingido | `CURRENT-LINE DIRECT / SCHOOL+VALUES UNVERIFIED` |

O fix instalado 1.0.8-fix declara apenas correção das Elemental Charges de Symmetry e Spirit. Ele não publica uma nova lista de spells, então estes nomes pertencem à linha base imediatamente corrigida, mas ainda não constituem prova de registry ID/classe/valor no JAR.

## 1.0.7 — introduções públicas

| Nome público | Escola publicada em 1.0.7 | Semântica pública | Estado no catálogo atual |
|---|---|---|---|
| Guardian Connetion | Holy | liga caster a alvo; enquanto vínculo/caster persistem, alvo fica imune a dano e hits evitados são redirecionados ao caster | `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` |
| Blessed Connetion | Holy | liga dois alvos e compartilha parte da cura até expirar ou romper por distância | `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` |
| Cursed Connection | Blood | liga dois alvos e compartilha parte do dano até expirar ou romper por distância | `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` |
| Chain Connection | Evocation em 1.0.7 | limita separação dos alvos | `RENAMED SCHOOL ASSIGNMENT`: movido para Aqua em 1.0.8 |
| Bloodmark | Blood | quatro casts marcam pontos; cast seguinte liga os pontos em zona de sangue persistente que causa dano | `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` |
| Water Control | Aqua | mantém massa de água suspensa à frente do caster acompanhando a mira durante channel | `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` |
| Firestorm Vortex | Fire | vortex no alvo puxa inimigos para dentro e os queima ao longo do tempo | `INTRODUCED-HISTORICAL / CURRENT REGISTRY UNVERIFIED` |

O changelog 1.0.7 dizia que Guardian/Blessed/Cursed Connection exigiam Mowzie's Mobs para ficarem disponíveis. O pack atual contém Mowzie's Mobs 1.8.2, mas a disponibilidade exata 1.0.8-fix não foi reconfirmada em registry/runtime e permanece fail-closed.

## 1.0.6 — migrações Aqua explicitamente publicadas

| Nome | Estado |
|---|---|
| Tsunami | `REMOVED` em 1.0.6; não tratar como spell atual |
| Tidal Grasp | `RENAMED` → Ceraunus Grasp |
| Ceraunus Grasp | nome sucessor publicado; presença exata 1.0.8-fix ainda registry-pending |
| Tidal Dash | `RENAMED` → Ceraunus Dash |
| Ceraunus Dash | nome sucessor publicado; presença exata 1.0.8-fix ainda registry-pending |

## Outros nomes publicamente referenciados na linha

- `Missionary Rain` aparece no changelog 1.0.5 apenas como alvo de uma configuração de remoção. Isso prova que o nome fazia parte da superfície daquela linha, mas **não** prova presença/estado atual 1.0.8-fix.
- `Evocation Fortitude` aparece em 1.0.4 como `Evocation Charge`, recebendo Summon Damage. Tratar como charge/system reference até registry atual ser auditado, não como spell comum por inferência.

## Campos que continuam bloqueados para todos os nomes

Salvo quando o changelog publica uma semântica específica:

- registry ID;
- classe Java/inheritance;
- min/max level;
- rarity;
- mana/cooldown/cast time;
- fórmulas de dano/heal;
- range/radius/duration;
- targeting/PvP/boss rules;
- acquisition/loot/crafting;
- packet/persistence/state implementation;
- API/hook estável.

## Consequência para deduplicação

A ausência de um nome neste arquivo não prova lacuna semântica. O publisher declara `50+` spells, enquanto este documento contém apenas nomes explicitamente demonstráveis por changelogs. Até o registry exato estar disponível, o restante do espaço Somake deve ser tratado como **unknown occupied provider space**.