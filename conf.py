import toml
from util import *


def validate_args(args):
    config = {
        'input_path': args.input,
        'inplace': args.inplace,
        'sort': args.sort,
        'space': args.space,
        'merge': args.merge,
        'verbose': args.verbose
    }

    if args.config != None:
        info("using config file, overwriting other commandline options")
        config_path = args.config
        validate_config(config, config_path)

    return config


# validate the config from the file
def validate_config(config, config_path):
    config_valid = True
    with open(config_path) as config_file:
        conf_dict = toml.load(config_file)

        # TODO: add validation of config here

        # now we update the original config with the content from the file
        for conf_key in conf_dict:
            config[conf_key] = conf_dict[conf_key]

    if not config_valid:
        error("invalid config file")
        exit(1)
