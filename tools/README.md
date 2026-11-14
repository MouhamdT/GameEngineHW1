# Unreal MCP client

`unreal_mcp.py` calls Epic's bundled local MCP server over HTTP. It uses only the Python standard library and never sends OS keyboard/mouse input. Tools execute in the live editor; run calls sequentially.

The project enables the MCP, Blueprint and UMG toolsets for Editor targets. The current editor was started with `-ModelContextProtocolStartServer` and is already connected on `http://127.0.0.1:8000/mcp`.

For a later editor session, start the MCP server from the Unreal console with `ModelContextProtocol.StartServer`, or launch the project with the `-ModelContextProtocolStartServer` flag. Do not launch a duplicate editor for the same project.

From the project folder:

```powershell
python tools\unreal_mcp.py initialize
python tools\unreal_mcp.py list_toolsets
python tools\unreal_mcp.py call_tool @Saved/Automation/request.json
```

Discover schemas before making changes. A call request contains `toolset_name`, `tool_name` and `arguments`. Pass Unreal object references as `{ "refPath": "/Game/..." }` where the schema requires them.

Important observations from this engine version:

- Save newly created assets before discovering their cast/input-event nodes in another Blueprint. The node-type cache refreshes when graph/variable structure changes.
- Inspect actual pin IDs for Enhanced Input events and explicitly wire Started. The text graph decompiler omits some multi-exec event connections, so do not round-trip an entire existing input graph indiscriminately.
- Pure-node bindings are references to outputs, not cached values. Store a local variable before moving a component when subsequent calculations need its original position.
- Compile affected child Blueprints and verify inherited defaults after adding parent variables/components.
- `AssetTools.save_assets` with an empty `asset_paths` list saves all dirty packages, including World Partition external actor packages. Saving the map asset alone does not guarantee new actors are persisted.
- `CaptureViewport` captures the Edit viewport. Use `CaptureEditorImage` during Play to inspect the actual HUD/game result, and parse its returned image payload without dumping base64 to the chat.

Gameplay lives in the saved Blueprint assets. Scratch tests under `Saved/Automation` are ignored by Git. Temporary test actors and Blueprints were removed after verification.
