from pathlib import Path
from fluent.runtime import FluentLocalization, FluentResourceLoader

def get_fluent_localization(language: str) -> FluentLocalization:
    locales_dir = Path(__file__).parent.joinpath("Locales")
    if not locales_dir.exists():
        err = '"Locales" does not exist'
        raise FileNotFoundError(err)
    if not locales_dir.is_dir():
        err = '"Locales" is not a directory'
        raise NotADirectoryError(err)

    locales_dir = locales_dir.absolute()
    locale_dir_found = False
    for directory in Path.iterdir(locales_dir):
        if directory.stem == language:
            locale_dir_found = True
            break
    if not locale_dir_found:
        err = f'Directory for "{language}" locale not found'
        raise FileNotFoundError(err)

    locale_files = list()
    for file in Path.iterdir(Path.joinpath(locales_dir, language)):
        if file.suffix == ".ftl":
            locale_files.append(str(file.absolute()))

    l10n_loader = FluentResourceLoader(str(Path.joinpath(locales_dir, "{locale}")))

    return FluentLocalization([language], locale_files, l10n_loader)
