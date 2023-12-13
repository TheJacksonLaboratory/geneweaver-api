# GitHub Actions

The files in this directory are used to configure the Github Actions workflows for
`geneweaver-api`. The workflows are used to automatically build and test the project
when changes are pushed to the repository.

Any file that starts with an underscore (`_`) is a "reusable workflow". These files
are not directly used by GitHub Actions, but are instead referenced by the workflows
files that do not start with an underscore.

There are five reusable workflows:

- Check Coverage (`_check-coverage-action.yml`): This workflow is used to check the code
  coverage of the project.
- Format Lint (`_format-lint-action.yml`): This workflow is used to check the formatting
  and linting of the project.
- Run Tests (`_run-tests-action.yml`): This workflow is used to run the tests for the
  project.
- Skaffold Build (`_skaffold-build-k8s.yml`): This workflow is used to build the
  Docker images for the project.
- Skaffold Deploy (`_skaffold-deploy-action.yml`): This workflow is used to deploy the
  Docker images to kubernetes.

There are two _main_ workflows that are used by GitHub Actions:

- Pull Requests (`pull_requests.yml`): This workflow is used to build and test the
  project when a pull request is opened.
- Release (`release.yml`): This workflow that is run whenever the version number changes
  on the `main` branch.

There are also three quality assurance workflows that are run on any change to the main
branch:

- Coverage (`coverage.yml`): This workflow is used to check the code coverage of the
  project.
- Style (`style.yml`): This workflow is used to check the formatting and linting of the
  project.
- Tests (`tests.yml`): This workflow is used to run the tests for the project.


## Pull Requests

The pull request workflow is run whenever a pull request is opened. This workflow
will:

- Check the formatting and linting of the project.
- Run the tests for the project.
- Check the code coverage of the project.
- Build the Docker images (into the `test` registry) for the project.
- Deploy the Docker images (from the `test` registry) to kubernetes (into the `dev` 
  environment).

## Release

The release workflow is run whenever the version number changes on the `main` branch.
This workflow will:

- Check the formatting and linting of the project.
- Run the tests for the project.
- Check the code coverage of the project.
- Build the Docker images (into the `prod` registry) for the project.
- Deploy the Docker images (from the `prod` registry) to kubernetes (into the `sqa` 
  environment).
  - It will wait for approval from SQA before running this step
- If the version number is not a pre-release version (contains a letter) it will then:
    - Deploy the Docker images (from the `prod` registry) to kubernetes (into the 
      `stage` environment).
      - It will wait for approval from SQA before running this step
    - Deploy the Docker images (from the `prod` registry) to kubernetes (into the `prod` 
      environment).
      - It will wait for approval from SQA before running this step
    - It will then create a draft GitHub release