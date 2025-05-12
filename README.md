# confluence deploy

## confluence release

Script to trigger GitHub actions to create a release for all modules

```bash
python3 create_release.py -t <token> -b main -v 1.0.0
```

- -t: GitHub token
- -b: Branch to deploy
- -v: Version to create release for

## confluence AWS deployment

Script to tigger GitHub actions to deploy all modules

```bash
python3 deploy_all_modules.py -t <token> -b main -n OPS -v 1.0.0 -a
```

- -t: GitHub token
- -b: Branch to deploy
- -n: Venue to deploy to (e.g., DEV1, DEV2, OPS)
- -v: Version to tag deployment
- -a: Deploy toplevel confluence-terraform
