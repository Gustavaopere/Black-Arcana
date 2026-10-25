# Ars Nouveau 5.13.1 — 5 Forms: certificação estática para planejamento de perks

**5/5 Forms documentadas estaticamente, não 5 hooks de perks implementados.** Roster original 85 glyphs (5 Forms, 67 Effects, 13 Augments) e 24 rituais, sem novas raízes. Dentro de 2.075 fichas candidatas do catálogo, 18 receberam a certificação técnica estrita source-pinned. O universo total de mods não está fechado.

Fonte upstream imutável: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; JAR publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [prova compilada de registro](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) valida identidades e classes, **não** correspondência integral de métodos nem client/Survival.

| Form | Seleção/entrega comprovada no source fixo | Boundary |
|---|---|---|
| [Self](glyphs/forms/self.md) | EntityHitResult do caster em todos overloads; nenhum augment | ⛔ alterar para terceiros sem adapter |
| [Touch](glyphs/forms/touch.md) | Bloco/entidade ao toque; onCast genérico FAILURE; Rune entity SUCCESS_NO_EXPEND | ⛔ não converter retorno em bônus de pagamento |
| [Underfoot](glyphs/forms/underfoot.md) | Prioriza veículo, 1ª entidade na AABB inflada (0.1,1.5,0.1), ou bloco inferior | ⛔ não universalizar a seleção como alvo PvP |
| [Pantomime](glyphs/forms/pantomime.md) | BlockHitResult pela posição do olhar; distância = (2 ou 3) + offset; **não é raycast comum de colisão** | ⛔ sem hook seguro de geometry |
| [Projectile](glyphs/forms/projectile.md) | Duas formas de spawn; n=1+Split, velocity depende de acc no caminho shooter; TTL default 60 s | ⛔ não duplicar resolver/spawns |

**Não aplicáveis como escala própria da Form:** dano e DamageType final do Effect, cooldown separado de um cast, target de todos os Effects posteriores e Mastery adicional por projétil/partícula. A fonte demonstra `SpellModifierEvent` público, mas sua existência não prova contrato seguro de reescrita da seleção, do cast, dos custos e do settlement por RPG Skill Tree/Black Arcana.

**Gate:** `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; os cinco itens usam evidência local por campo no manifesto. Nenhum teste de modpack físico ou compatibilidade real ocorreu nesta rodada; Stage 06.05/09 e runtime não foram alterados.
