import click
import json

PROM_BUILD_FILE= "prom_build_info.json"

@click.command()
@click.argument('appname', envvar='APPNAME')
@click.argument('branch', envvar='BRANCH')
@click.argument('revision', envvar='REVISION')
@click.argument('version', envvar='VERSION')
def make_build_info(appname, branch, revision, version):
    buildinfo= {
        "appname": appname,
        "branch": branch,
        "revision": revision,
        "version": version
    }
    with open(PROM_BUILD_FILE, 'w') as buildinfo_file:
        buildinfo_file.write(json.dumps(buildinfo, indent=4, sort_keys=True))
    click.echo("BuildInfo updated")