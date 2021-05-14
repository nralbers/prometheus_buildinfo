# Prometheus BuildInfo
Python library for adding a buildinfo metric to your Prometheus-enabled applications.

## Usage
### Installation

    pip install prometheus-build-info
    
### make-build-info utility

The make-build-info utility can be used during building or packaging to create a prom_build_info.json file that stores the
relevant build information that this library publishes. 

    make-build-info --help
    Usage: make-build-info [OPTIONS] APPNAME BRANCH REVISION VERSION

    Options:
      --help  Show this message and exit.

Alternatively, running the utility when environment variables exist with the same name as the arguments listed above will
have the same effect.

### Manual creation of prom_build_info.json

If this suits your build process better, you can manually create prom_build_info.json during the build. It has the following 
format:

    {
    "appname": "test_app",
    "branch": "master",
    "revision": "abcdef",
    "version": "1.0.1"
    }
    
### Adding the metric to your app

Ensure that prom_build_info.json is in your application working directory. Import ```prometheus_build_info.metrics``` 
into a code file that will be run during or after application initialisation.