import setuptools

with open("README.md", "r", encoding ="utf-8") as f:
    long_description = f.read()

__version__="0.0.0"

REPO_NAME = "chicken-diseases-Detection2"
Author_user_name = "PratikPatel2407"
SRC_REPO = "objectDetecction"
AUTHOR_EMAIL = "pratikpatel24@hotmail.com"


setuptools.setup(
    name=SRC_REPO,
    author=Author_user_name,
    author_email=AUTHOR_EMAIL,
    description="a cnn model to detect chicken disease",
    Long_description=long_description,
    Long_description_content = "text/markdown",
    url=f"https://github.com/{Author_user_name}/{REPO_NAME}",
    project_urls={
        "Bug Tracker":f"https://github.com/{Author_user_name}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages= setuptools.find_packages(where="src")

)

