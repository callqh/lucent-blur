# Releasing Lucent Blur

## Repository setup

Configure these settings before running the release workflow:

1. Open the repository's **Settings → Actions → General** page.
2. Enable read and write workflow permissions.
3. Allow GitHub Actions to create and approve pull requests.
4. Add a repository secret named `COMMITTER_TOKEN`.

`COMMITTER_TOKEN` is used to push a branch to
[`callqh/extensions`](https://github.com/callqh/extensions) and open the Zed
store update pull request. The referenced action recommends a classic personal
access token with `repo` and `workflow` scopes.

## First store publication

The release workflow can update an extension that already exists in the Zed
store, but it cannot create the initial store entry.

For the first publication, add this repository as a submodule in your
`callqh/extensions` fork and add the matching `extensions.toml` entry:

```toml
[lucent-blur-theme]
submodule = "extensions/lucent-blur-theme"
version = "0.3.0"
```

Then open a pull request from `callqh/extensions` to
[`zed-industries/extensions`](https://github.com/zed-industries/extensions).
Follow Zed's current extension publishing requirements when preparing that PR.

## Creating a release

1. Open **Actions → Release → Run workflow**.
2. Select `patch`, `minor`, or `major`.
3. Run the workflow from `main`.

The workflow updates `extension.toml`, validates the themes, commits the
release, creates a version tag, publishes a GitHub Release, and opens the Zed
store update pull request.

Store publication completes after the Zed maintainers approve and merge that
pull request.
