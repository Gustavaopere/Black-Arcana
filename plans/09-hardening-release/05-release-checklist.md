# 09.05 — Release Checklist

Before release:

- [ ] clean build/test/CI green;
- [ ] dedicated-server smoke green;
- [ ] exact dependency/recommended-mod versions documented;
- [ ] default config reviewed for grief/OP behavior;
- [ ] migration notes written and upgrade tests green;
- [ ] known incompatibilities documented;
- [ ] no debug content/commands exposed unintentionally;
- [ ] changelog and version aligned;
- [ ] `LICENSE`, `SOURCES.md` and `THIRD_PARTY_NOTICES.md` are current;
- [ ] built JAR contains Black Arcana `LICENSE` and `THIRD_PARTY_NOTICES.md`;
- [ ] clean-room audit confirms no Mahou Tsukai code/assets/text/models/sounds/implementation material was imported;
- [ ] every actual `DERIVED_CODE`/`DERIVED_ASSET` record has exact upstream revision/file/license/permission/notice evidence;
- [ ] no actual derived material remains `REVIEW_REQUIRED`, `PERMISSION_REQUIRED` or unknown;
- [ ] third-party API/dependency targets match the compatibility matrix and do not leak optional classes into standalone startup;
- [ ] player-facing terminology/assets pass the Stage 01 identity/provenance check;
- [ ] provenance/license audit (`09.06`) is green.

A release is not complete because a JAR exists; all release-blocking checklist items must be verified on the exact release HEAD.
