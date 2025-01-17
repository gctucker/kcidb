"""I/O schema"""

import jsonschema

# JSON schema for a named remote resource
JSON_RESOURCE = {
    "title": "resource",
    "description": "A named remote resource",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Resource name",
        },
        "url": {
            "type": "string",
            "format": "uri",
            "description": "Resource URL",
        },
    },
    "additionalProperties": False,
    "required": [
        "name",
        "url",
    ],
}

# JSON schema for a code revision
JSON_REVISION = {
    "title": "revision",
    "description": "A revision of the tested code",
    "type": "object",
    "properties": {
        "origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the revision",
            "pattern": "^[a-z0-9_]*$"
        },
        "origin_id": {
            "type": "string",
            "description": "Origin-unique revision ID",
        },
        "git_repository_url": {
            "type": "string",
            "format": "uri",
            "description":
                "The URL of the Git repository which contains the base code "
                "of the revision. The shortest possible HTTPS URL.",
        },
        "git_repository_commit_hash": {
            "type": "string",
            "description":
                "The full commit hash of the revision's base code "
                "in the Git repository",
        },
        "patch_mboxes": {
            "type": "array",
            "description":
                "List of mboxes containing patches applied "
                "to the base code of the revision, in order of application",
            "items": JSON_RESOURCE,
        },
        "message_id": {
            "type": "string",
            "format": "email",
            "description":
                "The value of the Message-ID header of the e-mail message "
                "introducing this code revision, if any. E.g. a message with "
                "the revision's patchset, or a release announcement sent to "
                "a maillist.",
        },
        "description": {
            "type": "string",
            "description":
                "Human-readable description of the revision. "
                "E.g. a release version, or the subject of a patchset message."
        },
        "publishing_time": {
            "type": "string",
            "format": "date-time",
            "description":
                "The time the revision was made public",
        },
        "discovery_time": {
            "type": "string",
            "format": "date-time",
            "description":
                "The time the revision was discovered by the CI system",
        },
        "contacts": {
            "type": "array",
            "description":
                "List of e-mail addresses of contacts concerned with "
                "this revision, such as authors, reviewers, and mail lists",
            "items": {
                "type": "string",
                "description":
                    "An e-mail address of a contact concerned with this "
                    "revision, e.g. an author, a reviewer, or a mail list, "
                    "as in https://tools.ietf.org/html/rfc5322#section-3.4"
            },
        },
        "log_url": {
            "type": "string",
            "format": "uri",
            "description":
                "The URL of the log file of the attempt to construct this "
                "revision from its parts. E.g. 'git am' output.",
        },
        "valid": {
            "type": "boolean",
            "description":
                "True if the revision is valid, i.e. if its parts could be "
                "combined. False if not, e.g. if its patches failed to apply."
        },
        "misc": {
            "type": "object",
            "description":
                "Miscellaneous extra data about the revision",
        },
    },
    "additionalProperties": False,
    "required": [
        "origin",
        "origin_id",
    ],
}

# JSON schema for a build of a revision
JSON_BUILD = {
    "title": "build",
    "description": "A build of a revision",
    "type": "object",
    "properties": {
        "revision_origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the built revision",
            "pattern": "^[a-z0-9_]*$"
        },
        "revision_origin_id": {
            "type": "string",
            "description":
                "Origin-unique ID of the built revision. The revision must "
                "be valid for the build to be considered valid.",
        },
        "origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the build",
            "pattern": "^[a-z0-9_]*$"
        },
        "origin_id": {
            "type": "string",
            "description": "Origin-unique build ID",
        },
        "description": {
            "type": "string",
            "description":
                "Human-readable description of the build"
        },
        "start_time": {
            "type": "string",
            "format": "date-time",
            "description":
                "The time the build was started",
        },
        "duration": {
            "type": "number",
            "description":
                "The number of seconds it took to complete the build",
        },
        "architecture": {
            "type": "string",
            "description":
                "Target architecture of the build",
            "pattern": "^[a-z0-9_]*$"
        },
        "command": {
            "type": "string",
            "description":
                "Full shell command line used to make the build, "
                "including environment variables",
        },
        "input_files": {
            "type": "array",
            "description":
                "A list of build input files. E.g. configuration.",
            "items": JSON_RESOURCE,
        },
        "output_files": {
            "type": "array",
            "description":
                "A list of build output files: images, packages, etc.",
            "items": JSON_RESOURCE,
        },
        "log_url": {
            "type": "string",
            "format": "uri",
            "description":
                "The URL of the build log file.",
        },
        "valid": {
            "type": "boolean",
            "description":
                "True if the build is valid, i.e. if it could be completed. "
                "False if not.",
        },
        "misc": {
            "type": "object",
            "description":
                "Miscellaneous extra data about the build",
        },
    },
    "additionalProperties": False,
    "required": [
        "revision_origin",
        "revision_origin_id",
        "origin",
        "origin_id",
    ],
}

# JSON schema for a test environment
JSON_ENVIRONMENT = {
    "title": "test",
    "description": "An environment a test ran in",
    "type": "object",
    "properties": {
        "origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the environment",
            "pattern": "^[a-z0-9_]*$"
        },
        "origin_id": {
            "type": "string",
            "description": "Origin-unique ID of the environment",
        },
        "description": {
            "type": "string",
            "description":
                "Human-readable description of the environment"
        },
        "misc": {
            "type": "object",
            "description":
                "Miscellaneous extra data about the environment",
        },
    },
    "additionalProperties": False,
    "required": [
        "origin",
        "origin_id",
    ],
}

# JSON schema for a test run on a build
JSON_TEST = {
    "title": "test",
    "description": "A test run against a build",
    "type": "object",
    "properties": {
        "build_origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the tested build",
            "pattern": "^[a-z0-9_]*$"
        },
        "build_origin_id": {
            "type": "string",
            "description":
                "Origin-unique ID of the tested build. The build must be "
                "valid for the test run to be considered valid.",
        },
        "environment_origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the environment "
                "the test ran in",
            "pattern": "^[a-z0-9_]*$"
        },
        "environment_origin_id": {
            "type": "string",
            "description":
                "Origin-unique ID of the environment the test ran in",
        },
        "origin": {
            "type": "string",
            "description":
                "The name of the CI system which submitted the test run",
            "pattern": "^[a-z0-9_]*$"
        },
        "origin_id": {
            "type": "string",
            "description": "Origin-unique ID of the tested build",
        },
        "path": {
            "type": "string",
            "description":
                "Dot-separated path to the node in the test classification "
                "tree the executed test belongs to. E.g. \"LTPlite.sem01\". "
                "The empty string, or the absence of the property signify "
                "the root of the tree, i.e. an abstract test.",
            "pattern": "^[.a-zA-Z0-9_]*$"
        },
        "description": {
            "type": "string",
            "description":
                "Human-readable description of the test run"
        },
        "status": {
            "type": "string",
            "description":
                "The test status, one of the following. "
                "\"ERROR\" - the test is faulty, "
                "the status of the tested code is unknown. "
                "\"FAIL\" - the test has failed, the tested code is faulty. "
                "\"PASS\" - the test has passed, the tested code is correct. "
                "\"DONE\" - the test has finished successfully, "
                "the status of the tested code is unknown. "
                "Missing property means the test wasn't executed.",
            "enum": ["ERROR", "FAIL", "PASS", "DONE"],
        },
        "waived": {
            "type": "boolean",
            "description":
                "True if the test status should be ignored",
        },
        "start_time": {
            "type": "string",
            "format": "date-time",
            "description":
                "The time the test run was started",
        },
        "duration": {
            "type": "number",
            "description":
                "The number of seconds it took to run the test",
        },
        "output_files": {
            "type": "array",
            "description":
                "A list of test outputs: logs, dumps, etc.",
            "items": JSON_RESOURCE,
        },
        "misc": {
            "type": "object",
            "description":
                "Miscellaneous extra data about the test run",
        },
    },
    "additionalProperties": False,
    "required": [
        "build_origin",
        "build_origin_id",
        "environment_origin",
        "environment_origin_id",
        "origin",
        "origin_id",
    ],
}

# JSON schema for I/O data
JSON = {
    "title": "kcidb",
    "description": "Kernelci.org test data",
    "type": "object",
    "properties": {
        "version": {
            "type": "string",
            "description": "Version of the schema the data complies to",
            "const": "1"
        },
        "revisions": {
            "description": "List of code revisions",
            "type": "array",
            "items": JSON_REVISION,
        },
        "builds": {
            "description": "List of builds",
            "type": "array",
            "items": JSON_BUILD,
        },
        "environments": {
            "description": "List of test environments",
            "type": "array",
            "items": JSON_ENVIRONMENT,
        },
        "tests": {
            "description": "List of test runs",
            "type": "array",
            "items": JSON_TEST,
        },
    },
    "additionalProperties": False,
    "required": [
        "version",
    ]
}


def validate(io_data):
    """Validate I/O data with its schema"""
    jsonschema.validate(instance=io_data, schema=JSON)
