# Community Voting

Skillpper can use GitHub Discussions as a low-friction voting surface for skills. Community members vote by reacting with `:+1:` to one discussion per skill, and a scheduled workflow generates `RANKING.md`.

## Maintainer setup

1. Enable GitHub Discussions in the repository settings.
2. Create a discussion category named `Skill Votes`.
3. Merge the voting workflow.
4. Run **Actions -> Update skill votes -> Run workflow** with `sync_discussions` enabled.

The first manual run creates one vote discussion for each root-level skill. Later scheduled runs create any missing vote discussions and update `RANKING.md` from the current reaction counts every five minutes.

## How voting works

Each generated discussion includes a hidden marker:

```markdown
<!-- skillpper-vote-skill: design-craft -->
```

The ranking script uses that marker to connect a GitHub Discussion to a skill folder. It counts only `:+1:` reactions on the discussion itself.

## Permissions

The workflow requests:

- `discussions: write` to create missing vote discussions during sync runs.
- `contents: write` to commit generated `RANKING.md` updates.

Forked pull requests normally cannot create discussions in the upstream repository. This is expected. The automation starts working after maintainers merge it and run it from the upstream repository.

## Local preview

Without GitHub credentials, this command generates a zero-vote local preview:

```bash
python scripts/update_skill_votes.py
```

Inside GitHub Actions, the same script reads `GH_TOKEN` and `GITHUB_REPOSITORY`, fetches discussion reactions through GitHub GraphQL, and updates the ranking.
