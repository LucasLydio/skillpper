# Community Voting

Skillpper can use GitHub Discussions as a low-friction voting surface for skills. Community members vote by upvoting one discussion per skill, and a scheduled workflow generates `RANKING.md` plus the GitHub Pages dashboard data.

For the full post-merge setup checklist, see [Community Voting Rollout](community-voting-rollout.md).

## Maintainer setup

1. Enable GitHub Discussions in the repository settings.
2. Create a discussion category named `Skill Votes`.
3. Merge the voting workflow.
4. Run **Actions -> Update skill votes -> Run workflow** with `sync_discussions` enabled.
5. Enable GitHub Pages from the default branch's `/docs` folder.

The first manual run creates one vote discussion for each root-level skill and records its discussion ID in `docs/vote-discussions.json`. Later scheduled runs create any missing vote discussions and update `RANKING.md` and `docs/votes.json` from the current upvote counts every five minutes, offset from exact five-minute boundaries to reduce GitHub Actions schedule delays.

## How voting works

Each generated discussion includes a hidden marker:

```markdown
<!-- skillpper-vote-skill: design-craft -->
```

The ranking script uses that marker only on registered discussions created by the workflow. The trusted skill-to-discussion mapping lives in `docs/vote-discussions.json`, so copied markers in community-created discussions are ignored. It counts only upvotes on the registered discussion itself.

## Permissions

The workflow requests:

- `discussions: write` to create missing vote discussions during sync runs.
- `contents: write` to commit generated `RANKING.md`, `docs/votes.json`, and `docs/vote-discussions.json` updates.

Forked pull requests normally cannot create discussions in the upstream repository. This is expected. The automation starts working after maintainers merge it and run it from the upstream repository.

## Local preview

Without GitHub credentials, this command generates a zero-vote local preview:

```bash
python scripts/update_skill_votes.py
```

Inside GitHub Actions, the same script reads `GH_TOKEN` and `GITHUB_REPOSITORY`, fetches discussion upvotes through GitHub GraphQL, and updates the ranking.
