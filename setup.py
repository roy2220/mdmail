from distutils.core import setup

setup(
    name="mdmail",
    version="0.2.2",
    description="A tool to send mails written in Markdown",
    packages=["mdmail"],
    package_dir={"mdmail": "src/mdmail"},
    package_data={
        "mdmail": [
            "github-markdown-css/github-markdown.css",
        ]
    },
    entry_points={
        "console_scripts": [
            "mdmail=mdmail:main",
        ],
    },
    python_requires=">=3.9",
    install_requires=[
        "Markdown==3.3.6",
    ],
)
