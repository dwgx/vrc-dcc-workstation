# Avatar perf / VRAM (load on 显存, 下载, Poor/Very Poor, AAO)

Do not Crunch or drop remaining 2K because SDK VRAM “looks too good” after deleting a pack. Rest-OFF meshes **still upload**.

## Two numbers (never mix)

| Number | What it is |
|---|---|
| Editor Profiler texture | Usually **RGBA** in the Editor |
| SDK / world **VRAM** | **Compressed** (BC7/DXT) of textures the bake uses |

RGBA ≈ 2× compressed. Telling the Owner “we saved 300 MB” from the Profiler alone is a lie. Quote the SDK control-panel VRAM (or the number they pasted).

PC rank band (VRAM): Excellent &lt;40 · Good &lt;75 · Medium &lt;110 · **Poor 110–150** · Very Poor ≥150. A 2K body often sits in Poor. Excellent/Good after deleting packs usually means you destroyed the face/clothes. Live numbers: `maps/<avatar>/`.

## What actually drops VRAM (do this)

1. **Delete a pack the Owner named unused** (whole outfit + its 2K set). Rest-OFF meshes **still upload**.
2. **Audio cap 3**, not more AudioSources. Silence a competitor so PCS can play. That is **not** VRAM.
3. **Bits:** do not add synced params. Overflow → `SPS_DickSize` local, never re-drag ABT.
4. Health check after a drop: `missingMat=0`, `Hidden/InternalErrorShader=0`, `crunch=0`, `uncomp=0`, no 4K. Then it is a pack delete, not a strip.

## What looks like “optimization” and is wrong here

| Fake win | Why it is wrong |
|---|---|
| Crunch / drop 2K | Freeze. Face and maid clothes go muddy. Owner 不要降 2K. |
| AAO until Owner yes | Not in project. Wait. |
| Merge 白+黑 maid armatures | Freeze. 41+41 PhysBones are the cost of two whole suits. |
| MeshCutter nipples / VertexFilterByShape | Morph mx &lt; 0.01 hides nothing. Gothic-only poke; pack gone. |
| “null texture slots = missing” | lilToon unused `_2nd`/`_3rd` slots. Thousands of nulls are normal. Count **pink shader** and **missing Material**. |
| Profiler 227 → force 40 | That is the Excellent trap. Stop. |

## When the Owner says 显存好低 / 会不会出事

1. Dump unique tex / 2K / 4K / streaming / crunch / pink / missingMat. Named `vrc_audit` (or emergency paste).
2. Compare to the last vram note, not to a Quest chart.
3. If pink=0 and 2K still on body/face/maid: **reassure, do not downres.**
4. If SDK VRAM &lt;40 on this avatar: hunt missing materials, do not celebrate.

Human SDK Publish. Do not click Build to “refresh VRAM.”
