# Phantom Charge

**Dossiê documental — 27/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`, lógica `RELEASE_BOUNDED_SOURCE / SOURCE_CAUSALITY`, integração `CONDITIONAL / CONTRATO_CONDICIONAL`, QA físico `PENDING`. **+0 identidades/+0 strict**: entidades, efeitos e impactos derivados continuam filhos desta spell.

## Identidade, proveniência e ingresso

Provider ISS: Magic From The East, `mod_id=iss_magicfromtheeast`; spell **`iss_magicfromtheeast:phantom_charge`**, escola default **`iss_magicfromtheeast:spirit`**. Declarante `net.warphan.iss_magicfromtheeast.spells.spirit.PhantomChargeSpell`. [Registro][registry], [escola][school].

JAR de referência MC 1.21.1/NeoForge **`iss_magicfromtheeast-1.1.5.jar`**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`, 1.680.780 bytes; [publisher CF7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), [inventário binário histórico](../EXACT-BINARY-SPELLS-1.1.5.md). Candidato oficial de source **`WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`**, 27/12/2025, anterior ao upload publicado: lógica **`RELEASE_BOUNDED_SOURCE`**, sem equivalência integral demonstrada entre source e métodos do JAR. Data e versão iguais não provam essa equivalência. O candidato declara 1.1.5, NeoForge 21.1.187/Iron’s 3.14.8; o pack usa NeoForge 21.1.250/Iron’s 3.16.3. Os contratos do host abaixo vêm de Iron’s 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`, portanto sua combinação também exige teste. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-1.1.5.md). Defaults não fecham a config implantada. Metadata **All Rights Reserved**; MIT do template tem escopo limitado ao template. Só fatos, paráfrases e permalinks, sem importar implementação ou assets.

**Corroboração binária estreita:** `PhantomChargeSpell#getUniqueInfo` divide power por 2, mas `onCast` entrega power sem essa divisão a `PhantomCavalryVisualEntity#setDamage`, dentro do laço limitado por L. O constructor grava power 6/+2 e mana 45/+15. A inspeção confirma essa diferença entre apresentação e valor entregue, sem homologar o dano físico ou os métodos completos. [Limites da evidência](../SPELL-PERK-BOUNDARIES-1.1.5.md).

Esta classe não sobrescreve aquisição, aprendizado ou resolver de pre-cast. A escola usa constructor host com requiresLearning=false/allowLooting=true; crafting ainda depende da config e origem/admissão do host. Isso é elegibilidade, sem garantir scroll/rota Survival. [Spell][spell], [constructor escolar][school-constructor], [aquisição host][acquisition-host].

[Guia][guide], parafraseado: cria uma formação de cavalaria espectral que avança à frente. A entidade é um projétil de contato, não summon com AI/slots só por ter cavalo/samurai no visual.

## Defaults e pipeline causal

`P=(6+2(L−1))×SPELL_POWER×spiritPower×POWER_MULTIPLIER`. Max default 6, mana neutra 45–120, P6–16. **Tooltip mostra P/2=3–8**, mas onCast grava **D=P=6–16** em cada cavalry, e o contato lê esse damage. Preservados valor anunciado e consumer efetivo source, sem escolher um como balanceamento físico homologado. [Spell][spell], [spawn][spawn], [contato][collision], [power][power].


Os níveis máximos acima são defaults de configuração; este `onCast` não aplica clamp local de L. As fórmulas `int(...)` usam conversão Java para inteiro (truncamento em direção a zero nos valores positivos usuais). Mudar L em evento posterior não refaz admissão, custo anterior ou estado já capturado pelo host. [AbstractSpell#getManaCost/getSpellPower/getEffectiveCastTime][power], [AbstractSpell#castSpell][cast-host].
1. **Cast/custo:** INSTANT, 0 ticks, mana `int((45+15(L−1))×MANA_MULTIPLIER)`, cooldown 80s=1600 ticks antes de modifiers. Sem recast/charges. No wrapper jogador, evento/mana precedem criar os filhos; recusar um spawn não tem refund local demonstrado. [Defaults][spell], [host][cast-host].
2. **Formação:** laço i=1..L cria L `PhantomCavalryVisualEntity`. orth horizontal unitário vem do yaw; offset=orth×i se i par, orth×(−i+1) se ímpar. Defaults dão centros laterais0,+2,−2,+4,−4,+6 blocks, na altura/posição base do caster. Não é distribuição simétrica para todoL nem seleção de alvo remoto. P é consultado para cada filho no loop. Cada spawn retorna boolean ignorado. [Spawn][spawn].
3. **Constructor/velocidade:** tipo `iss_magicfromtheeast:phantom_cavalry`, dimensões1.2×2.5 blocks. Constructor faz noPhysics=true→**super.tick antes de owner/posição/dano**→noPhysics=false→noGravity=true. Depois recebe owner e posição acima, shoot(lookAngle com Y0), D=P. Host shoot só multiplica por getSpeed=1, sem normalizar de novo: módulo horizontal nominal=cos(pitch), até1block/tick; não afirmar 1 block/tick em qualquer pitch. Sem inaccuracy, aceleração ou homing ativados pela spell. Host não condiciona hitDetection/travel a noPhysics. [Constructor/tick][entity-code], [tipo][entity], [host][projectile-host].
4. **Scan:** block clip do segmento position→position+delta; quando não-MISS chama onHit(block), senão consulta overlap da **AABB atual.inflate0.25**, nominalmente1.7×3×1.7 blocks. canHitEntity herda filtros owner/aliados/Minecraft. Não há LOS/cap/ordenação/ledger local, swept entity ray ou ProjectileImpactEvent publicado nesse override; callback não possui guarda server local. [Scan][collision], [base][projectile-host].
5. **Contato:** chama super.onHitEntity; para Living, pede ignoreNextKnockback e Slowness/Weakness **80 ticks=4 s, amplifier0** antes do dano, sem testar hurttrue. Depois tenta applyDamage(D, fonte PhantomCharge, direta=cavalry/causador=getOwner atual). Com Living+SpellDamageSource há evento mutável/cancelável e resistência/friendly/hurt. Cancelar dano não desfaz por si as tentativas de debuff já feitas. Não há discard local por entity hit: repetição em ticks seguintes é possível. [Contato][collision], [helper][damage-host], [knockback][knockback].
6. **Saída:** tick executa super primeiro, som de galope a cada 10 enquanto tickCount<35 no servidor, depois discard se **tickCount>40**. Último tick pode executar scan/movimento antes do descarte. Isso não é garantia de40 blocks de alcance ou40acertos. AntiMagic, despawn por chunk e NBT Damage/Age são herdados; lifecycle cliente/persistência efetiva precisam QA. [Tick][entity-code], [state][projectile-state].

## Matriz para perks

| Eixo | Valor, consumer e fase | Superfície real / limite | QA |
| --- | --- | --- | --- |
| Dano/power | D=P por filho; UI=P/2; defaultL 1–6. [Spell][spell], [spawn][spawn], [contato][collision]. | SPELL_POWER/spirit_spell_power **NATIVE_ATTRIBUTE**, POWER_MULTIPLIER **CONFIG_NATIVE**; helper Living aceita SpellDamageEvent amount/cancel **HOOK_VERIFICADO**, adapter por cavalry/spell/owner **CONDITIONAL**. Não normalizar UI por perk. | Q1/Q3 |
| Tipo/crítico | SpellDamageSource default spirit_magic, owner atual na colisão; sem crítico próprio. [Fonte][source], [tipo][source-type]. | Evento não altera DamageType; conversão/crítico/reownership por perk **⛔ SEM_HOOK_SEGURO** sem contrato separado de autoria/procs. | Q3 |
| Alvo/alcance/área | Formação lateral, nenhum target adquirido; overlap1.7×3×1.7 nominal por filho. [Spawn][spawn], [scan][collision]. | Sem cap global/ledger/LOS local; retarget/área/largura **⛔ SEM_HOOK_SEGURO**. Tracking64 não é alcance ofensivo. | Q2 |
| Projétil/contagem | L filhos,1.2×2.5 registrado, delta horizontal até1, noGravity, clock>40. [Tipo][entity], [entity][entity-code]. | Contagem é nível usado pelo loop; public setDamage/homing/pierce por instância não provam callback pré-constructor. Homing/pierce não são setters seguros do scan custom. Resize/speed/count independente **⛔ SEM_HOOK_SEGURO**. | Q2/Q4 |
| Tempo/cooldown | 0cast;80sdefault;>40 após super; base>300. [Spell][spell], [tick][entity-code]. | Cooldown config/atributo/evento host no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md) não muda clock40 ou duração de debuff. Nenhum setter local de lifetime identificado. | Q1/Q4 |
| Mana/recast | `int((45+15(L−1))×config)` inicial, sem recast/custo de cada cavalry. [Power][power], [wrapper][cast-host]. | setManaCost/setSpellLevel host reais, mas mudarL não recalcula admissão/custo anterior. Não cobrar por filho nem criar fallback quando spawn falha. | Q1 |
| Debuff/knockback | Slowness 80/amp 0, Weakness 80/amp 0 e ignoreNextKnockback pedidos antes de helper. [Contato][collision]. | Amount/cancel de dano não muta esses literals ou confirma aplicação. Duração/força por jogador **⛔ SEM_HOOK_SEGURO** nesta entidade; listeners/merge ainda downstream. | Q3 |
| Summon/mundo/persistência | Cavalry é projétil, slots/AI **N/A**; sem heal/fire/block mutation própria; state host Damage/Age. [State][projectile-state]. | Provider mantém cleanup/owner/entidades. Dedup por UUID/fase/tick/vítima; não Mastery por cada cavalry/debuff/partícula. Escola custom condicionada no [comum](../SPELL-PERK-BOUNDARIES-1.1.5.md). | Q4/Q5 |

Assinatura ocupada: parede de múltiplos projéteis espectrais que avança e aplica debuffs por contato. Uma magia original precisa declarar orçamento, trajetória e repetição próprios, sem tomar VFX como summon autônomo.

- **Q1:** mana/origem/config/Survival, L/power e divergência UI/armazenado, listeners entre spawns, quantidade pedida versus aceita.
- **Q2:** pitch/cos, posições0,+2,−2…, gaps/cantos/solo/blocos, constructor antes de init, owner/aliados/PvP/claims e limites de entidade/targets.
- **Q3:** debuffs em dano vetado/resistido, merges/iFrames/knockback, mesmas vítimas por tick, fonte após reflexão/reownership, kill credit.
- **Q4:** clocks40/300/primeiro-último tick, antiMagic/chunks/NBT/relog/restart e som cliente/servidor.
- **Q5:** dedicado/cliente/multiplayer/Survival/sync e correlação do cast pai. **Todos PENDING**, sem adapter/runtime novo.

[registry]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESpellRegistries.java#L24-L50
[versions]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/gradle.properties#L11-L36
[power]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L257
[cast-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[acquisition-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L634
[school-constructor]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/SchoolType.java#L30-L44
[school]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTESchoolRegistries.java#L32-L54
[source]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L560-L565
[source-type]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/SpellDamageSource.java#L24-L51
[damage-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L64
[damage-event]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellDamageEvent.java#L24-L50
[guide]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/resources/assets/iss_magicfromtheeast/lang/en_us.json#L53-L54
[spell]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/PhantomChargeSpell.java#L24-L62
[spawn]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/spells/spirit/PhantomChargeSpell.java#L74-L95
[entity]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/registries/MFTEEntityRegistries.java#L138-L142
[entity-code]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/phantom_cavalry/PhantomCavalryVisualEntity.java#L35-L86
[collision]: https://github.com/WarPhan78/ISS_MagicFromTheEast-1.21.x/blob/f2a095cbbc89f8d8428dca758140663adf54ae88/src/main/java/net/warphan/iss_magicfromtheeast/entity/spells/phantom_cavalry/PhantomCavalryVisualEntity.java#L88-L119
[projectile-host]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L78-L114
[projectile-state]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L289-L359
[knockback]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L67-L88
[setters]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/AbstractMagicProjectile.java#L445-L499
