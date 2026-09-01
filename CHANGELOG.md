# Release notes

<!-- do not remove -->

## 0.2.9

### New Features

- Import APIError from fasttransport ([#19](https://github.com/AnswerDotAI/fastgws/pull/19)), thanks to [@jph00](https://github.com/jph00)


## 0.2.8

### New Features

- Add WorkspaceAddons for Workspace Add-ons deployment and test installation ([#18](https://github.com/AnswerDotAI/fastgws/pull/18)), thanks to [@jph00](https://github.com/jph00)


## 0.2.7

### New Features

- Add resilient Google API clients and Workspace administration ([#17](https://github.com/AnswerDotAI/fastgws/pull/17)), thanks to [@jph00](https://github.com/jph00)
- Drop `batch_get` and the googleapiclient dependency ([#15](https://github.com/AnswerDotAI/fastgws/pull/15)), thanks to [@ncoop57](https://github.com/ncoop57)

### Bugs Squashed

- Apply `@allow` to the OAuth functions at definition ([#14](https://github.com/AnswerDotAI/fastgws/pull/14)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.2.6

### New Features

- Add split OAuth flow (auth_url/finish_auth) for agent-friendly auth ([#13](https://github.com/AnswerDotAI/fastgws/pull/13)), thanks to [@ncoop57](https://github.com/ncoop57)
- Pin version


## 0.2.5

### New Features

- Auto-refresh OAuth tokens non-blockingly during API calls ([#11](https://github.com/AnswerDotAI/fastgws/pull/11)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.2.4

### New Features

- Handle retries


## 0.2.3

### New Features

- Simplify auth


## 0.2.2

### New Features

- Add support for custom redirs and refreshing tokens


## 0.2.1

### New Features

- Add PySkill support for Google Workspace APIs ([#9](https://github.com/AnswerDotAI/fastgws/pull/9)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.2.0

### New Features

- Redesign fastgws to rely on fastspec for creating async Python clients to Google Workspace and APIs
