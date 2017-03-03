import argparse, os, time

from hamplify.config import *
from hamplify.parsers.parser import Parser

arg_parser = argparse.ArgumentParser(description="Convert HAML files to HTML.")
arg_parser.add_argument("src", metavar="source", help="A path to a single file or dir containing .haml files")
arg_parser.add_argument("dst", metavar="dest", nargs="?", help="A path to where the "
  "converted file(s) should go (defaults to src directory)")
arg_parser.add_argument("-e", "--ext", metavar="extension", default=["haml"], nargs="+", 
  help="The extensions of the haml files to look for (defaults to 'haml')")
arg_parser.add_argument("-o", "--out", metavar="extension", default="html", nargs="?", 
  help="The extension to save the converted files as (defaults to 'html')")
arg_parser.add_argument("-v", "--verbose", action="store_true", 
  help="Verbose mode. Prints out file paths as files are being converted")
arg_parser.add_argument("--django", action="store_true", 
  help="Parses the file(s) with Django syntax and tag names")
arg_parser.add_argument("--jinja", action="store_true", 
  help="Parses the file(s) with Jinja syntax and tag names")

args = arg_parser.parse_args()
dir_stack = []
parser = None

if args.django:
    parser = Parser({"engine": ENGINE_DJANGO})
elif args.jinja:
  parser = Parser({"engine": ENGINE_JINJA})
else:
  parser = Parser()

# Output dir defaults to the source
if not args.dst:
  if os.path.isfile(args.src):
    args.dst = os.path.dirname(args.src)
  else:
    args.dst = args.src

# Make sure all extensions start with a period
for i in range(len(args.ext)):
  if not args.ext[i].startswith("."):
    args.ext[i] = "." + args.ext[i]

if not args.out.startswith("."):
  args.out = "." + args.out

# Normalize paths to be the full path
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

  # Converting just a single file
  if os.path.isfile(args.src):
    convert_file()

    if args.verbose:
      print()

    print("Finished converting in %d ms." % ((time.time() - earlier) * 1000))
  else:
    count = convert_dir()

    if args.verbose and count > 0:
      print()

    print("Finished converting %d files in %d ms." % (count, (time.time() - earlier) * 1000))

def create_out_dir(path):
  try:
    os.makedirs(path)
  except OSError:
    pass

def convert_dir():
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
          write_file(os.path.join(path, f), os.path.join(out_path, f[:-len(ext)]) + args.out)
          converted += 1
          break

  return converted

def convert_file():
  """ Converts a single file
  """

  create_out_dir(os.path.dirname(args.dst))
  file_name = os.path.basename(args.src).split(".")[0] + args.out
  write_file(args.src, os.path.join(args.dst, file_name))

def write_file(in_file, out_file):
  """ Converts a file and saves it to the destination folder
  """

  earlier = time.time()

  with open(in_file, "r") as fin:
    with open(out_file, "w") as fout:
      buffer = fin.read()
      fout.write(parser.parse(buffer).render())

  if args.verbose:
    print()
    print("Input file:   %s" % os.path.relpath(in_file))
    print("Output file:  %s" % os.path.relpath(out_file))
    print("Conversion took %.3f ms" % ((time.time() - earlier) * 1000))