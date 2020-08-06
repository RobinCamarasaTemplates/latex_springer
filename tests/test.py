"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-08-06

**Project** : Latex Springer Template

**Test project generation of Latex Springer Template**

"""
import sys
import os
from datetime import datetime
import pytest
import shutil
from pathlib import Path
from cookiecutter import main
import subprocess


ROOT = Path(__file__).parents[1]
TESTS_ROOT = ROOT / 'test_output'
EXTRA_CONTEXT = {
    "repo_name": "test_repo",

    "author_names": "John Doe and Doe John",
    "author_institutions": "Lambda company and Omega company",
    "author_names_running": "J. Doe et al.",

    "article_title": "Wonderful explanation of life",
    "article_title_running": "Explanation of life"
}


def test_generate_project() -> None:
    """
    Test project generation

    :return: None
    """
    # Clean
    if TESTS_ROOT.exists():
        shutil.rmtree(TESTS_ROOT)
    TESTS_ROOT.mkdir()

    # Get path
    output_dir = TESTS_ROOT.resolve()

    # Launch project generation
    main.cookiecutter(
        str(ROOT),
        no_input=True,
        extra_context=EXTRA_CONTEXT,
        output_dir=output_dir
    )

    assert (
        TESTS_ROOT / EXTRA_CONTEXT['repo_name']
    ).exists()

    files = [
        'lit.bib', 'llncs.cls',
        'main.tex', 'splncs04.bst',
    ]

    for file_ in files:
        assert (
            TESTS_ROOT / EXTRA_CONTEXT['repo_name'] /\
            file_
        ).exists()

    # Test compilation
    folder_path = (
        TESTS_ROOT / EXTRA_CONTEXT['repo_name']
    ).resolve()
    process = subprocess.Popen(
        ['pdflatex', 'main.tex'],
        cwd=folder_path
    )
    process.wait()
    process = subprocess.Popen(
        ['bibtex', 'main.aux'],
        cwd=folder_path
    )
    process.wait()
    process = subprocess.Popen(
        ['pdflatex', 'main.tex'],
        cwd=folder_path
    )
    process.wait()
    process = subprocess.Popen(
        ['pdflatex', 'main.tex'],
        cwd=folder_path
    )
    process.wait()

    assert (
        TESTS_ROOT / EXTRA_CONTEXT['repo_name'] / 'main.pdf'
    ).exists()


