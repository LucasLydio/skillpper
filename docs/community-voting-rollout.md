# Community Voting Rollout

Use this checklist after the community voting pull request is merged.

## 1. Enable GitHub features

1. Open the repository on GitHub.
2. Go to **Settings -> General -> Features**.
3. Enable **Discussions**.
4. Go to the **Discussions** tab.
5. Create a discussion category named exactly:

```text
Skill Votes
```

6. Go to **Settings -> Pages**.
7. Set **Source** to **Deploy from a branch**.
8. Select the default branch.
9. Select the `/docs` folder.
10. Save.

The dashboard will be available at:

```text
https://OWNER.github.io/REPOSITORY/
```

## 2. Allow the workflow to update files

1. Go to **Settings -> Actions -> General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Save.

The voting workflow needs write access to:

- create missing vote discussions
- update `RANKING.md`
- update `docs/votes.json`
- update `docs/vote-discussions.json`

## 3. Run the first sync

1. Go to **Actions**.
2. Open **Update skill votes**.
3. Click **Run workflow**.
4. Keep `sync_discussions` enabled.
5. Run it on the default branch.

Expected result:

- one `Vote: skill-name` discussion is created for each root-level skill
- `docs/vote-discussions.json` stores the official discussion IDs
- `RANKING.md` is updated
- `docs/votes.json` is updated for the GitHub Pages dashboard

## 4. Smoke test the public flow

1. Open the GitHub Pages dashboard.
2. Confirm all skills are visible.
3. Search for a skill by name.
4. Open a skill's **Vote on GitHub** link.
5. Upvote the discussion.
6. Run **Update skill votes** manually, or wait up to five minutes.
7. Refresh the dashboard.
8. Confirm the vote count changed.

## 5. Announce to the community

Suggested announcement:

```md
We launched Skillpper community voting.

Open the leaderboard, pick the skills you use, and upvote each skill's GitHub Discussion.

Leaderboard: https://OWNER.github.io/REPOSITORY/

Votes help us understand which skills are useful, which ones need improvement, and what the community wants next.
```

## 6. Ongoing maintenance

- New skills are picked up automatically from root-level `*/SKILL.md` files.
- The workflow runs every five minutes, offset from exact five-minute boundaries to reduce GitHub Actions schedule delays.
- Missing official vote discussions are created automatically.
- Copied vote markers in community-created discussions are ignored.
- The trusted discussion mapping is stored in `docs/vote-discussions.json`.

If a skill is renamed, check the next workflow run and confirm the new skill has a vote discussion.

If a discussion is deleted manually, remove the matching entry from `docs/vote-discussions.json` and rerun the workflow with `sync_discussions` enabled.

## 7. Troubleshooting

If the workflow does not run automatically:

- confirm the workflow file is on the default branch
- confirm Actions are enabled
- confirm scheduled workflows are enabled if this is a fork
- wait 10-20 minutes, because scheduled GitHub Actions can be delayed

If the workflow fails to create discussions:

- confirm Discussions are enabled
- confirm the category is named `Skill Votes`
- confirm workflow permissions are **Read and write permissions**

If the dashboard loads but shows old data:

- confirm `docs/votes.json` was updated by the workflow
- confirm GitHub Pages is deploying from `/docs`
- wait for the Pages deployment to finish
