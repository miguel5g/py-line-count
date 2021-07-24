import sys, os

valid_extensions = (
  '.ts',
  '.js',
  '.html',
  '.tsx',
  '.jsx',
  '.py',
  '.css',
  '.d.ts'
)

invalid_dirs = (
  'node_modules',
  'build',
  'output',
  'dist',
  '.git',
  '.vscode',
  '.next',
)

valid_args = (
  (('h', 'help'), 'boolean', 'Mostrar como usar o comando'),
  (('l', 'log'), 'boolean', 'Mostrar o path de cada arquivo analizado'),
  (('p', 'path'), 'string', 'Path para ser analizado'),
)

def countDir(path, show_header=True, log=True):
  # Retornar tupla de 0 caso o path fornecido não seja um diretório
  if not os.path.isdir(path): return (0, 0, 0)

  # Variáveis iniciais
  dir_items = os.listdir(path)
  lines = 0
  files = 0
  folders = 0

  # Mostrar o header
  if show_header and log and len(dir_items) > 0: print(f'\n{"Lines": <6} - Path\n')

  # Fazer um for em cada item dentro do diretório
  for item in dir_items:
    # Verificar se o item está dentro da lista de diretórios inválidos
    try:
      invalid_dirs.index(item)
    except:
      # Verificar se o item é um diretório
      if os.path.isdir(os.path.join(path, item)):
        result = countDir(os.path.join(path, item), False, log)
        lines += result[0]
        files += result[1]
        folders += (result[2] + 1)
        continue

      # Pegar a extensão do arquivo
      item_ext = item[item.find('.'):]

      # Verficar se a extensão é valida e contar as linhas do arquivo
      try:
        valid_extensions.index(item_ext)
        temp = file_len(os.path.join(path, item))
        lines += temp
        files += 1

        # Mostrar na tela o path do arquivo e quantida de linhas do arquivo
        if log: print('{: <6} - '.format(temp) + os.path.join(path, item))
      except:
        continue
  
  # Retornar resultados
  return (lines, files, folders)

# Contar a quantidade de linhas em um arquivo
def file_len(fname):
  with open(fname, encoding="utf8") as f:
    for i, l in enumerate(f):
      pass
  return i + 1

# Recuperar um argumento
def get_arg(name):
  arg = None

  for arg_help in valid_args:
    try:
      arg_help[0].index(name)

      type = arg_help[1]
      arg_names = arg_help[0]
      has = False

      try:
        for arg_name in arg_names:
          formated_arg_name = f'--{arg_name}' if len(arg_name) > 1 else f'-{arg_name}'


          try:
            if type == 'boolean':
              sys.argv.index(formated_arg_name)
              arg, has = True, True
              break
            elif type == 'string':
              index = sys.argv.index(formated_arg_name)
              arg = sys.argv[index + 1]
              has = True
              break
          except:
            pass
      except:
        pass
      finally:
        if has == False:
          if type == 'boolean': arg = False
          elif type == 'string': arg = ''
      break
    except:
      pass

  return arg

def show_helper():
  print('\nOlá! Vou te mostrar todas as opções.\n')
  print('{: <16} {: <8} {}'.format('Argumentos', 'Tipo', 'Descrição'))
  
  for arg_help in valid_args:
    print('{: <16} {: <8} {}'.format(', '.join(arg_help[0]), arg_help[1], arg_help[2]))

  print('')

if __name__ == '__main__':
  dir_path = get_arg('path')
  dir_path = dir_path if len(dir_path) > 0 else '.'
  log = get_arg('log')
  helper = get_arg('help')

  if helper:
    show_helper()
  else:
    result = countDir(dir_path, log=log)

    # Mostrar resultados bonitinho
    print(f'\nTotal de linhas: {result[0]}\nTotal de arquivos: {result[1]}\nTotal de pastas: {result[2]}\n')
