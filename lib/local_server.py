from livereload import Server, shell

server = Server()
server.watch(
  '*.mustache',
  shell('python build.py', cwd='lib')
)
server.watch(
  'lib/*.py',
  shell('python3 build.py', cwd='lib')
)
server.serve(root='./build/')
