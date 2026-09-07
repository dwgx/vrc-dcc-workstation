# ワークフロー（Blender → Unity → 人が Publish）

<!-- I18N:START -->
[English](../../WORKFLOW.md) · [简体中文](../zh-CN/WORKFLOW.md) · **日本語** · [한국어](../ko/WORKFLOW.md)
<!-- I18N:END -->

ピン：`manifests/tools.json`（`scripts/refresh-pins.ps1` で再確認。GitHub **releases** が第三者 VPM カタログより優先）。本ページは 2026-09 公開パイプラインです。

```
Blender 5.2 LTS  --blender-mcp-->  FBX / VRM
Unity 2022.3 LTS --CoplayDev HTTP + named vrc_*-->  MA / NDMF / menus
Human: VRChat SDK Build & Publish
```

## 0. ヒアリング

1. [AGENTS.ja.md](../../../AGENTS.ja.md) を読む。導入アンケートのあと `scripts/bootstrap.ps1 -Apply` で `local.json.example` から `local.json` を埋める。[DROP_ON_AGENT.md](../../DROP_ON_AGENT.md)。
2. Blender / Unity MCP を Claude / Codex / Cursor / Grok の**ユーザーグローバル**設定に**付けない**。`skills/` をユーザーグローバルにコピーしない。
3. パッケージ追加や Editor 操作は、**アバター Unity プロジェクト専用のウィンドウ**で行う。

指名 `vrc_*` には記入済みの `POLICY.json`（`unity_root_name`）が必要。シーンの最初のアバターは取らない。工位 HTTP は `vrc_*` のみ。`gate.py begin` が JOB lease を書く（`VRC_DCC_JOB_HOLDER`）。反復：[ITERATION.md](../../ITERATION.md)。

## 1. Blender（メッシュ / ウェイト / ヴィセム）

目標エディタ：**Blender 5.2 LTS**。`manifests/tools.json` のピンの PyPI `blender-mcp` で接続（既定 Python が 3.14+ なら `uvx` 下の CPython **3.11**）。

1. 人：**Interface: Blender MCP** を有効化し、N パネルで **Start MCP Server**（ポート 9876）。
2. クライアント：`uvx --python 3.11 blender-mcp==<pin>`。必要なら `UV_PYTHON_PREFERENCE=only-managed`。
3. blender-mcp の**クライアントは同時に 1 つ**（Cursor **または** Claude Desktop。両方は不可）。
4. ウェイト、ヴィセム、アーマチュア名、CATS（任意 vendor `Alrauna/Cats-Blender-Plugin`）は Blender 側。
5. Unity 向け FBX を書き出す。Humanoid ボーン名は Modular Avatar マージ前に**対象**アーマチュアと一致させる。
6. 衣装がこの体に**未適応**なら**止める**。Unity の MA はウェイトを直せない。

5.2 が ahujasid を拒む場合：マニフェストの `dcc-mcp-blender` ピン。

詳細：`skills/vrc-dcc/blender.md`（スキル本文は英語）。

## 2. Unity 2022.3（MA / NDMF / メニュー）

目標エディタ：**Unity 2022.3 LTS**（このアバター管線では Unity 6 ではない）。

**開いているアバタープロジェクト**で（home / 制御プレーンの窓ではない）：

1. `manifests/tools.json` の `upm` から CoplayDev MCP for Unity を入れる。
2. Window → **MCP for Unity** → Start（HTTP `http://localhost:8080/mcp`）。
3. lighfu UnityAgent / EditorEye / 第二の Unity MCP は入れない。
4. **MA Merge Armature** / Menu Installer / Parameters で服を合せる。頼まれない限り NDMF を bake しない。衣装メニュー：[CLOTHING_MENU.md](../zh-CN/CLOTHING_MENU.md)（日本語ページが無ければ中/英）。
5. `.prefab` YAML を手で直すより、指名 `vrc_*` を使う。`execute_code` / `execute_csharp` を発明しない。
6. MCP から `EditorUtility.DisplayDialog` を呼ばない（Editor が固まる）。

公式 Unity 6 MCP / `com.unity.ai.assistant` はこの 2022.3 プロジェクトでは**オフ**。TunaSync UnityMCP-VCC や swax/UnityMCP-VRC を既定ブリッジにしない。

パッケージ URL：[UNITY.md](UNITY.md)。PhysBone：`skills/vrc-dcc/references/physbones.md`。

## 3. 人が Publish + ワールドで確認

人が VRChat SDK の **Build & Publish** を押す。エージェントは押さない、`upload_vrchat_avatar` を呼ばない、SDK cookie を残さない。

Editor Play が VRCFury の haptic bake で止まるのは服の失敗ではない。Build のあと VRChat で見る：[upload-test.md](../../../skills/vrc-dcc/references/upload-test.md)。店の歩行 vs GoGo：[gogoloco.md](../../../skills/vrc-dcc/references/gogoloco.md)（既定の歩きは MAP/OWNER。キャラ固定ではない）。

## 4. 仕事のあと

`skills/vrc-review` → `notes/`（`templates/AFTER_ACTION.md`）。チャットは記憶ではない。
