"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()


def sort_most_important_first(path: Path):
    if path.name == 'kaspersmicrobit.py':
        return Path("_1", path)
    elif path.parts[2] == 'services':
        return Path("_2", path)
    elif path.name != 'bluetoothdevice.py':
        return Path("_3", path)
    else:
        return path


paths = sorted(Path("src").glob("**/*.py"), key=sort_most_important_first)

for path in paths:
    module_path = path.relative_to("src").with_suffix("")
    doc_path = path.relative_to("src", "kaspersmicrobit").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    if parts[-1] != '__init__':
        nav[parts] = str(doc_path)

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(module_path.parts)
            print("::: " + ident, file=fd)

        mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
