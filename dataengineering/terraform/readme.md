# Overview - Sample Terraform Project Set Up

The default branch is `dev`, and any changes should be PR:ed against `dev`.
A pull request is configured to 'terraform plan' the changes and return the
results as a comment to the PR. Changes are applied upon merging the PR to
`dev`.

To propagate a new configuration from `dev` to `stage`, or from `stage` to
`prod`, create a pull request from `dev` to `stage` which will run a terraform
plan to highlight the changes to be applied in the `stage` environment, and
upon merging the PR to `stage`. GitHub should be configured to enforce code
(and change) review from a team member when performing these changes.

# CI/CD configuration

This repository is configured with three protected branches, `dev`, `stage`
and `prod`. Each branch corresponds to the gcp project in that environment.
GitHub actions are configured to terraform plan changes in a pull request
towards the protected branch, and upon merge the changes should be applied to
the environment with `terraform apply`.

Terraform itself in this repository is controlled with a terraform variable -
accessible using `TF_VAR_gcp_environment` which should be one of `dev`, `stage`
or `prod`. Manually running terraform (outside of CI/github actions) needs to
follow the pattern:
```bash
TF_VAR_gcp_environment=dev terraform plan
```
This variable directs terraform to the correct environment, and should not have
a default - causing the command to fail unless it is explicitly set.

These assumptions might change.

# Local Testing

```
gcloud auth application-default login
```

You should so something similar to below:

```
https://accounts.google.com/o/oauth2/auth?client_id=<long_url>
Enter verification code: <some_code>
```

# Initialise Terraform
The following command will run a version of `terraform init` and give the user ability to choose the relevant environment:

```
TF_VAR_gcp_environment=dev terraform init -backend-config "prefix=terraform/${TF_VAR_gcp_environment}/state" -backend-config "bucket=<my-project>-cicd"
```
# Format and Validate

Run the following to format and validate the terraform config scripts:

```
$ terraform fmt
$ terraform validate
```
# Apply

Running the apply command will attempt to build resources on the cloud:

```
$ terraform apply
```
You will need to choose the env:

```
var.gcp_environment
  The Google Cloud Platform environment - dev, stage or prod

  Enter a value: dev
```

and you should see some messages similar to:

```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # module.ingkametrics.google_bigquery_dataset.public_views will be created
  ....
```
