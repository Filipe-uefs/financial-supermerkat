from configparser import ConfigParser


def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Não foi possivel abrir conexão com o database'.format(section, filename))

    return config


if __name__ == '__main__':
    config = load_config()
    print(config)