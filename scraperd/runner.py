import os

from scraperd import get_application


def main():
    project = os.environ['SCRAPY_PROJECT']
    with project_environment(project):
        from scrapy.cmdline import execute
        execute()

if __name__ == '__main__':
    main()
