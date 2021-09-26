from livereload import Server, shell
import os
import argparse

DIRNAME = os.path.dirname(__file__)


parser = argparse.ArgumentParser()
parser.add_argument("--skip-fetch", help="uses pre-existing XMLs as cache", action="store_true")
args = parser.parse_args()
cmd = f'poetry run python -m meteo.scripts.build {"--skip-fetch" if args.skip_fetch else ""}'

server = Server()
server.watch(
  os.path.join(DIRNAME, '../templates/*.jinja'),
  shell(cmd)
)
server.watch(
  os.path.join(DIRNAME, '../templates/*.html'),
  shell(cmd)
)
server.watch(
  os.path.join(DIRNAME, '../**/*.py'),
  shell(cmd)
)
server.serve(root=os.path.join(DIRNAME, '../../docs'))
