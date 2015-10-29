 [![NPM version](http://img.shields.io/npm/v/travis-weigh-in.svg)](https://www.npmjs.org/package/travis-weigh-in)
 
# travis-weigh-in
Track how each commit/pull request affects the size of a file in your repo.

You are what you measure! This script lets you track the size of a generated file (e.g. your minified JavaScript bundle) as it's changed by each Pull Request and commit in your GitHub repo. Here's what the Pull Request Statuses section looks like after you've set it up:

![status with weigh-in](https://cloud.githubusercontent.com/assets/98301/10703019/161a9d40-799b-11e5-9798-8ebbab465d02.png)

The last line shows the current size of your file and how it's changed from the base of your PR (typically the `master` branch). With this Travis script, you'll catch code bloat regressions as they happen.

# Setup

I'll assume you have a GitHub repo with [Travis-CI][] enabled.

## Generate a GitHub OAuth token

First you'll need to create a GitHub OAuth token for the weigh-in script to post status messages on your behalf. To do this, go to GitHub settings → "Personal Access Tokens" → "Generate a Token":

![generate new token](https://cloud.githubusercontent.com/assets/98301/10703144/173d430c-799c-11e5-8ac2-915482cacd17.png)

Be sure to check the `repo:status` scope and give your token some descriptive name:

![granting repo status on github](https://cloud.githubusercontent.com/assets/98301/10703161/369dfa2a-799c-11e5-9d94-6451fb8097ef.png)

Once your token is generated, copy it (you'll never be able to see it again!).

Now go to Travis-CI and open up the Settings page for your repo. Add the token as an environment variable named `GITHUB_TOKEN`:

![github_token set](https://cloud.githubusercontent.com/assets/98301/10703222/822cbe86-799c-11e5-8419-794a68339543.png)

Don't forget to click the "Add" button!

## Run the weigh-in script

With the token in place, you need to run the script from your `.travis.yml` file. You can either `npm install travis-weigh-in`, save a copy of the `weigh_in.py` script into your repo, add it as a git submodule, or just `curl` it into place. The script is intentionally written to have zero dependencies so, however you pull it in, it should Just Work.

For example, for a JavaScript project, your `.travis.yml` file might look like this:

```
language: node_js
node_js:
  - "0.12"
script: >
    npm run build &&
    npm run test &&
    curl -O https://raw.githubusercontent.com/danvk/travis-weigh-in/master/weigh_in.py &&
    python weigh_in.py dist/script-to-track.min.js
```

Either push this commit to your repo or send it out as a pull request. The first run will only show an absolute size (i.e. no changes), but subsequent runs should show how the commit/PR changes the size of the file.

If you don't see code sizes posted, check out the logs of your Travis-CI builds for details on what went wrong.

## Setup with NPM

This script is most useful for JavaScript projects, which often use NPM to pull in dependencies. If this is convenient for you, you can set up travis-weigh-in by running:

    npm install --save-dev travis-weigh-in
    
Then your `.travis.yml` file might look like:

```
language: node_js
node_js:
  - "0.12"
script: >
    npm run build &&
    npm run test &&
    python node_modules/travis-weigh-in/weigh_in.py dist/script-to-track.min.js
```

Note that you still have to go through the process of setting `GITHUB_TOKEN` with this approach.

# Notes

If you rename the file, the weigh-in script won't be able to track size changes through the rename. You'll get size change information for subsequent commits after the rename is merged onto `master`, though.

In a pull request, the "push" build pushes an absolute code size, while the "pr" build pushes a size with changes (e.g. "+10 bytes"). If the "push" build finishes first, you'll see the absolute size before you see the delta.

The code in the `master` branch can and will change. If you'd prefer not to trust me, you should either include a copy of the script directly in your own repo, use a submodule checked out at a specific commit or download a copy with a recent git SHA, e.g.

```
curl -O https://raw.githubusercontent.com/danvk/travis-weigh-in/08700622d972fed7adeda13a49988e26a3e98387/weigh_in.py
```

git SHAs are cryptographically secure, so you can be confident that the script won't break underneath you.

[Travis-CI]: https://travis-ci.org/
