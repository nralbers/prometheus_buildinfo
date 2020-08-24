import click
import json

@click.command()
@click.argument('appname')
@click.argument('branch')
@click.argument('revision')
@click.argument('version')
def make_build_info(appname, branch, revision, version):
    buildinfo= {
        "appname": appname,
        "branch": branch,
        "revision": revision,
        "version": version
    }
    with open('build_info.json', 'w') as buildinfo_file:
        buildinfo_file.write(json.dumps(buildinfo, indent=4, sort_keys=True))
    click.echo("BuildInfo updated")