# Branching Strategies

In order to maintain a clear and collaborative process while developing, it is essential for the team to adhere to a common strategy for source code version control management. We will be using `git` and GitHub for all projects within the SS Utopia project. As such, the following document is a guide for checking code into repositories, checking code out of repositories, and merging new code into existing code.

## Initial Code Checkout
All code can be retrieved directly from the appropriate GitHub repository via the command line with the following command:
```sh
git clone https://github.com/jms-smoothstack-utopia/<PROJECT-NAME>.git
```

This will clone the repository to the local file system and allow development to be controlled with the version control system. Additionally, it will add the repository as the origin of the project, allowing the developer to push new changes to the repository.

## Primary Branches
Every repository will have two branches that are considered "primary." These are
1. `main`
2. `dev`

An additional `staging` branch will be introduced following the full project 1.0 release but is not currently present.

### `main` Branch
The `main` branch is for currently released, or live, code. This means the code is either compiled to binary and deployed to an artifact repository (rare), applications built and deployed inside a Docker container, or frontend applications built and deployed to Amazon S3.

In general, code should never be pushed directly to the `main` branch. Instead, all code should be merged into this branch via a pull request from the `dev` branch through GitHub and approved by at least 2 members of the team. Ideally, this approval will be through GitHub directly; however, while prototyping a proof of concept, it may be necessary to provide this approval through Slack communication or meetings via Zoom or Google Meets.

Once version 1.0 is released for any individual repository, additional changes to the `main` branch will require approval documented through GitHub.

### `dev` Branch
The `dev` branch is for ongoing development and considered a potentially unstable version of the source code. Code on this branch is considered to still be a "work in progress" but should also be the source for which additional feature branches stem from.

Like the `main` branch, code should not be pushed directly to the `dev` branch. Instead, all code merged into this branch should come from a "feature" branch with new code. For minor tasks, chores, etc., these pull requests may be immediately merged in when the risk is known to be low for breaking changes. However, for very large pull requests that encompass significant features, a code review should first be performed with the author of the feature branch and one additional member of the team. This may be through GitHub conversations, through Slack, or meetings via Zoom or Google Meets. Verbal approval for merges into the `dev` branch are acceptable prior any 1.0 release of a repository.

### `staging` Branch
The `staging` branch is for code to be tested with a full replica of the existing architecture. This branch will perform integration testing, stress testing, user acceptance testing, and other tests as deemed necessary throughout the lifecycle of the project.

Currently, this branch is not included but will be implemented following the full project 1.0 release.

Code should _never_ be pushed directly to this branch (even for HOTFIX modifications). It is considered a sandbox that can be used to explore potential issues with the entire application deployed. All architecture should be full destroyed and rebuilt upon any changes to this branch. All code to be merged into this branch will come from a pull request from the `dev` branch.

This branch will act as an intermediary between the `dev` and `main` branch upon implementation.

### Feature Branches
All feature branches should originate from the most up-to-date version of the `dev` branch. Each branch should be named with the Jira project key abbreviation, the Jira ticket number, and a brief title indicative of the feature. For example, the following branch name is for Jira ticket `SSUTO-32` (viewing booking details):

```
SSUTO-32-ViewBookingDetails
```

The last portion of the branch name, the description, is up to the individual developer. Ideally, these descriptions should be succinct and not go beyond 2 or 3 words but this is not a hard limit.

To initiate a new feature branch off the `dev` branch, the following command can be used to pull and integrate the most recent code from the repository (origin) `dev` branch into the local workspace `dev` branch, checkout this version of code locally, and begin development in a new feature branch from this code:

```sh
git checkout dev
git pull
git checkout -b SSUTO-32-ViewBookingDetails
```

## Pull Requests
All Pull Requests should be initiated through the GitHub web interface. The title of the Pull Request should be the name of the branch (as discussed above). Additionally, a brief message should be included about the incoming changes. This includes, but is not limited to, new feature implementations and how they work, discussions about bug fixes, and/or a brief discussion regarding file changes.

![Example Pull Request](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/pull-request.png)

Continuous Integration testing via Jenkins will be implemented to provide feedback to the viability of the request. The results of the testing can be seen with the most recent commit hash. A green check-mark ![green check-mark](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/green-check.png) indicates all tests passed, whereas a red 'X' ![red X](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/red-x.png) indicates test failures.

Additionally, within the request, an indication is given that "all checks pass" and there are no merge conflicts. When this is seen, the request is ready for review prior to merging.

![Ready to Merge](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/pull-request2.png)

## Code Reviews
### Via Slack
For minor changes, code reviews may take place over a quick conversation in Slack.

Maxwell initiates a PR:
![Maxwell initiates a PR](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/code-review-slack1.png)

Stephen reviews and merges it:
![Stephen reviews and merges it](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/code-review-slack2.png)

### Via GitHub Conversations
Larger changes can be accomplished via GitHub conversations, over meetings in Zoom or Google Meets, or a combination of both.

The following is an example of this. Jordan initiates a Pull Request for a new feature addition to the User Portal. Stephen reviews it and comments directly on it via GitHub. Following this, the entire team discusses the changes and potential fixes over Google Meets. Jordan implements the changes. Another conversation takes place over Google Meets to validate the changes meet the standard for the team. Stephen approves the changes and merges them into the `dev` branch.
![Code review 1](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/example-code-review1.png)
![Code review 2](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/example-code-review2.png)
![Code review 3](https://utopia-documentation-media.s3.amazonaws.com/branching-strategies/example-code-review3.png)

For the full conversation, go to [https://github.com/jms-smoothstack-utopia/UtopiaUserPortal/pull/10](https://github.com/jms-smoothstack-utopia/UtopiaUserPortal/pull/10).