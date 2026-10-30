# Alex's Caves Continued — catálogo técnico 1.0.10

**Ações sobrenaturais: 8/8 contratos técnicos estáticos documentados.** [Índice de ações](actions/INDEX.md) · [evidência binária](EXACT-TECHNICAL-CONTRACTS-1.0.10.md) · [manifesto dos contratos](EXACT-TECHNICAL-CONTRACTS-1.0.10.json).

**Mob effects: 8/8 contratos técnicos estáticos documentados.** [Índice de efeitos](effects/INDEX.md) · [evidência e reprodução](EXACT-EFFECT-CONTRACTS-1.0.10.md) · [manifesto dos efeitos](EXACT-EFFECT-CONTRACTS-1.0.10.json). As fichas distinguem aplicações, atributos, dano, targeting, movimento, consumidores e cleanup; não acrescentam raízes mágicas.

**Damage types (recursos exatos):** 11/11 JSONs e seis arquivos de tags inventariados ([fichas](damage-types/INDEX.md), [manifesto](damage-types/EXACT-RESOURCE-MANIFEST-1.0.10.json)). **0/11** possui consumidor Java/contrato técnico completo certificado. Trata-se de classificação de dano e não de 11 magias adicionais.

**Catálogo integral do provider: pendente.** As famílias concluídas ainda não abrangem armas, armaduras, enchantments e outros sistemas integráveis por perks. [Escopo e trabalho restante](PERK-INTEGRATION-SCOPE-1.0.10.md), [inventário exato das famílias](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) e [índice geral](../INDEX.md). A fila alfabética permanece neste provider.

## Identidade e versões

- Artefato: `alexscaves-1.0.10-neoforge+1.21.1.jar`, mod id `alexscaves`, Minecraft 1.21.1 / NeoForge.
- Fingerprint físico/publicador: SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes.
- Publisher: CurseForge projeto `1645389`, arquivo `8856293`; autoridade física histórica: linha #19 do sibling.
- Dependência declarada no JAR: CodxLib `[1.3.6,)`; o pack registra CodxLib 1.6.0. Compatibilidade em execução continua pendente.
- Fonte pública usada anteriormente: commit `523308608422ab8e31974befa7111ecdf495dd37`, que declara **1.1.1**. Seus parâmetros não são tratados como 1.0.10. Os contratos atuais usam bytecode/dados do JAR exato; [distinção de autoridades](EXACT-TECHNICAL-CONTRACTS-1.0.10.md#diferença-entre-fonte-e-release).

## Oito raízes e seus contratos

| Ação | Ficha | Eixos úteis para perks |
|---|---|---|
| Water Bolt | [Sea Staff](actions/sea-staff-water-bolt.md) | Dano, homing, busca/colisão, cooldown e custo |
| Peppermint Cast | [Sugar Staff](actions/sugar-staff-peppermint-cast.md) | Quantidade, órbita, movimento, dano, duração e save/load |
| Hex Cast | [Sugar Staff Hex](actions/sugar-staff-hex-cast.md) | Posição, área/escala, dano, duração e owner |
| Summon Deep Ones | [Magic Conch](actions/magic-conch-summon-deep-ones.md) | Charge, seleção dos summons, custo, duração e ownership |
| Possession / Control | [Totem](actions/totem-possession-remote-control.md) | Binding, geometria de olhar, movimento, ataque, desgaste e sincronização |
| Remote Observation | [Occult Gem + Beholder](actions/occult-gem-beholder-observation.md) | Binding, autoridade do pacote, câmera, tickets e cleanup |
| Darkness Incarnate | [Cloak of Darkness](actions/cloak-darkness-incarnate.md) | Carga, ativação, voo, duração, ambiente e remoção |
| Biome Conversion | [Conversion Crucible](actions/conversion-crucible-biome-conversion.md) | Ofertas, tempo, largura/bioma quart, fila de blocos e persistência |

São **8 COUNTED_EXACT**, já integrantes do ledger semântico; esta revisão acrescenta **0 raízes**. Sugar Staff tem duas ações escolhidas pelo jogador. Binding/gestão do Totem, variantes de Deep Ones, cores, enchants e passos do Crucible são parâmetros/consequências, não novos spells.

As fichas cobrem identidade, comportamento, parâmetros, targeting, custos, integração e validação. A certificação limita-se a **STATIC_TECHNICAL_CATALOG_ONLY** / **SHA_EXACT_BINARY_BEHAVIOR**. Hooks mutadores continuam **NOT_VERIFIED** e QA física **NOT_TESTED**. Nenhum adapter ou Stage é promovido por esses certificados.

## Aquisição e autoridade

O inventário anterior identifica Sea Staff no barter de Deep One Mage, Sugar Staff no loot de Licowitch, Magic Conch no barter de Deep One Knight, Occult Gem no loot de Forlorn/Watcher e receitas de Beholder, Totem, Cloak/Hood, Crucible e Biome Treat. As fichas atuais distinguem dados empacotados, condições de uso e valores dependentes da configuração; existência da receita não prova aquisição executada em Survival.

O Biome Treat pode armazenar uma chave de bioma válida; o nome do componente `CaveBiome` não comprova whitelist restrita às seis cavernas. O Crucible converte um ciclo por vez; bioma, ofertas, sacrifício, ticks e alterações de blocos são partes dessa raiz. A busca de jogadores para advancement não define o raio da mutação de bioma.

Alex's Caves mantém autoridade sobre cast, custo, cooldown, dano, movimento, AI, voo, câmera, tickets e alteração de mundo. Black Arcana/RPG Skill Tree não devem repetir settlement, invocar entidades em duplicidade ou presumir que um setter permita mutação por jogador. Casos de multiplayer, autorização de rede, proteção de mundo, cleanup e reload continuam no plano de QA das fichas.

## Histórico preservado

A [auditoria de identidade do artefato](EXACT-1.0.10-ARTIFACT-AUDIT.md), a [disposição semântica de 42 classes](ITEM-ACTION-DISPOSITION-1.0.10.md), o [checkpoint de materialização](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md) e o [resumo de identidades](actions/SUPERNATURAL-ACTION-CARDS.md) permanecem como histórico. As PRs #944 e #945 foram preservadas e aprofundadas pelo exame binário exato; a fonte 1.1.1 ficou identificada como corroboração adjacente. O JAR e os assets do provider não são distribuídos neste repositório.
