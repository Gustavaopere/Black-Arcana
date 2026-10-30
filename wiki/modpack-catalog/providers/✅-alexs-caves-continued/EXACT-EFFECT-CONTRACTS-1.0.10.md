# Alex's Caves Continued 1.0.10 — contratos dos oito mob effects

Este recorte cobre os **oito efeitos próprios registrados por `ACEffectRegistry`**, com uma ficha por efeito e seus consumidores. Não são oito novos spells: os efeitos podem ser aplicados por itens, projéteis, mobs, comida ou poções. As [oito ações sobrenaturais](actions/INDEX.md) mantêm suas identidades anteriores.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A fonte pública adjacente `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sem paridade demonstrada com esse JAR. [Proveniência e limites](EXACT-TECHNICAL-CONTRACTS-1.0.10.md#diferença-entre-fonte-e-release).

| Campo de `ACEffectRegistry` | Ficha individual | Fronteira a preservar |
|---|---|---|
| `BUBBLED` | [Bubbled](effects/bubbled.md) | Aplicação, ar, movimento e representação visual |
| `DARKNESS_INCARNATE` | [Darkness Incarnate](effects/darkness-incarnate.md) | Ativação, voo, dano, ambiente e remoção |
| `DEEPSIGHT` | [Deepsight](effects/deepsight.md) | Duração e renderização versus autoridade de combate |
| `IRRADIATED` | [Irradiated](effects/irradiated.md) | Amplifier, agendamento de dano, exaustão e cura |
| `MAGNETIZING` | [Magnetizing](effects/magnetizing.md) | Sincronização visual versus consumidores de movimento |
| `RAGE` | [Rage](effects/rage.md) | Atributos, seleção de alvo e consumidores do status |
| `STUNNED` | [Stunned](effects/stunned.md) | Duração, movimento, ações e gates cliente/servidor |
| `SUGAR_RUSH` | [Sugar Rush](effects/sugar-rush.md) | Atributos, movimento, tick rate local e encerramento |

Cada ficha documenta identidade, comportamento/lifecycle, parâmetros, targeting, custos/aquisição, integração e validação. Duração e amplifier pertencem ao caminho de aplicação: um efeito não recebe uma duração universal deduzida do nome. Uma partícula, mensagem visual ou alteração da câmera não prova dano, hitbox ou alcance servidor. Referências auxiliares têm escopo explícito nas fichas; este recorte não encerra o catálogo de todos os itens, mobs ou poções que as aplicam.

## Reprodução

O [manifesto selado](EXACT-EFFECT-CONTRACTS-1.0.10.json) associa as oito fichas aos hashes dos membros exatos do JAR, descritores JVM e instruções selecionadas por offset. A inspeção é estática: ela não executa o Minecraft nem valida configuração carregada, PvP, multiplayer ou compatibilidade com os demais mods.

```sh
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile effects \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-EFFECT-CONTRACTS-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
```

A CI confere hashes do artefato, fichas e membros, owner da classe declarada, descriptors e âncoras. Uma âncora isolada não certifica toda a interpretação causal: a revisão técnica acompanha essas evidências. O perfil `actions` continua validando as oito ações anteriores, com manifesto separado e sem mudar seus hashes.

## Estado e próximos escopos

**`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`** limita a certificação aos contratos documentados. **Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; universo do provider: aberto.** Cast, custo, dano, status, atributos, voo e tick rate continuam sob autoridade de seus sistemas nativos. Não há adapter RPG/Black Arcana implementado por esta documentação.

O [índice de efeitos](effects/INDEX.md) registra o recorte concluído. O [índice do provider](INDEX.md), o [índice global](../INDEX.md) e a [fila alfabética](PERK-INTEGRATION-SCOPE-1.0.10.md) distinguem esse resultado do fechamento integral. Armas, armaduras, enchantments, damage types, poções e outros sistemas ainda precisam de disposição própria antes de avançar ao próximo provider.
