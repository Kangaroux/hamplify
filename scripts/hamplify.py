import argparse, os, time

from hamplify.parsers.parser import Parser

arg_parser = argparse.ArgumentParser(description="Convert HAML files to HTML.")
arg_parser.add_argument("src", metavar="source", help="A path to a file_name or dir containing .haml files")
arg_parser.add_argument("dst", metavar="dest", nargs="?", help="A path to where the "
  "converted file(s) should go (defaults to src directory)")
arg_parser.add_argument("-e", "--ext", metavar="extension", default=["haml"], nargs="+", 
  help="The extensions of the haml files to look for (defaults to 'haml')")
arg_parser.add_argument("-o", "--out", metavar="extension", default="html", nargs="?", 
  help="The extension to save the converted files as (defaults to 'html')")

args = arg_parser.parse_args()
dir_stack = []
parser = Parser()

# Output dir defaults to the source
if not args.dst:
  args.dst = args.src

# Make sure all extensions start with a period
for i in range(len(args.ext)):
  if not args.ext[i].startswith("."):
    args.ext[i] = "." + args.ext[i]

if not args.out.startswith("."):
  args.out = "." + args.out

#
args.src = os.path.realpath(args.src)
args.dst = os.path.realpath(args.dst)

def main():
  """ Main entrypoint for the script
  """

  if not os.path.exists(args.src):
    print("Source path or file does not exist: %s" % args.src)
    exit(1)

  print("Working...")
  earlier = time.time()
  count = convert()
  print("Finished converting %d files in %dms." % (count, (time.time() - earlier) * 1000))

def create_out_dir(path):
  try:
    os.makedirs(path)
  except OSError:
    pass

def convert():
  """ Recursively walks a path, converting every haml file it finds, then returns how
  many files were converted
  """

  converted = 0
  
  for path, dirs, files in os.walk(args.src):
    out_path = os.path.join(args.dst, os.path.relpath(path, args.src))

    # This is the case where the destination path is inside the source folder.
    # If we find it while walking, skip over it, otherwise weird recursive
    # stuff can happen
    if path.startswith(args.dst) and args.dst != args.src:
      continue

    create_out_dir(out_path)
    
    for f in files:
      # Check if the file extension matches
      for ext in args.ext:
        if f.endswith(ext):
          # Remove the extension so we can replace it with the output extension
          convert_file(os.path.join(path, f), os.path.join(out_path, f[:-len(ext)]))
          converted += 1
          break

  return converted

def convert_file(in_file, out_file):
  """ Converts a file and saves it to the destination folder
  """

  with open(in_file, "r") as fin:
    with open(out_file + args.out, "w") as fout:
      buffer = fin.read()
      parser._reset()
      fout.write(parser.parse(buffer).render())