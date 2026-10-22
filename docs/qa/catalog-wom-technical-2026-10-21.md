# Continuação do catálogo — Weapons of Miracles 2.0.178

Base: Black Arcana `75f54b37ea329c482b43f1fa058ff5723c661f00`; RPG `ed5b65b890767b406ce41127bcb793775263c7bd`; Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`. Checkpoint 21/10/2026.

A lacuna anterior era documental: 64 IDs dispositionados, 13 fichas mágicas individuais e 51 habilidades úteis à integração sem ficha própria. A entrega adiciona **51 fichas** e enriquece as **13 existentes**; preserva classificação, owner/acquisition e +0 no numerador mágico.

## Evidência local executada

- JAR WOM: SHA-1 `b507eb376778cfd1cbecec2841c38891b26a7349`, SHA-256 `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`, 20.941.584 bytes; compatível com hash físico documentado, sem leitura de instalação ao vivo.
- Host Epic Fight 21.17.3.1: SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`, 8.578.288 bytes.
- `javap` Java 21, sem classloading dos mods. **12/12 autotestes** do verificador passaram.
- Verificador exato: **PASS_EXACT_STATIC_CATALOG**; 64 links ID→bootstrap/supplier/holder, 64 classes/fichas únicas, 58 JSONs, seis ausências, três objetos vazios, **370 descritores de métodos**, **915 referências delimitadas por método**, **64 recursos de builder**, **dez casos limitados de operandos/referências**.
- Regressões de documentação: **52/52** global magic catalog, **5/5** ledger físico e **26/26** magic pendency tracker; diff sem erros de whitespace; links locais em 67 fichas/índices/dossiês sem ausências.
- Consumidores base Skill/Guard e builders foram inspecionados no host hash-exato, sem promover source 21.17.3 a equivalência global.

Reprodução, limites e pontos de código: [dossiê técnico](../../wiki/modpack-catalog/providers/✅-weapons-of-miracles/skills/EXACT-TECHNICAL-BOUNDARIES-2.0.178.md), [índice dos 64](../../wiki/modpack-catalog/providers/✅-weapons-of-miracles/skills/INDIVIDUAL-SKILL-CARDS-2.0.178.md), [verificador](wom_20178_catalog_binary.py) e [workflow](../../.github/workflows/wom-20178-catalog-binary.yml). A descrição do PR registra HEAD, execução de CI, merge e validação posterior, evitando um checkpoint circular de SHA nesta documentação.

## Decisões e limites

A barra WOM passa a **64/64 fichas por ID**, recorte documental com evidência estática, e o painel mantém seu denominador técnico global aberto. Não somar este recorte a outras métricas. A identidade binária selecionada continua 38/39; Aeromancy físico permanece condicionado.

Casos registrados incluem Time Travel (JSON 0 versus chamada STAMINA/12), Charybdis (recurso do builder versus débito explícito/override nativo), Spider Techniques (loader próprio força 0,2), Heart Shield (MAX_SHIELD=20 em código), Voodoo (consumo negativo e possível interação com max(0,amount) no sibling), e dimensões AABB separadas de raio/colisão real.

Não houve código de produção Black Arcana, RPG ou Enshrouded alterado. Nenhum novo adapter/perk foi implementado. Rejeitar nova mudança de alvo, área, DamageType, hitbox, alcance ou tempo sem contrato real; reaproveitar os hooks genéricos RPG já presentes, respeitando elegibilidade e recurso. Config implantada, composição de listeners/recuperação, resultado de jogador conectado, PvP/claims, Survival e full pack continuam **PENDING**. Stage 06.05/09 físico não avança.
