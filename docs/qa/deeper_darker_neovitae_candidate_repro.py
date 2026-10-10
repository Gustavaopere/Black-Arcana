#!/usr/bin/env python3
"""
Evidence-only clean-room reproduction audit for Deeper and Darker 1.4.1.

Downloads the official public release JAR at runtime, verifies its published
fingerprint, then generates bounded candidate repacks that only change
deeperdarker.mixins.json. It emits TEXT/JSON evidence only; candidate JARs are
temporary and must not be uploaded or committed.

This script does not assert that any candidate equals the deployed pack unless
its SHA-1 exactly matches the physical authority:
83f7edd0a8516b2767c2cda7a3b2402f9e290d88
"""

from __future__ import annotations

import argparse
import binascii
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import tempfile
import urllib.request
import zipfile
import zlib

OFFICIAL_URL = (
    "https://github.com/KyaniteMods/DeeperAndDarker/releases/download/"
    "v1.4.1/deeperdarker-neoforge-1.21.1-1.4.1.jar"
)
OFFICIAL_SIZE = 3_906_057
OFFICIAL_SHA1 = "b6094adde68bd4b909bc75c64901e1f3fb99ad8f"
OFFICIAL_SHA256 = "eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af"

PHYSICAL_SHA1 = "83f7edd0a8516b2767c2cda7a3b2402f9e290d88"
KNOWN_LOCAL_FIRST_SIZE = 3_906_052
KNOWN_LOCAL_V2_SIZE = 3_906_044

MIXIN_PATH = "deeperdarker.mixins.json"
EXPECTED_MIXINS = [
    "ContainerMenuMixin",
    "HangingEntityItemMixin",
    "PaintingMixin",
    "PlayerMixin",
    "ServerGamePacketListenerImplMixin",
    "ServerPlayerMixin",
    "VibrationListenerMixin",
    "WardenMixin",
]

EOCD_SIG = b"PK\x05\x06"
LOCAL_SIG = b"PK\x03\x04"
CENTRAL_SIG = b"PK\x01\x02"
DD_SIG = b"PK\x07\x08"


def sha1_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download_official(dst: Path) -> None:
    req = urllib.request.Request(
        OFFICIAL_URL,
        headers={
            "User-Agent": "Black-Arcana-clean-room-audit/1.0",
            "Accept": "application/octet-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as response, dst.open("wb") as out:
        shutil.copyfileobj(response, out)


def verify_official(data: bytes) -> dict:
    result = {
        "size": len(data),
        "sha1": sha1_bytes(data),
        "sha256": sha256_bytes(data),
    }
    assert result["size"] == OFFICIAL_SIZE, result
    assert result["sha1"] == OFFICIAL_SHA1, result
    assert result["sha256"] == OFFICIAL_SHA256, result
    return result


def load_mixin_json(jar_path: Path) -> tuple[zipfile.ZipInfo, bytes, dict]:
    with zipfile.ZipFile(jar_path, "r") as zf:
        info = zf.getinfo(MIXIN_PATH)
        raw = zf.read(info)
    parsed = json.loads(raw.decode("utf-8"))
    assert parsed["mixins"] == EXPECTED_MIXINS, parsed["mixins"]
    return info, raw, parsed


def transform_json(raw: bytes, remove: tuple[str, ...]) -> bytes:
    text = raw.decode("utf-8")
    parsed = json.loads(text)
    parsed["mixins"] = [x for x in parsed["mixins"] if x not in set(remove)]

    # Preserve the publisher's actual newline convention and all untouched
    # formatting. Remove only the full list lines whose normalized content is
    # the requested mixin name. This supports both LF and CRLF release JARs.
    lines = text.splitlines(keepends=True)
    for name in remove:
        targets = {f'"{name}",', f'"{name}"'}
        matches = [
            index
            for index, line in enumerate(lines)
            if line.strip() in targets
        ]
        if len(matches) != 1:
            raise AssertionError(
                f"expected exactly one mixin line for {name!r}, found {len(matches)}"
            )
        del lines[matches[0]]

    text = "".join(lines)
    roundtrip = json.loads(text)
    assert roundtrip["mixins"] == parsed["mixins"]
    return text.encode("utf-8")

def rewrite_zipfile(
    jar_path: Path,
    modified: bytes,
    out_path: Path,
    compresslevel: int | None,
) -> None:
    with zipfile.ZipFile(jar_path, "r") as zin:
        infos = zin.infolist()
        payloads = [(info, zin.read(info)) for info in infos]

    kwargs = {"compression": zipfile.ZIP_DEFLATED}
    if compresslevel is not None:
        kwargs["compresslevel"] = compresslevel

    with zipfile.ZipFile(out_path, "w", allowZip64=True, **kwargs) as zout:
        for info, payload in payloads:
            zi = copy.copy(info)
            # Preserve the original entry compression method. Python's ZipFile
            # will recompress entry data, matching a common local repack path.
            zi.compress_type = info.compress_type
            if compresslevel is not None and info.compress_type == zipfile.ZIP_DEFLATED:
                zi._compresslevel = compresslevel
            data = modified if info.filename == MIXIN_PATH else payload
            zout.writestr(zi, data)


def raw_deflate(data: bytes, level: int) -> bytes:
    comp = zlib.compressobj(level, zlib.DEFLATED, -15)
    return comp.compress(data) + comp.flush()


def find_eocd(data: bytes) -> int:
    pos = data.rfind(EOCD_SIG, max(0, len(data) - (0xFFFF + 22)))
    if pos < 0:
        raise ValueError("EOCD not found")
    return pos


def parse_central_records(data: bytes) -> tuple[int, int, list[dict]]:
    eocd = find_eocd(data)
    if len(data) < eocd + 22:
        raise ValueError("truncated EOCD")
    disk_no, cd_disk, disk_entries, total_entries, cd_size, cd_offset, comment_len = struct.unpack_from(
        "<HHHHIIH", data, eocd + 4
    )
    if disk_no or cd_disk or disk_entries != total_entries:
        raise ValueError("multi-disk ZIP not supported")
    if cd_offset == 0xFFFFFFFF or cd_size == 0xFFFFFFFF:
        raise ValueError("ZIP64 central directory not supported by this audit")
    if eocd + 22 + comment_len > len(data):
        raise ValueError("truncated EOCD comment")

    records = []
    pos = cd_offset
    for _ in range(total_entries):
        if data[pos : pos + 4] != CENTRAL_SIG:
            raise ValueError(f"central signature missing at {pos}")
        if pos + 46 > len(data):
            raise ValueError("truncated central record")
        (
            _sig,
            made_by,
            need_ver,
            flags,
            method,
            mod_time,
            mod_date,
            crc,
            csize,
            usize,
            fn_len,
            extra_len,
            comment_len_entry,
            disk_start,
            int_attr,
            ext_attr,
            local_offset,
        ) = struct.unpack_from("<IHHHHHHIIIHHHHHII", data, pos)
        end = pos + 46 + fn_len + extra_len + comment_len_entry
        name = data[pos + 46 : pos + 46 + fn_len].decode("utf-8")
        records.append(
            {
                "start": pos,
                "end": end,
                "name": name,
                "flags": flags,
                "method": method,
                "crc": crc,
                "csize": csize,
                "usize": usize,
                "local_offset": local_offset,
            }
        )
        pos = end
    if pos != cd_offset + cd_size:
        raise ValueError(
            f"central directory size mismatch: parsed={pos-cd_offset}, declared={cd_size}"
        )
    return eocd, cd_offset, records


def patch_data_descriptor(old_tail: bytes, crc: int, csize: int, usize: int) -> bytes:
    if old_tail.startswith(DD_SIG):
        if len(old_tail) != 16:
            raise ValueError(f"unexpected signed data descriptor length {len(old_tail)}")
        return DD_SIG + struct.pack("<III", crc, csize, usize)
    if len(old_tail) == 12:
        return struct.pack("<III", crc, csize, usize)
    if old_tail:
        raise ValueError(f"unexpected data descriptor/tail length {len(old_tail)}")
    return b""


def surgical_patch(original: bytes, modified: bytes, level: int) -> bytes:
    eocd, cd_offset, records = parse_central_records(original)
    target_idx = next(i for i, rec in enumerate(records) if rec["name"] == MIXIN_PATH)
    target = records[target_idx]
    if target["method"] != zipfile.ZIP_DEFLATED:
        raise ValueError("mixin JSON is not DEFLATED")

    local_offsets = [rec["local_offset"] for rec in records]
    sorted_by_offset = sorted(enumerate(local_offsets), key=lambda x: x[1])
    ordered_indexes = [idx for idx, _ in sorted_by_offset]
    if ordered_indexes != list(range(len(records))):
        raise ValueError("central/local entry order differs; audit assumes stable order")

    start = target["local_offset"]
    next_start = records[target_idx + 1]["local_offset"] if target_idx + 1 < len(records) else cd_offset

    if original[start : start + 4] != LOCAL_SIG:
        raise ValueError("target local header signature missing")
    (
        _sig,
        need_ver,
        flags,
        method,
        mod_time,
        mod_date,
        local_crc,
        local_csize,
        local_usize,
        fn_len,
        extra_len,
    ) = struct.unpack_from("<IHHHHHIIIHH", original, start)

    header_end = start + 30 + fn_len + extra_len
    name_bytes = original[start + 30 : start + 30 + fn_len]
    if name_bytes.decode("utf-8") != MIXIN_PATH:
        raise ValueError("target local filename mismatch")

    old_csize = target["csize"]
    old_payload_end = header_end + old_csize
    if old_payload_end > next_start:
        raise ValueError("target compressed payload exceeds next record")
    old_tail = original[old_payload_end:next_start]

    compressed = raw_deflate(modified, level)
    crc = binascii.crc32(modified) & 0xFFFFFFFF
    csize = len(compressed)
    usize = len(modified)

    new_local = bytearray(original[start:header_end])
    if flags & 0x0008:
        # Sizes/CRC are carried by the data descriptor. Preserve whatever the
        # local header used (normally zeros).
        descriptor = patch_data_descriptor(old_tail, crc, csize, usize)
    else:
        struct.pack_into("<III", new_local, 14, crc, csize, usize)
        descriptor = old_tail

    target_record = bytes(new_local) + compressed + descriptor
    delta = len(target_record) - (next_start - start)

    new_local_offsets = []
    for rec in records:
        off = rec["local_offset"]
        new_local_offsets.append(off if off <= start else off + delta)

    local_section = bytearray()
    cursor = 0
    for i, rec in enumerate(records):
        rec_start = rec["local_offset"]
        rec_end = records[i + 1]["local_offset"] if i + 1 < len(records) else cd_offset
        if cursor != rec_start:
            # Preserve any prefix/self-extracting bytes if present.
            local_section.extend(original[cursor:rec_start])
        if i == target_idx:
            local_section.extend(target_record)
        else:
            local_section.extend(original[rec_start:rec_end])
        cursor = rec_end

    if cursor != cd_offset:
        local_section.extend(original[cursor:cd_offset])

    new_cd = bytearray()
    for i, rec in enumerate(records):
        raw = bytearray(original[rec["start"]:rec["end"]])
        if i == target_idx:
            struct.pack_into("<III", raw, 16, crc, csize, usize)
        struct.pack_into("<I", raw, 42, new_local_offsets[i])
        new_cd.extend(raw)

    old_cd_size = eocd - cd_offset
    if len(new_cd) != old_cd_size:
        raise ValueError("central directory length unexpectedly changed")

    eocd_bytes = bytearray(original[eocd:])
    struct.pack_into("<I", eocd_bytes, 16, cd_offset + delta)

    result = bytes(local_section) + bytes(new_cd) + bytes(eocd_bytes)

    # Verify structural correctness and target content.
    with tempfile.NamedTemporaryFile(suffix=".jar", delete=False) as tmp:
        tmp.write(result)
        tmp_path = Path(tmp.name)
    try:
        with zipfile.ZipFile(tmp_path, "r") as zf:
            assert zf.testzip() is None
            assert zf.read(MIXIN_PATH) == modified
    finally:
        tmp_path.unlink(missing_ok=True)

    return result


def candidate_row(name: str, strategy: str, level: int | None, data: bytes) -> dict:
    size = len(data)
    sha1 = sha1_bytes(data)
    return {
        "candidate": name,
        "strategy": strategy,
        "compresslevel": level,
        "size": size,
        "size_delta_vs_official": size - OFFICIAL_SIZE,
        "sha1": sha1,
        "sha256": sha256_bytes(data),
        "matches_physical_sha1": sha1 == PHYSICAL_SHA1,
        "matches_first_local_size": size == KNOWN_LOCAL_FIRST_SIZE,
        "matches_v2_local_size": size == KNOWN_LOCAL_V2_SIZE,
    }


def run(out_json: Path, out_md: Path) -> dict:
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        official_path = td_path / "official.jar"
        download_official(official_path)
        official = official_path.read_bytes()
        official_meta = verify_official(official)
        info, mixin_raw, parsed = load_mixin_json(official_path)

        transforms = {
            "remove_player": ("PlayerMixin",),
            "remove_server_player": ("ServerPlayerMixin",),
            "remove_player_and_server_player": ("PlayerMixin", "ServerPlayerMixin"),
        }

        rows = []
        transformed = {}
        for name, remove in transforms.items():
            transformed[name] = transform_json(mixin_raw, remove)

        # Strategy A: common Python zipfile rewrite, using levels 1..9 plus
        # default zlib behavior. The historical artifacts were model-generated,
        # so this is a relevant reproduction family.
        for name, modified in transformed.items():
            for level in [None, *range(1, 10)]:
                out_path = td_path / f"{name}-zipfile-{level}.jar"
                rewrite_zipfile(official_path, modified, out_path, level)
                rows.append(
                    candidate_row(
                        name,
                        "python_zipfile_rewrite",
                        level,
                        out_path.read_bytes(),
                    )
                )

        # Strategy B: surgical single-entry replacement preserving all other
        # archive bytes, central metadata, entry order and timestamps.
        for name, modified in transformed.items():
            for level in range(1, 10):
                data = surgical_patch(official, modified, level)
                rows.append(
                    candidate_row(
                        name,
                        "surgical_single_entry",
                        level,
                        data,
                    )
                )

        rows.sort(
            key=lambda row: (
                not row["matches_physical_sha1"],
                not (row["matches_first_local_size"] or row["matches_v2_local_size"]),
                abs(row["size_delta_vs_official"]),
                row["candidate"],
                row["strategy"],
                -1 if row["compresslevel"] is None else row["compresslevel"],
            )
        )

        report = {
            "scope": "Deeper and Darker 1.4.1 local NeoVitae candidate reproduction",
            "official": official_meta,
            "physical_target_sha1": PHYSICAL_SHA1,
            "known_local_artifact_sizes": {
                "first": KNOWN_LOCAL_FIRST_SIZE,
                "v2": KNOWN_LOCAL_V2_SIZE,
            },
            "official_mixin_entry": {
                "filename": info.filename,
                "uncompressed_size": info.file_size,
                "compressed_size": info.compress_size,
                "crc": f"{info.CRC:08x}",
                "compress_type": info.compress_type,
                "flag_bits": info.flag_bits,
                "mixins": parsed["mixins"],
            },
            "candidates": rows,
            "physical_matches": [r for r in rows if r["matches_physical_sha1"]],
            "size_matches_first": [r for r in rows if r["matches_first_local_size"]],
            "size_matches_v2": [r for r in rows if r["matches_v2_local_size"]],
            "disposition": (
                "EXACT_PHYSICAL_MATCH_FOUND"
                if any(r["matches_physical_sha1"] for r in rows)
                else "NO_EXACT_PHYSICAL_MATCH_IN_BOUNDED_CANDIDATE_FAMILY"
            ),
        }

        out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        lines = [
            "# Deeper and Darker 1.4.1 — NeoVitae candidate reproduction evidence",
            "",
            f"- official size: {official_meta['size']}",
            f"- official SHA-1: \`{official_meta['sha1']}\`",
            f"- physical target SHA-1: \`{PHYSICAL_SHA1}\`",
            f"- retained local first size: {KNOWN_LOCAL_FIRST_SIZE}",
            f"- retained local v2 size: {KNOWN_LOCAL_V2_SIZE}",
            f"- official mixin entry compressed size: {info.compress_size}",
            f"- official mixin entry uncompressed size: {info.file_size}",
            f"- disposition: **{report['disposition']}**",
            "",
            "## Physical SHA-1 matches",
            "",
        ]
        if report["physical_matches"]:
            for row in report["physical_matches"]:
                lines.append(
                    f"- {row['candidate']} / {row['strategy']} / level={row['compresslevel']} "
                    f"/ size={row['size']} / SHA-1=\`{row['sha1']}\`"
                )
        else:
            lines.append("- none in the bounded candidate family")

        lines += ["", "## Candidates matching retained local artifact sizes", ""]
        selected = [
            row for row in rows
            if row["matches_first_local_size"] or row["matches_v2_local_size"]
        ]
        if selected:
            for row in selected:
                labels = []
                if row["matches_first_local_size"]:
                    labels.append("first-size")
                if row["matches_v2_local_size"]:
                    labels.append("v2-size")
                lines.append(
                    f"- {'/'.join(labels)}: {row['candidate']} / {row['strategy']} "
                    f"/ level={row['compresslevel']} / size={row['size']} "
                    f"/ SHA-1=\`{row['sha1']}\`"
                )
        else:
            lines.append("- none")

        lines += [
            "",
            "## Boundary",
            "",
            "A size match is not byte identity. Only an exact SHA-1 match to the physical target "
            "can close deployed-byte identity. A no-match result only rules out the explicitly "
            "generated candidate family; it does not prove what other local transformation produced "
            "the physical JAR.",
            "",
        ]
        out_md.write_text("\n".join(lines), encoding="utf-8")
        return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-json", default="deeper-darker-neovitae-candidate-repro.json")
    parser.add_argument("--out-md", default="deeper-darker-neovitae-candidate-repro.md")
    args = parser.parse_args()

    report = run(Path(args.out_json), Path(args.out_md))
    print(json.dumps({
        "disposition": report["disposition"],
        "physical_matches": report["physical_matches"],
        "size_matches_first": report["size_matches_first"],
        "size_matches_v2": report["size_matches_v2"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
