# Release acceptance worksheets

Practical review prompts for app teams handing over software. Start with the system's promised behavior, record the conditions, then keep the observed evidence beside the decision.

Prepared by **Omnistu** with AI assistance. These are proposed review methods, not reports of customer projects, independent audits or device tests. This repository contains documentation only, not the source code of an Omnistu product.

## Choose a worksheet

| Review | Use it when | Evidence to keep |
| --- | --- | --- |
| [App handoff](#app-handoff) | A developer or AI-assisted build is being handed over | Fresh-clone run, deployment notes, access owner and restore result |
| [Android edge-to-edge](#android-edge-to-edge) | Target-SDK changes may put content behind system bars | Build/OS/navigation-mode matrix and full-screen captures |
| [CSV import acceptance](#csv-import-acceptance) | A bulk import can reject rows or be retried | Explicit atomic/partial contract, planned records and rejects |
| [Restore rehearsal](restore-rehearsal-evidence.md) | A backup exists but recovery evidence is missing | Isolation checks, observed behavior, decision limits and cleanup |

## App handoff

A folder of source files is not a complete handoff. Use this review sequence:

1. **Ownership:** record who controls the repository, hosting, domains and third-party accounts. Do not paste passwords or secrets into this repository.
2. **Fresh setup:** have a different maintainer follow the written setup steps from a fresh clone. Record the runtime and dependency versions actually used.
3. **Small change:** make a harmless change in the agreed non-production environment, run the tests and demonstrate its deployment path.
4. **Data recovery:** identify the backup, restore procedure and recovery evidence. A backup file existing is not proof of a successful restore.
5. **Known gaps:** keep unfinished work, operational limits and support responsibilities explicit before sign-off.

Background: [Omnistu's codebase handoff checklist](https://omnistu.com/blog/codebase-handoff-checklist/).

For the data recovery step, use the [restore rehearsal evidence record](restore-rehearsal-evidence.md). It separates backup metadata from observed application behavior and keeps isolation, untested checks and cleanup explicit. It is a proposed worksheet, not a claim that any production system has been restored.

## Android edge-to-edge

Android's current guidance states that edge-to-edge is automatically enabled for apps targeting SDK 35 or later on Android 15 devices or later. This worksheet is a starting point for a release ticket, not an Android certification checklist.

Record **build, target SDK, OS, device/emulator, navigation mode, theme, orientation and screen** before judging a screenshot.

- **Top controls:** title, back control and first action remain readable and reachable near the status bar.
- **Bottom action:** the main action and bottom navigation can be used. A background behind a system bar is not by itself a defect.
- **Long content:** the last list item can be seen and acted on, rather than remaining hidden under the navigation area.
- **Navigation modes:** repeat relevant checks with gesture and 3-button navigation where supported; do not assume identical transparency or scrim defaults.
- **Theme/orientation:** repeat supported light/dark themes and orientations, recording overlap and icon contrast separately.
- **Return path:** leave the screen and return normally to check that inset handling remains correct after navigation.

Copy this evidence row into your own release record:

```text
Build | Target SDK | OS | Device | Navigation mode | Theme | Orientation
Screen | Steps | Expected | Actual | Pass / Fail / Not run
Screenshot | Owner | Fix reference | Retest result
```

This does not establish accessibility conformance or cover every keyboard, cutout, dialog or window configuration. Add cases the actual product needs. No device tests are claimed here.

Reading:
- [Omnistu's explanation of Android edge-to-edge enforcement](https://omnistu.com/blog/android-15-edge-to-edge-enforcement/)
- [Android Developers: display content edge-to-edge](https://developer.android.com/develop/ui/views/layout/edge-to-edge)
- [Android Developers: Android 15 behavior changes](https://developer.android.com/about/versions/15/behavior-changes-15)

Android sources checked 20 November 2026. Re-check the owning documentation when the OS or target SDK changes.

## CSV import acceptance

Before a bulk import goes near real data, decide:

- Does one invalid row reject the entire file, or can valid rows proceed?
- Are existing identifiers rejected, updated or treated as an already-completed retry?
- Does an invalid first occurrence reserve an identifier within the file?
- How are quoted commas, multiline fields, missing fields and non-finite prices handled?
- What exactly is returned to support staff when some rows fail?

Keep validation/planning tests separate from database transaction and concurrency tests. A preflight plan cannot prevent another request inserting the same identifier before commit.

An existing [eight-row Python planning example](https://gist.github.com/imAYUSH621/76cec2e8e0a1f39c330e88845c7d686e) shows atomic/partial/replay outputs using synthetic data and no database. It is not a strict CSV validator, production importer or transaction test. This repository does not copy or relicense that code.

## Use the evidence, not the label

Mark cases **pass**, **fail** or **not run**. Record unsupported configurations rather than marking them passed. Replace the suggested checks with your product's actual contract and have the responsible maintainer review the result.

These materials do not promise search ranking, indexing, traffic or citations. Public visibility is not proof of reuse permission: no additional license has been selected for this repository.
