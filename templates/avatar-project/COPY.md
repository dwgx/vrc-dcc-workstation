# Copy into an avatar Unity project (optional)

You do not need this to start an avatar job if Cursor already loads `vrc-dcc` and `session-probe` prints `kind: dcc`.

Copy these files only on a machine **without** the station skill, or if you want a pointer inside the Unity folder itself. Do it from an avatar Cursor window (not home). Home cwd must not write the avatar Unity project.

```
copy  templates\avatar-project\AGENTS.md
  →   <unity-project>\AGENTS.md

copy  templates\avatar-project\.cursor\rules\vrc-dcc-job.mdc
  →   <unity-project>\.cursor\rules\vrc-dcc-job.mdc
```

Do not copy the station `.cursor/rules/vrc-dcc-workstation.mdc` (that one is install/bootstrap).
