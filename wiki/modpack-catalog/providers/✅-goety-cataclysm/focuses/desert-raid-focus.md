# Goety Cataclysm 1.21.1-1.8.2 — `DESERT_RAID_FOCUS`

Estado: **✅ CATALOGADO / `COUNTED_EXACT`** pela auditoria de JAR hash-matched; **⚠️** mecânicas, valores de balanceamento, registry ID executável e QA físico continuam condicionados.

## Identidade comprovada

- **Provider dono do conteúdo:** Goety Cataclysm, mod ID `goety_cataclysm` (addon sobre Goety + L_Ender's Cataclysm).
- **Focus holder observado:** `DESERT_RAID_FOCUS` — identificador factual de campo de Focus registrado no artefato. **Não converter automaticamente em `ResourceLocation` ou ID de spell do host**.
- **Posição na lista exata:** 12/28 (ordem editorial, não ID/ordem de carregamento).
- **Artefato instalado e auditado:** `goety_cataclysm-1.21.1-1.8.2.jar`, Minecraft 1.21.1 / NeoForge, SHA-1 físico = publisher `4e3052a082200371b36e1a88fdce05e294d82757`, CurseForge project/file `1224214 / 8518940`.
- **Registro:** um dos 28 Focus holders incondicionais no initializer auditado (0 branches, 0 referências a `GCSpellConfig` e 0 flags enable/disable-like registradas na verificação restrita).
- **Aquisição documentada:** cada um dos 28 Focuses possui **uma receita de aquisição no JAR**; o conjunto total é 24 `goety:ritual` e 4 crafting normal. **Qual dessas duas vias pertence a este Focus individual: NÃO VERIFICADO** a partir do inventário preservado.
- **Contagem semântica:** um dos **28 `COUNTED_EXACT` já contabilizados** do addon; esta ficha adiciona **+0 novas identidades**. A receita de aquisição não se soma novamente como um ritual independente.

## Limites da evidência

- **Classe concreta da magia, registry ID runtime, escola, efeito real, Soul Energy numérica, cast time, cooldown, alcance, targeting, dano, invocações, world safety, recipe ingredients, research e condições reais de Survival:** **NÃO VERIFICADO nesta ficha**. A denominação do holder não comprova essas mecânicas.
- **Evidência de componente:** o JAR exato comprova o Focus e a presença de aquisição em pacote. O conteúdo do modpack com configuração implantada, gameplay do cliente e servidor e interop com as demais integrações permanece **⚠️ pendente de QA físico**.
- **Rituais não-Focus:** 24 outcomes próprios adicionais foram encerrados **no agregado** (10 conversões, 13 summons/thralls, 1 fabricator), mas seus 24 caminhos e signatures individuais **não estão preservados** neste inventário. Não criar fichas individuais ou presumir IDs para esses rituais sem nova evidência.

## Autoridade e clean-room

Goety conserva Soul Energy e Focus/Staff casting, custos, ritual settlement e servant lifecycle base; Cataclysm controla os mobs/bosses base; Goety Cataclysm controla somente os Focuses/rituais/conversões do addon. Black Arcana não pode duplicar costs, efeitos, summons, recursos, hooks ou cast pipelines. Qualquer bridge futura requer contrato exato e prova causal, sob fail-closed.

A ficha contém somente identidades e limites factuais já preservados pela auditoria; **nenhum bytecode, JSON de receita, asset, tooltip ou implementação upstream** foi copiado. Licença do provider: All Rights Reserved.

**Evidência:** [README canônico](../README.md) · [auditoria hash-matched](../EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md) · [fronteiras de integração](../INTEGRATION-RULES.md).
