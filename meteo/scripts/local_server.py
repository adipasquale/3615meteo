from livereload import Server, shell
import os

DIRNAME = os.path.dirname(__file__)

server = Server()
server.watch(
  os.path.join(DIRNAME, '../templates/*.jinja'),
  shell('poetry run python -m meteo.scripts.build')
)
server.watch(
  os.path.join(DIRNAME, '../templates/*.html'),
  shell('poetry run python -m meteo.scripts.build')
)
server.watch(
  os.path.join(DIRNAME, '../**/*.py'),
  shell('poetry run python -m meteo.scripts.build')
)
server.serve(root=os.path.join(DIRNAME, '../../docs'))
