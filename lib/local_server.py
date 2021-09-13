from livereload import Server, shell

server = Server()
server.watch(
  'index.mustache',
  shell('python3 build.py --use-cache', cwd='scripts')
)
server.watch(
  'scripts/build.py',
  shell('python3 build.py', cwd='scripts')
)
server.serve(root='./build/')
