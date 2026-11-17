# Alex's Mobs Continued 2.1.13 — ciclo de vida do portal do Dimensional Carver

**Escopo:** auditoria do classfile publisher SHA-exato, read-only, de `ItemDimensionalCarver` e `EntityVoidPortal`. **Estado:** 🟡 descoberta parcial. **Não** é certificação estática de todas as dependências, QA física, API/hook de perk ou prova de segurança do teleporte.

## Autoridades

- Modlist física do sibling, linha 021: `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod ID `alexsmobs`, Minecraft 1.21.1 / NeoForge / Java 21.
- Publisher CurseForge projeto 1635121, file 8856498: SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`; SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`; 27.452.738 bytes.
- Auditoria de referência do mesmo JAR: [EXACT-2.1.13-ARTIFACT-AUDIT.md](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-2.1.13-ARTIFACT-AUDIT.md), prova non-merge PR #511 (GitHub Actions `36949047824`), e [controle de operandos](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-CONTROL-OPERANDS-2.1.13.md).
- **A fonte pública `2.2.3` não é autoridade para o JAR `2.1.13`.** Tampouco a última release `2.2.4` altera a versão física documentada na modlist.

## Lacuna técnica e motivo

O cartão individual [Dimensional Carver Passage](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/actions/dimensional-carver-passage.md) documenta `onPortalOpen` atribuindo lifespan inicial de **1200 ticks**, controle de âncora, ray trace inicial de 1,5 bloco e cooldowns de 40/200 ticks. Porém **atribuição inicial não comprova duração efetiva**. Faltam especialmente a implementação exata de `EntityVoidPortal`, seus decrementos, invalidação, lifecycle de destino/entidade e eventual serialização, além de avaliação física de teleport/claims.

## Procedimento de coleta

[Probe read-only](alexsmobs_213_carver_portal_lifecycle_probe.py) e [12 regressões sintéticas](alexsmobs_213_carver_portal_lifecycle_probe_test.py) implementam:

1. Gate estrito de SHA-1, SHA-256, tamanho, versão JVM 65 e paths de classe `ItemDimensionalCarver` e `EntityVoidPortal` do artefato instalado;
2. Inspeção de todos os seis métodos próprios conhecidos do Carver (sem publicação de corpos completos) e descoberta **limitada** dos métodos de ciclo de vida do portal a partir do bytecode real;
3. Registros compactos de métodos, digest das instruções JVM, desvios, referências simbólicas e seus vizinhos imediatos, com limites explícitos de quantidade e bytes;
4. Manifesto JSON SHA-exato fixado **após** conferência da descoberta, replay de CI com `--snapshot` e manutenção dos índices globais sem promoção.

O [workflow](../../.github/workflows/alexsmobs-213-carver-portal-lifecycle.yml) obtém o mesmo publisher usado na prova #511, sem comitar bytes de terceiros, executa testes sob Java 21 e conferências de índices.

## Gates não satisfeitos nesta primeira coleta

`static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`. A ação é dependente da cadeia do Void Worm para obtenção normal; os parâmetros da config *implantada* e overrides permanecem `NOT_VERIFIED`.

**Proibido inferir:** dimension hopping arbitrário; bypass de claim; destino validado pelo servidor; tempo efetivo de vida igual ao valor inicial; aceitação do spawn; cardinalidade do teleporte; logout/save/reload; hook mutador; ou QA real apenas de um callsite.

Após a descoberta, qualquer afirmação substantiva nova deve indicar offset/descritor e classe revisados do classfile 2.1.13, com limites claros. Não editar Raygun/X-Ray ou os índices 80/81 do Alex's Caves.
