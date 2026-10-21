# Blood Cut 1.0.9 × Iron's 3.16.3 — despacho virtual e lifesteal nominal

**Estado:** ✅ `SHA_EXACT_VIRTUAL_DISPATCH_WITH_015F_SETTER`; ⚠️ cura efetivamente entregue, caps/host settlement e QA físico; ⛔ perks mutadoras sem API real.

## Proveniência física

| Provider | Artefato exato | Hash validado |
|---|---|---|
| Somake Spells 1.0.9 | CurseForge File `8867079`, `somakespells-1.0.9-1.21.1.jar` | SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` |
| Iron's Spellbooks 3.16.3 | API oficial addon-facing `irons_spellbooks-1.21.1-3.16.3-api.jar` | SHA-256 `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad` |

[GitHub Actions Java 21 #39613550972](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39613550972): **SUCCESS**, os dois artefatos hash-pinned e **97 testes sintéticos** no total (7+9+5+10+10+10+22+13+11). Inspeção: [verificador](../../../../docs/qa/somake_109_blood_cut_irons_dispatch.py), [regressões](../../../../docs/qa/somake_109_blood_cut_irons_dispatch_test.py) e [workflow](../../../../.github/workflows/somake-109-blood-cut-refs.yml). Nenhum JAR, classfile, implementação proprietária ou método descompilado foi adicionado ao repositório.

## Relação exata entre as duas sobrecargas

A auditoria identificou as duas assinaturas JVM distintas:

- **Iron's**, `AbstractSpell.getDamageSource(Entity):SpellDamageSource`: **5 instruções JVM**. A sequência de opcodes `aload_0`, `aload_1`, `aload_1`, `invokevirtual`, `areturn` passa o **mesmo Entity duas vezes** para `getDamageSource(Entity,Entity):SpellDamageSource`. O opcode `invokevirtual` realiza resolução virtual em receiver `this`.
- **Somake**, `BloodCutSpell.getDamageSource(Entity,Entity):SpellDamageSource`: **7 instruções JVM**. A sequência `aload_0`, `aload_1`, `aload_2`, `invokespecial`, `ldc`, `invokevirtual`, `areturn` chama a implementação-base com os dois Entity, depois carrega `float 0.15f` e invoca `SpellDamageSource.setLifestealPercent(float)`, devolvendo a referência retornada por esse setter.

O JAR comprova que `BloodCutSpell` estende diretamente `AbstractSpell`. Consequentemente, o callsite `BloodCutSpell.getDamageSource(Entity)` do evento Post (ver [prova do callsite](EXACT-BINARY-BLOOD-CUT-APPLY-DAMAGE-1.0.9.md)) encontra o método de um argumento herdado. Quando executado num receiver `BloodCutSpell`, o `invokevirtual` interno resolve para a **sobrecarga de dois argumentos declarada em BloodCutSpell**, passando a mesma `Entity` como origem e segundo argumento.

A sequência de despacho compilada certificada pode ser representada semanticamente:

```text
AbstractSpell.getDamageSource(e)
  → [invokevirtual sobre receiver BloodCutSpell] getDamageSource(e, e)
  → BloodCutSpell.getDamageSource(e, e)
  → super.getDamageSource(e, e)
  → SpellDamageSource.setLifestealPercent(0.15f)
```

Essa reconstrução representa **resolução de sobrecarga e despacho JVM**, não transcrição do código do provider. Os testes falham diante de mudança de `invokevirtual` para `invokespecial` no método de um argumento, mudança dos loads, divergência da assinatura, mudança do literal `0.15f`, drift da chamada super e mudança do setter.

## Significado e limites

**Certificado:** o caminho compilado que constrói a fonte do dano secundário no `LivingDamageEvent.Post` chega ao setter `setLifestealPercent(0.15f)`, com o mesmo `Entity` encaminhado duas vezes pelo host.

**Não certificado:** o percentual da vida efetivamente recuperada, a identidade final do beneficiário, se o booleano de `applyDamage` representa aplicação bem-sucedida, efeitos de armadura/proteção/invulnerabilidade, regras PvP/claims, composição com outros handlers, tetos internos e a fórmula do processamento do lifesteal. Também não foi executado servidor com ambos os providers carregados neste lote.

O host Iron's permanece autoridade sobre a semântica efetiva de `SpellDamageSource`, `DamageSources.applyDamage` e liquidação de dano/cura. Somake controla o efeito Blood Cut. Black Arcana não substitui esse pipeline. RPG Skill Tree é apenas provider de atributos/Mastery/perks mediante boundary real.

## Consequências para integração

- **Dano:** o [dossiê causal](EXACT-BINARY-BLOOD-CUT-CAUSAL-EVENT-1.0.9.md) preserva `event.getNewDamage * (((float)(amplifier + 1) * getEntityPowerMultiplier(sourceEntity)) * 0.1f)` como valor intermediário solicitado; não confundir com dano final.
- **Alvo:** o [dossiê applyDamage](EXACT-BINARY-BLOOD-CUT-APPLY-DAMAGE-1.0.9.md) certifica `event.getEntity()` como alvo e `getDamageSource(sourceEntity)` como fonte, mas não substitui testes de targeting.
- **Perks de lifesteal:** o parâmetro nominal `0.15f` agora está vinculado estaticamente ao caminho de dano secundário. Falta contrato mutador efetivo por jogador/caster; não introduzir setter paralelo nem repetir hit por conta própria.
- **Mastery/proc chains:** não atribuir segundo settlement, custo ou Mastery a partir da simples execução do setter ou do callsite de dano. O handler descarta o retorno booleano de `applyDamage`.

**Status de engenharia:** +0 magias, +0 adapters e nenhum hook por jogador; Somake **83/83 IDs registrados**, recorte técnico estático **8/83**, aprofundamento downstream anterior **5/83**, global **—%** (universo ainda aberto, piso conservador ≥1.856). Stage 06.05 🟡, Stage 09 físico PENDING.

**Próxima prova necessária:** estudar o processamento do percentual de lifesteal no JAR/API host da versão exata e realizar QA provider-loaded, incluindo dano, cura real, PvP, absorção, resistência, invulnerabilidade e reinício.
