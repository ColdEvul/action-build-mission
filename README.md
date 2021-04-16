# action-build-mission

Binarize mission SQM, and pack as pbo using armake2


## Inputs

### `missions-dir`

**Required**

Path to directory containing subsequent directories that have a mission.sqm

### `version-tag`

**Required**

Version to tag missions with

### `release-dir`

_Optional_

Path to directory that compiled missions will be stored in

Will default to $GITHUB_WORKSPACE/release

## Outputs

*There is no output*

## Usage

```yml
uses: 7cav/action-build-mission
with:
  missions-dir: path/to/maps/dir
  version-tag: 0.0.1
  release-dir: path/to/release/dir
```